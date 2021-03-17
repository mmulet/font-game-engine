 
from .ExportError import ExportError
# from ..bpy import *
import bpy


def get_node_scene(node):
    # type: (bpy.AllSceneNodeTypes) -> bpy.types.Scene
    scene = node.node_scene
    if not scene:
        raise ExportError("Node is missing a scene", [node])
    return scene
