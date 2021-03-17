 

from .get_node_scene import get_node_scene
import bpy

def node_to_scene_path_id(node):
    # type: (bpy.AllSceneNodeTypes) -> bpy.NodeId
    scene = get_node_scene(node)
    return scene.name + node.name.replace(" ", "").replace(".","")
