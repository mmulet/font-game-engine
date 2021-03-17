
from ..Plugin import Plugin
from bpy.types import Operator
import bpy


class AddFontTextOperator(Operator, Plugin):
    """Add lines of text to the scene"""
    bl_idname = "font.add_font_text"
    bl_label = "Add font text"
    bl_icon = "SYNTAX_OFF"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        bpy.ops.object.font_create_text()
        return {'FINISHED'}

 
