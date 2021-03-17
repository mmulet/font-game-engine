
from .SceneTreeNode import SceneTreeNode
from ..Plugin import Plugin
from .adjust_scene_inputs import adjust_inputs
import bpy
from bpy.types import Node, Scene
from bpy.props import IntProperty, PointerProperty
from .draw_slot_buttons import draw_slot_buttons
from .draw_node_scene import draw_node_scene
from .Slots import Slots

class EndSceneNode(Node, SceneTreeNode, Slots, Plugin):
    '''A Node Representing an end scene. 
    A scene that links to no other scenes'''
    bl_idname = 'EndSceneNode'
    bl_label = "End Scene Node"
    bl_icon = "TRIA_LEFT"

    number_of_inputs: IntProperty(
        default=1, min=1, update=adjust_inputs)

    node_scene: PointerProperty(
        name="Scene", type=Scene)

    def init(self, context):
        # type: (bpy.ContextType) -> None
        # End nodes all have the id of 0, we can have multiple
        # end nodes with the same scene because there are no
        # outputs for an end node. So we don't need to encode
        # the game state as a node position
        _ = self.inputs.new('SceneInputSocket', "Scene")

    def draw_buttons(self, context, layout):
        # type: (bpy.ContextType, bpy.types.UILayout) -> None
        draw_node_scene(self, layout)
        draw_slot_buttons(self, layout)
        _ = layout.prop(self, "number_of_inputs")

    def draw_label(self):
        if not self.node_scene:
            return "empty"
        return self.node_scene.name
