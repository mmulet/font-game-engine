
from .SceneTreeNode import SceneTreeNode
from ..Plugin import Plugin
from bpy.types import Node
from bpy.props import StringProperty
import bpy


class ConditionNode(Node, SceneTreeNode, Plugin):
    '''A Node Representing a condition. Place between scene nodes
    if you want to connect two scenes unconditionally, then
    just connect them directly, don't use this node'''
    bl_idname = 'ConditionNode'
    bl_label = 'Condition Node'
    bl_icon = "SORTALPHA"

    condition_key: StringProperty(
        name="Key", description="The key on which this switches")

    def init(self, context):
        # type: (bpy.ContextType) -> None
        _ = self.inputs.new('SceneInputSocket', "Scene")
        _ = self.outputs.new('NodeSocketFloat', "Scene")

    def draw_buttons(self, context, layout):
        # type: (bpy.ContextType, bpy.types.UILayout) -> None
        _ = layout.prop(self, 'condition_key')

    def draw_label(self):
        if not self.condition_key:
            return "empty condition"
        return self.condition_key
