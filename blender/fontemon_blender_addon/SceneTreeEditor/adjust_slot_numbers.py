import bpy


def adjust_slot_numbers(connected_nodes, new_slot_number, increase_slot_number):
    # type: (list[bpy.SlotNodeType], int, bool) -> None
    location_change = (-250 if increase_slot_number else 250)
    for node in connected_nodes:
        if node.slot_number < new_slot_number:
            continue
        node.slot_number += 1 if increase_slot_number else -1

        node.location[1] += location_change
        for input in node.inputs:
            for link in input.links:
                link.from_node.location[1] += location_change
