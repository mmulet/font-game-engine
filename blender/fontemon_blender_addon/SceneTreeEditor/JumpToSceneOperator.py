
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import StringProperty


class JumpToSceneOperator(Operator, Plugin):
    """Set this scene as the active scene"""
    bl_idname = "font.jumptoscene"
    bl_label = "Jump to Scene"
    bl_options = {'REGISTER', 'UNDO'}
    nodeSceneName: StringProperty()

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.jumpToScene(context)
        return {'FINISHED'}

    def jumpToScene(self, context):
        # type: (bpy.ContextType) -> None
        try:
            scene = bpy.data.scenes[self.nodeSceneName]
        except KeyError:
            self.report({"ERROR"}, "No scene attached to the node!")
            return
        context.window.scene = scene
