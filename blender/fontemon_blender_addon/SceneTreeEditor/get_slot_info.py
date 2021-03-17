import bpy
from .SlotInfo import SlotInfo


def get_slot_info(o):
    # type: (bpy.EmptyImageObjectType) -> bpy.Optional[SlotInfo]
    if not ('font_is_a_slot' in o):
        return None
    if not o['font_is_a_slot']:
        return None
    return SlotInfo(name=o['font_slot_name'], number=o['font_slot_number'])
