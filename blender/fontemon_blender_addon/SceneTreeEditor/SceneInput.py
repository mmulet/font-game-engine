 
from ..Plugin import Plugin
import bpy
from bpy.types import NodeSocket


class SceneInput(NodeSocket, Plugin):
    '''Custom socket type,. probably don't need this'''
    bl_idname = 'SceneInputSocket'
    bl_label = "Scene Input Socket"

    def draw(self, context, layout, node, text):
        # type: (bpy.ContextType, bpy.types.UILayout, bpy.AllNodeTypes, str) -> None
        layout.label(text=text)

    def draw_color(self, context, node):
        # type: (bpy.ContextType, bpy.AllNodeTypes) -> bpy.Tuple[float,float,float,float]
        return (1.0, 0.4, 0.216, 0.5)
