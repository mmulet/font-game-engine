
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import IntProperty, StringProperty
from ..Common import image_object
from .get_slot_info import get_slot_info


class SelectSlotOperator(Operator, Plugin):
    """Select all objects in a scene with the correct slot"""
    bl_idname = "font.selectslot"
    bl_label = "Select Objects"
    bl_options = {'REGISTER', 'UNDO'}
    nodeSceneName: StringProperty()

    slotNumber: IntProperty(default=0)

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.selectSlotOperator(context)
        return {'FINISHED'}

    def selectSlotOperator(self, context):
        # type: (bpy.ContextType) -> None
        try:
            scene = bpy.data.scenes[self.nodeSceneName]
        except KeyError:
            self.report({"ERROR"}, "No scene attached to the node!")
            return

        found_objects = []  # type: list[bpy.EmptyImageObjectTypeWithData]

        for o in scene.objects:
            image_o = image_object(o)
            if image_o is None:
                continue
            slot_info = get_slot_info(image_o)
            if slot_info is None or slot_info.number != self.slotNumber:
                continue
            found_objects.append(image_o)
        if len(found_objects) <= 0:
            self.report(
                {"ERROR"}, "Couldn't find any objects with that slot number!")
            return
        context.window.scene = scene
        for o in found_objects:
            o.select_set(True)
