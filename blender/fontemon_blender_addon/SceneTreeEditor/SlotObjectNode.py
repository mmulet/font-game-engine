
from .SceneTreeNode import SceneTreeNode
from ..Plugin import Plugin
import bpy
from bpy.types import Node, Object
from bpy.props import PointerProperty, StringProperty


class SlotObjectNode(Node, SceneTreeNode, Plugin):
    '''A Node Representing an object with a slot'''
    bl_idname = 'SlotObjectNode'
    bl_label = "Slot Object Node"

    object: PointerProperty(
        name="Scene", type=Object)

    parent_name: StringProperty(name="ParentName")

    def init(self, context):
        # type: (bpy.ContextType) -> None
        _ = self.inputs.new('SceneInputSocket', "Scene")
        _ = self.outputs.new('NodeSocketFloat', "Scene")

    def draw_buttons(self, context, layout):
        # type: (bpy.ContextType, bpy.types.UILayout) -> None
        _ = layout.prop(self, "object")
        if self.parent_name != "":
            layout.label(text=f"Parent Name: {self.parent_name}")

    def draw_label(self):
        if not self.object:
            return "empty"
        return self.object.name
