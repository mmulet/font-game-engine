
import bpy
from bpy.types import Menu

def menu_func_export(self, context):
    # type: (Menu, bpy.ContextType) -> None
    layout = self.layout
    layout.operator("font.add_font_image", icon="IMAGE_DATA")
    layout.operator("font.add_font_text", icon="SYNTAX_OFF")
    layout.operator("font.add_font_animation", icon="RENDER_ANIMATION")


class AddFontImageAndTextMenu:
    @classmethod
    def plug_in(cls):
        bpy.types.VIEW3D_MT_add.prepend(menu_func_export)

    @classmethod
    def plug_out(cls):
        bpy.types.VIEW3D_MT_add.remove(menu_func_export)
