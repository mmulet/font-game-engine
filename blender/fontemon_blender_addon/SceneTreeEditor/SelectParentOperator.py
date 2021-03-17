
from ..Plugin import Plugin
import bpy
from bpy.types import Operator

class SelectParentOperator(Operator, Plugin):
    """Select the parent of this object"""
    bl_idname = "font.selectparent"
    bl_label = "Select Parent"



    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.select_parent(context)
        return {'FINISHED'}

    def select_parent(self, context):
        # type: (bpy.ContextType) -> None
        o = context.active_object
        context.view_layer
        if o is None:
            return
        if o.parent is None:
            return
        context.view_layer.objects.active = o.parent
        for selected_o in context.selected_objects:
            selected_o.select_set(False)
        o.parent.select_set(True)
