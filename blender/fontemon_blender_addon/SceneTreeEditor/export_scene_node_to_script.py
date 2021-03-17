import bpy
from .get_linked_scene_nodes import get_linked_scene_nodes
from .get_node_scene import get_node_scene
from .get_scene_script import get_scene_script

def export_scene_node_to_script(node, out_visited_nodes, out_scene_scripts):
    # type: (bpy.AllSceneNodeTypes, set[str], bpy.SceneScriptsType) -> None
    if node.name in out_visited_nodes:
        return
    out_visited_nodes.add(node.name)
    scene = get_node_scene(node)
    if scene.name not in out_scene_scripts:
        out_scene_scripts[scene.name] = get_scene_script(scene)
    next_nodes = get_linked_scene_nodes(node)
    for next_node in next_nodes:
        export_scene_node_to_script(
            next_node,
            out_visited_nodes,
            out_scene_scripts
        )


        

