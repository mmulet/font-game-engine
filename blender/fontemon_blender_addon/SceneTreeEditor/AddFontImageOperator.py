
from ..Plugin import Plugin
from bpy.types import Operator
import bpy


class AddFontImageOperator(Operator, Plugin):
    """Add an image to the scene. This image will be in the final game"""
    bl_idname = "font.add_font_image"
    bl_label = "Add font image"
    bl_icon = "IMAGE_DATA"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        bpy.ops.object.empty_add(type='IMAGE')
        return {'FINISHED'}
