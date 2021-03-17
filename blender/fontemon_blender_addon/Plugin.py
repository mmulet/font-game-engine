
from bpy.utils import register_class, unregister_class
import bpy


class Plugin:
    @classmethod
    def plug_in(cls):
        register_class(cls)

    @classmethod
    def plug_out(cls):
        unregister_class(cls)


class MultiplePluginHolder:
    """Make a class variable called plugins 
    and this mixin will let you plug-in all the plugins"""
    plugins = []  # type: bpy.Sequence[bpy.PluginType]

    @classmethod
    def plug_in(cls):
        for p in cls.plugins:
            p.plug_in()

    @classmethod
    def plug_out(cls):
        for p in reversed(cls.plugins):
            p.plug_out()
