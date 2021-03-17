
from .SceneTreeNode import SceneTreeNode
from ..Plugin import Plugin
from bpy.types import Node, Scene
from bpy.props import PointerProperty
from .draw_slot_buttons import draw_slot_buttons
from .draw_node_scene import draw_node_scene
from .Slots import Slots
import bpy


class FirstSceneNode(Node, SceneTreeNode, Slots, Plugin):
    '''The first scene in the game.
    Every scene tree needs exactly one of these.'''
    bl_idname = 'FirstSceneNode'
    bl_label = 'First Scene Node'
    bl_icon = "TRIA_RIGHT"
    node_scene: PointerProperty(
        name="Scene", type=Scene)

    def init(self, context):
        # type: (bpy.ContextType) -> None
        _ = self.outputs.new('NodeSocketFloat', "Scene")
        _ = self.outputs.new('NodeSocketFloat', "Lost Scene")

    def draw_buttons(self, context, layout):
        # type: (bpy.ContextType,bpy.types.UILayout) -> None
        draw_node_scene(self, layout)
        draw_slot_buttons(self, layout)

    def draw_label(self):
        if not self.node_scene:
            return "First Scene: empty"
        return "First Scene: " + self.node_scene.name
