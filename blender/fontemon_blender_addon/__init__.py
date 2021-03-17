from .SceneTreeEditor import SceneTreeEditor
from .SizeImage import SizeImage
from .CreateText import CreateText
from .Plugin import MultiplePluginHolder
from .WebTools import StartWebServer

bl_info = {
    "name": "fontemon addon",
    "author": "Michael Mulet",
    "version": (1, 0),
    "blender": (2, 91, 0),
    "location": "",
    "description": "Everything needed to create and export fontemon levels",
    "warning": "",
    "doc_url": "",
    "category": "",
}


class AllAddonPlugins(MultiplePluginHolder):
    plugins = (SizeImage, SceneTreeEditor, CreateText, StartWebServer)


def register():
    AllAddonPlugins.plug_in()


def unregister():
    AllAddonPlugins.plug_out()


if __name__ == "__main__":
    register()
