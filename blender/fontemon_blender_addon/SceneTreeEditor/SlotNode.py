
from .SceneTreeNode import SceneTreeNode
from ..Plugin import Plugin
import bpy
from bpy.types import Node
from bpy.props import IntProperty, StringProperty
from .adjust_scene_inputs import adjust_inputs


class SlotNode(Node, SceneTreeNode, Plugin):
    '''A Node Representing a slot'''
    bl_idname = 'SlotNode'
    bl_label = "Slot Node"

    slot_number: IntProperty(
        name="Number",
        default=0,
        min=0,
        max=20
    )

    slot_name: StringProperty(name="Name")

    number_of_inputs: IntProperty(
        default=1, min=1, update=adjust_inputs)

    def init(self, context):
        # type: (bpy.ContextType) -> None
        _ = self.inputs.new('SceneInputSocket', "Object")

    def draw_buttons(self, context, layout):
        # type: (bpy.ContextType, bpy.types.UILayout) -> None
        props = layout.operator("font.addslotabove")
        props.node_name = self.name
        _ = layout.prop(self, "slot_number")
        _ = layout.prop(self, "slot_name")
        props = layout.operator("font.removeslotnode")
        props.node_name = self.name
        props = layout.operator("font.addslotbelow")
        props.node_name = self.name
        _ = layout.prop(self, "number_of_inputs")

    def draw_label(self):
        if self.slot_number < 0:
            return "empty"
        return f"Slot #: {self.slot_number}"
