# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

from http.server import SimpleHTTPRequestHandler
from bpy.path import abspath
from os.path import dirname, join
import bpy

handler_path = abspath(__file__)
webTools_path = dirname(handler_path)
addon_path = dirname(webTools_path)
web_dir = join(addon_path, "assets", "web")


class HandlerParent(SimpleHTTPRequestHandler):
    """Something is wrong with the type checking
    so it can't properly detect methods in the super class.
    So have to turn the type checking off in this file, and
    put the actual code in another file with the type checking on.
  """
    def __init__(self, *args, **kwargs):
        # type: (bpy.Any, bpy.Any) -> None
        # print(f"Going to run server at {web_dir}")
        super().__init__(*args, **kwargs, directory=web_dir)

    def send_file(self, f, file):
        # type: (bpy.Any, bpy.Any) -> None
        self.copyfile(f, file)

    def correct_path(self, path):
        # type: (str) -> str
        return self.translate_path(path)
