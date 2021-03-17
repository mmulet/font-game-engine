import bpy
from .ObjectSlotInfo import ObjectSlotInfo
from .SlotInfo import SlotInfo
from ..Common import image_object
from .AdjustSlotsError import AdjustSlotsError
from typing import cast, Any


def generate_object_slot_info(
        node):  # type: (bpy.SlotSceneNodeType) -> list[ObjectSlotInfo]
    """Go through the entire slots tree and look for errors. Return the info needed to fix the slots"""
    output = node.outputs[0]
    slot_numbers = {}  # type: dict[int, bpy.SlotNodeType]
    slot_infos = []  # type: list[ObjectSlotInfo]
    for link in output.links:
        slot_object_node = link.to_node
        if slot_object_node.bl_idname != "SlotObjectNode":
            raise AdjustSlotsError(
                "Linked to a node that is not a slot object node",
                [slot_object_node])
        if slot_object_node.object is None:
            raise AdjustSlotsError("Object node does not have an object!",
                                   [slot_object_node])
        socket = slot_object_node.outputs[0]
        image_o = image_object(cast(Any, slot_object_node.object))
        if image_o is None:
            raise AdjustSlotsError(
                "Object node is not connected to an image object. It's an object, but it isn't any image object",
                [slot_object_node])
        if len(socket.links) == 0:
            slot_infos.append(ObjectSlotInfo(image_o, None))
            continue
        if len(socket.links) > 1:
            raise AdjustSlotsError(
                "An image cannot be connected to multiple slots",
                [link.to_node])
        slot_link = socket.links[0]
        slot_node = slot_link.to_node
        if slot_node.bl_idname != "SlotNode":
            raise AdjustSlotsError("Linked to a node that is not a slot node",
                                   [slot_node])
        if slot_node.slot_number in slot_numbers:
            previous_slot_node = slot_numbers[slot_node.slot_number]
            # if they are not the same slot node then
            # it is an error
            if previous_slot_node.name != slot_node.name:
                raise AdjustSlotsError(
                    "Slot number used in more than one node!",
                    [slot_numbers[slot_node.slot_number], slot_node])
        slot_numbers[slot_node.slot_number] = slot_node
        if slot_node.slot_number < 0:
            raise AdjustSlotsError("Invalid slot number", [slot_node])
        slot_infos.append(
            ObjectSlotInfo(
                image_o, SlotInfo(slot_node.slot_name, slot_node.slot_number)))
    for i in range(len(slot_numbers)):
        if i in slot_numbers:
            continue
        raise AdjustSlotsError(f"Missing slot number #{i}", [])
    return slot_infos
