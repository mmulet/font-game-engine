import bpy
from bpy.app.handlers import persistent
from http.server import ThreadingHTTPServer
from threading import Thread
from .Handler import HTTPHandler

server = None  # type: ThreadingHTTPServer | None
server_running: bool = False
class RunServer(Thread):
    def run(self):
        global server
        global server_running
        server = ThreadingHTTPServer(("", 8020), HTTPHandler)
        print("starting server")
        server_running = True
        server.serve_forever()
        server_running = False
        print("stopping server")

# strong reference to prevent garbage collection
thread = None # type: RunServer | None
@persistent
def after_load(_):
    # type: (bpy.Any) -> None
    global server
    if server is not None:
        return
    print("going to start server")
    thread = RunServer()
    thread.start()


class StartWebServer:
    @classmethod
    def plug_in(cls):
        bpy.app.handlers.load_post.append(after_load)
        # run this now, so that everything will work
        # immediately after installing the addon
        after_load(False)

    @classmethod
    def plug_out(cls):
        global server
        global server_running
        global thread
        bpy.app.handlers.load_post.remove(after_load)
        if server is None:
            return
        if server_running:
            server.shutdown()
        server = None
        thread = None