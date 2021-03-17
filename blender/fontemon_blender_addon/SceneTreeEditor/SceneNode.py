
from .SceneTreeNode import SceneTreeNode
from ..Plugin import Plugin
from .adjust_scene_inputs import adjust_inputs
import bpy
from bpy.types import Node, Scene
from bpy.props import IntProperty, PointerProperty
from .draw_slot_buttons import draw_slot_buttons
from .draw_node_scene import draw_node_scene
from .Slots import Slots


class SceneNode(Node, SceneTreeNode, Slots, Plugin):
    '''A Node Representing a scene'''
    bl_idname = 'SceneNode'
    bl_label = "Scene Node"
    bl_icon = "SCENE_DATA"

    number_of_inputs: IntProperty(
        default=1, min=1, update=adjust_inputs)

    node_scene: PointerProperty(
        name="Scene", type=Scene)

    def init(self, context):
        # type: (bpy.ContextType) -> None
        _ = self.inputs.new('SceneInputSocket', "Scene")
        _ = self.outputs.new('NodeSocketFloat', "Scene")

    def draw_buttons(self, context, layout):
        # type: (bpy.ContextType, bpy.types.UILayout) -> None
        draw_node_scene(self, layout)
        draw_slot_buttons(self, layout)
        _ = layout.prop(self, "number_of_inputs", text="Inputs")

    def draw_label(self):
        if not self.node_scene:
            return "empty"
        return self.node_scene.name
