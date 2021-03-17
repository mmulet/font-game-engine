
from ..Plugin import Plugin
from bpy.types import Operator
import bpy


class SelectChildrenAndShowOperator(Operator, Plugin):
    """Select all the children and show them in the Outliner"""
    bl_idname = "font.select_children_and_show"
    bl_label = "Select Children"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]

        self.select_children_and_show(context)
        return {'FINISHED'}

    def select_children_and_show(self, context):
        # type: (bpy.ContextType) -> None
        o = context.active_object
        if o is None or o.children is None:
            return
        for s in context.selected_objects:
            s.select_set(False)
      
            
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
        bpy.ops.outliner.show_active()
