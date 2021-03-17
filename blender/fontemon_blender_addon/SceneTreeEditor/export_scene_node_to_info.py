
from .create_scene_info import create_scene_info
from .node_to_scene_path_id import node_to_scene_path_id
import bpy
from .get_linked_scene_nodes import get_linked_scene_nodes

def export_scene_node_to_info(node, scene_type, out_scene_node_infos, out_scene_infos, out_scene_node_id_to_node):
    # type: (bpy.AllSceneNodeTypes, bpy.ExportSceneType,bpy.SceneNodeInfosType, bpy.SceneInfosType,  dict[bpy.NodeId, bpy.AllSceneNodeTypes]) -> None
    """Recursively walk the node tree and compute the scene node to scene info.
     Each scene info is only created once, and is stored in scene_infos. 
     Every possible path is walked to find and eliminate circular dependencies """
    scene_path_id = node_to_scene_path_id(node)

    out_scene_node_id_to_node[scene_path_id] = node
    scene_info_id = ("first_scene" if scene_type == "first_scene"
                     else "lost_scene" if scene_type == "lost_scene"
                     else scene_path_id)
    
    if scene_info_id in out_scene_node_infos:
        return
    scene_info = create_scene_info(node, out_scene_infos)
    out_scene_node_infos[scene_info_id] = scene_info
    next_scene_nodes = get_linked_scene_nodes(node)
    for next_node in next_scene_nodes:
        export_scene_node_to_info(
            node=next_node,
            scene_type=False,
            out_scene_node_infos=out_scene_node_infos,
            out_scene_infos=out_scene_infos,
            out_scene_node_id_to_node=out_scene_node_id_to_node,
            )
