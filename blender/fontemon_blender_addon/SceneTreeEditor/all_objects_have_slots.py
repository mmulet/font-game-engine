import bpy
from .get_slot_info import get_slot_info

def all_objects_have_slots(objects):
    # type: (list[bpy.EmptyImageObjectTypeWithData]) -> bool
    for o in objects:
        if get_slot_info(o) is None:
            return False
    return True