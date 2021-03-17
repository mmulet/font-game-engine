import bpy
from .ExportError import ExportError
from .is_a_scene_node import is_a_scene_node


def get_lost_scene_node(first_node):
    # type: (bpy.FirstSceneNodeType) -> bpy.AllSceneNodeTypes
    lost_scene_links = first_node.outputs[1].links
    lost_scene_links_len = len(lost_scene_links)
    if lost_scene_links_len == 0:
        raise ExportError("No lost scene node!", [first_node])
    if lost_scene_links_len > 1:
        lost_nodes = [
            link.to_node for link in lost_scene_links]  # type: list[bpy.AllNodeTypes]
        lost_nodes.append(first_node)
        raise ExportError("More than one lost scene!", lost_nodes)
    maybe_lost_scene_node = lost_scene_links[0].to_node
    if maybe_lost_scene_node.bl_idname == "ConditionNode":
        raise ExportError(
            "Lost scene can't be connected to a condition!", [maybe_lost_scene_node])
    if maybe_lost_scene_node.bl_idname == "GotoLostNode":
        raise ExportError(
            "Lost scene can't be connected to a goto lost scene node!", [maybe_lost_scene_node])
    lost_scene_node = is_a_scene_node(maybe_lost_scene_node)
    if lost_scene_node is None:
        raise ExportError(
            "Lost scene is not connected to a scene Node!", [maybe_lost_scene_node])
    return lost_scene_node
