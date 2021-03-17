
from .SceneTreeNode import SceneTreeNode
from ..Plugin import Plugin
import bpy
from bpy.types import Node, Scene
from bpy.props import PointerProperty


class SlotSceneNode(Node, SceneTreeNode, Plugin):
    '''A Node Representing a  scene with slots'''
    bl_idname = 'SlotSceneNode'
    bl_label = "Slot Scene Node"


    node_scene: PointerProperty(
        name="Scene", type=Scene)

    def init(self, context):
        # type: (bpy.ContextType) -> None
        _ = self.outputs.new('NodeSocketFloat', "Scene")

    def draw_buttons(self, context, layout):
        # type: (bpy.ContextType, bpy.types.UILayout) -> None
        _ = layout.prop(self, "node_scene")
        adjust_slots = layout.operator("font.adjustslots")
        adjust_slots.node_name = self.name

    def draw_label(self):
        if not self.node_scene:
            return "Slot Scene: empty"
        return "Slot Scene: " + self.node_scene.name
