import bpy
import json
from .get_first_node import get_first_node
from .get_lost_scene_node import get_lost_scene_node
from .export_scene_node_to_script import export_scene_node_to_script

def export_scene_tree_to_script(nodes, filepath) -> None:
    # type: (list[bpy.AllNodeTypes], str) -> bpy.Literal[True]
    """Export a scene Tree to a script."""
    first_node = get_first_node(nodes)
    lost_scene_node = get_lost_scene_node(first_node)
    scene_scripts = {}  # type: bpy.SceneScriptsType
    export_scene_node_to_script(first_node, set(), scene_scripts)
    export_scene_node_to_script(lost_scene_node, set(), scene_scripts)
    out = {
        'scenes': scene_scripts
    }
    with open(filepath, 'w') as f:
        _ = f.write(json.dumps(out))




