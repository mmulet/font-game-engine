
from .SceneTreeNode import SceneTreeNode
from ..Plugin import Plugin
import bpy
from bpy.types import Node


class GotoLostNode(Node, SceneTreeNode, Plugin):
    '''A Node Representing a scene'''
    bl_idname = 'GotoLostNode'
    bl_label = "Goto Lost Node"
    bl_icon = "DECORATE_DRIVER"

    def init(self, context):
        # type: (bpy.ContextType) -> None
        _ = self.inputs.new('SceneInputSocket', "Scene")

    def draw_buttons(self, context, layout):
        # type: (bpy.ContextType, bpy.types.UILayout) -> None
        pass

    def draw_label(self):
        return "Goto Lost"
