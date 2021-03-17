
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import StringProperty, IntProperty
from .multiple_image_objects import multiple_image_objects
from .evaluate_pattern import evaluate_pattern, PatternError


class AssignSlotsInPatternOperator(Operator, Plugin):
    """Assign slots in a pattern."""
    bl_idname = "font.assignslotsinpattern"
    bl_label = "Assign Slots"
    bl_options = {'UNDO'}

    pattern: StringProperty(
        name="Pattern",
        description="A python expression to return the filename given the index i"
    )
    slot_start: IntProperty(name="Slot start")

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.assign_slots_in_pattern(context)
        return {'FINISHED'}

    def assign_slots_in_pattern(self, context):
        # type: (bpy.ContextType) -> None
        objects = multiple_image_objects(context)
        if objects is None:
            return
        objects.sort(key=lambda o: o.name)
        for i in range(len(objects)):
            o = objects[i]
            try:
                o["font_slot_name"] = evaluate_pattern(
                    i, self.pattern)
            except PatternError as e:
                self.report(
                    {'ERROR'}, f"Error while running your pattern on i={e.i}. Try your pattern out in the blender script editor.")
            o['font_slot_number'] = i + self.slot_start
            o['font_is_a_slot'] = True
