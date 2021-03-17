import bpy
from .get_node_before import get_node_before
from .AdjustSlotsError import AdjustSlotsError
from .get_all_slot_nodes import get_all_slot_nodes


def get_all_connected_slot_nodes(node):
    # type: (bpy.SlotNodeType) -> list[bpy.SlotNodeType]
    object_node = get_node_before(node)
    if object_node is None:
        raise AdjustSlotsError(
            "Node is not connected to anything in the first slot!", [node])
    if object_node.bl_idname != "SlotObjectNode":
        raise AdjustSlotsError(
            "Node is not connected to an object node in the first slot!", [object_node, node])
    scene_node = get_node_before(object_node)
    if scene_node is None:
        raise AdjustSlotsError(
            "Node is not connected to anything in the first slot!", [node])
    if scene_node.bl_idname != "SlotSceneNode":
        raise AdjustSlotsError(
            "Node is not connected to a slot scene node in the first slot!", [scene_node, object_node, node])
    return get_all_slot_nodes(scene_node)
