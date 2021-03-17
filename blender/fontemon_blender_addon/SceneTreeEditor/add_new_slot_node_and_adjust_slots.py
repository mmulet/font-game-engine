import bpy
from .adjust_slot_numbers import adjust_slot_numbers


def add_new_slot_node_and_adjust_slots(nodes, connected_nodes, new_slot_number, position):
    # type: (bpy.types.Nodes, list[bpy.SlotNodeType], int, list[float]) -> None
    slot_node = nodes.new("SlotNode")
    slot_node.slot_name = ""
    slot_node.slot_number = new_slot_number
    slot_node.location = position  # [node.location[0], node.location[1]]
    slot_node.select = True
    slot_node.width = 250
    adjust_slot_numbers(
        connected_nodes,
        new_slot_number,
        increase_slot_number=True
    )
