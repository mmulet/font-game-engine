
import bpy
from bpy.types import Menu
from bpy.utils import register_class, unregister_class
from .draw_search_operators import draw_search_operators

def menu_func_export(self, context):
    # type: (Menu, bpy.ContextType) -> None
    self.layout.menu("NODE_MT_search_menu")


class SceneTreeSearchMenu(Menu):
    bl_idname = "NODE_MT_search_menu"
    bl_label = "Search"

    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        # return context.space_data.tree_type == 'SceneTreeType'
        return True

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        layout = self.layout
        draw_search_operators(layout)

    @classmethod
    def plug_in(cls):
        register_class(cls)
        bpy.types.NODE_MT_editor_menus.append(menu_func_export)

    @classmethod
    def plug_out(cls):
        bpy.types.NODE_MT_editor_menus.remove(menu_func_export)
        unregister_class(cls)
