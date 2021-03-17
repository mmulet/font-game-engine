
from ..Plugin import Plugin
from bpy.types import Operator
import bpy


class ClearChildrenOperator(Operator, Plugin):
    """Clear all the children"""
    bl_idname = "font.clear_children"
    bl_label = "UnParent this object"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]

        self.clearchildren(context)
        return {'FINISHED'}

    def clearchildren(self, context):
        # type: (bpy.ContextType) -> None
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
