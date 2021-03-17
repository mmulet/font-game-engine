
from http import HTTPStatus
import bpy
from bpy.path import abspath, ensure_ext
from os.path import basename, dirname, join, splitext


from mimetypes import guess_type
from os import fstat
from json import  dumps, loads
from re import compile, Match
from base64 import b64decode
from .HandlerParent import HandlerParent


class HTTPHandler(HandlerParent):

    extensions_map = _encodings_map_default = {
        ".js": 'text/javascript',
        ".png": 'image/png',
        ".jpeg": 'image/jpeg',
        ".jpg": 'image/jpeg',
        ".gif": 'image/gif',
        '.otf': 'font/otf',
        '.gz': 'application/gzip',
        '.Z': 'application/octet-stream',
        '.bz2': 'application/x-bzip2',
        '.xz': 'application/x-xz',
    }


    def guess_type(self, path):
        # type: (str) -> str
        """Guess the type of a file.
        Argument is a PATH (a filename).
        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.
        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.
        """
        _, ext = splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        guess, _ = guess_type(path)
        if guess:
            return guess
        return 'application/octet-stream'

    def get_image_type(self, path):
        # type: (str) -> str
        _, ext = splitext(path)
        if ext == ".png":
            return "image/png"
        if ext == ".jpeg" or ext == ".jpg":
            return "image/jpeg"
        if ext == ".gif":
            return "image/gif"
        if ext == ".webp":
            return "image/webp"
        return f"image/{ext.split('.')[1]}"

    def send_image(self, path, headers=[]):
        # type: (str, list[bpy.Tuple[str,str]]) -> None
        try:
            f = open(path, 'rb')
        except OSError:
            return self.send_error(HTTPStatus.NOT_FOUND, "File not found")
        try:
            fs = fstat(f.fileno())
            self.send_response_only(HTTPStatus.OK)
            self.send_header("Content-type", self.get_image_type(path))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(fs[6]))
            for key, value in headers:
                self.send_header(key, value)
            # self.send_header("Last-Modified",
            #                  self.date_time_string(fs.st_mtime))
            self.end_headers()

        except:
            f.close()
            raise
        try:
            self.send_file(f, self.wfile)
        finally:
            f.close()

    

    def get_font(self):
        use_most_recent_export = bpy.context.window_manager.converter_props.use_most_recent_export
        otf_file_path = bpy.context.window_manager.converter_props.otf_file_path
        most_recent_otf_export_path = bpy.context.window_manager.converter_props.most_recent_otf_export_path
        otf_path = ensure_ext(
            abspath(most_recent_otf_export_path
                    if use_most_recent_export else otf_file_path), ".otf")
        try:
            f = open(otf_path, 'rb')
        except OSError:
            return self.send_error(HTTPStatus.NOT_FOUND, "File not found")
        try:
            fs = fstat(f.fileno())
            self.send_response_only(HTTPStatus.OK)
            self.send_header("Content-type", "font/otf")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(fs[6]))
            self.end_headers()
        except:
            f.close()
            raise
        try:
            self.send_file(f, self.wfile)
        finally:
            f.close()
        return

    def load_image(self, input):
        # type: (bpy.LoadImageInput) -> None
        self.send_image(input["filePath"])

    numbers_at_end = compile(r"\d+$")

    def next_image(self, input):
        # type: (bpy.NextImageInput) -> None
        imageFilePath = input['imageFilePath']
        withoutExt, ext = splitext(imageFilePath)
        name = basename(withoutExt)

        def increase_num(match):
            # type: (Match[str]) -> str
            matching_string = match[0]
            return str(int(matching_string) + 1).zfill(len(matching_string))

        next_name = self.numbers_at_end.sub(increase_num, name)
        if next_name == name:
            return self.send_error(HTTPStatus.NOT_FOUND, "File not found")
        next_file_path = join(dirname(imageFilePath), f"{next_name}{ext}")
        self.send_image(path=next_file_path,
                        headers=[("next-file-path", next_file_path)])

    def save_file(self, input):
        # type: (bpy.SaveFileInput) -> None
        name = basename(input["name"])
        pngURL = input["pngURL"]
        comma = pngURL.index(",")
        if comma < 0:
            return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid ata url")
        data = b64decode(pngURL[comma:])
        # filePath = abspath(bpy.data.filepath)
        # blenderFilesPath = dirname(filePath)
        # blenderPath = dirname(blenderFilesPath)
        # projectRootDirectoryPath = dirname(blenderPath)
        # imagesPath = join(projectRootDirectoryPath, "images")
        imagesPath = abspath(
            bpy.context.window_manager.converter_props.images_folder)
        with open(join(imagesPath, f"{name}.png"), "wb") as f:
            _ = f.write(data)
        with open(join(imagesPath, "charStrings", f"{name}.charstring"),
                  "w") as f:
            _ = f.write(input["charStringInfo"])
        self.send_response_only(HTTPStatus.OK)
        self.end_headers()

    def should_reload_preview(self, input):
        # type: (bpy.ShouldReloadInput) -> None
        export_number =  bpy.context.window_manager.converter_props.export_number
        output = {
            'should_reload':export_number != input['export_number'],
            'export_num': export_number
        } #type: bpy.ShouldReloadOutput
        output_s = bytes(dumps(output), encoding="utf8")
        self.send_response_only(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(output_s)))
        self.end_headers()
        _ = self.wfile.write(output_s)
        return

    def do_POST(self) -> None:
        path = self.path
        length = int(self.headers['Content-Length'])
        input = loads(self.rfile.read(length))
        if path == "/loadImage":
            self.load_image(input=input)
            return
        if path == "/nextImage":
            self.next_image(input=input)
            return
        if path == "/saveFile":
            self.save_file(input=input)
            return
        if self.path == "/reloadPreview":
            self.should_reload_preview(input=input)
            return

    def do_GET(self) -> None:
        if self.path == "/getFont":
            self.get_font()
            return
        f = self.send_head()
        if not f:
            return
        try:
            self.send_file(f, self.wfile)
        finally:
            f.close()

    def send_head(self):
        path: str = self.correct_path(self.path)
        f = None
        ctype = self.guess_type(path)
        if path.endswith("/"):
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

        try:
            fs = fstat(f.fileno())
            self.send_response_only(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(fs[6]))
            # self.send_header("Last-Modified",
            #                  self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise
