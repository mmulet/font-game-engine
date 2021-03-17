from .export_scene_node_to_info import export_scene_node_to_info
# from .is_an_end_node import is_an_end_node
import bpy
from .get_first_node import get_first_node
from .get_lost_scene_node import get_lost_scene_node


def export_scene_tree_to_info(nodes):
    # type: (list[bpy.AllNodeTypes]) ->  bpy.SceneTreeOutputType
    """Export a scene Tree to a json file. 
    Also validates and highlights errors."""
    first_node = get_first_node(nodes)
    lost_scene_node = get_lost_scene_node(first_node)
    scene_node_infos = {}  # type: bpy.SceneNodeInfosType
    scene_infos = {}  # type: bpy.SceneInfosType
    scene_node_id_to_node = {}  # type: dict[str, bpy.AllSceneNodeTypes]
    export_scene_node_to_info(
        node=first_node,
        scene_type="first_scene",
        out_scene_node_infos=scene_node_infos,
        out_scene_infos=scene_infos,
        out_scene_node_id_to_node=scene_node_id_to_node,
    )

    # The lost path cannot contain a reference to any of the other
    # nodes in the scene, except for end nodes
    # ( no worry about circular references with end nodes)
    # lost_scene_path = {
    #     key: node for (key, node) in
    #     scene_node_id_to_node.items() if not is_an_end_node(node)}
    export_scene_node_to_info(
        node=lost_scene_node,
        scene_type="lost_scene",
        out_scene_node_infos=scene_node_infos,
        out_scene_infos=scene_infos,
        out_scene_node_id_to_node=scene_node_id_to_node,
    )

    out = {
        'nodes': scene_node_infos,
        'scenes': scene_infos
    }  # type: bpy.SceneTreeOutputType
    return out
