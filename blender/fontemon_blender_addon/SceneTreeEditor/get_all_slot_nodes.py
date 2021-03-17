import bpy
from .AdjustSlotsError import AdjustSlotsError


def get_all_slot_nodes(node):
    # type: (bpy.SlotSceneNodeType) -> list[bpy.SlotNodeType]
    found_nodes = {}  # type: dict[str, bpy.SlotNodeType]
    output = node.outputs[0]
    for link in output.links:
        object_node = link.to_node
        if object_node.bl_idname != "SlotObjectNode":
            raise AdjustSlotsError(
                "Linked to a node that is not a slot object node", [object_node])
        output = object_node.outputs[0]
        # allow multiple links for now,
        # because the user may still
        # be adjusting things
        for link in output.links:
            slot_node = link.to_node
            if slot_node.bl_idname != "SlotNode":
                raise AdjustSlotsError(
                    "Linked to a node that is not a slot node", [slot_node])
            found_nodes[slot_node.name] = slot_node
    return list(found_nodes.values())
