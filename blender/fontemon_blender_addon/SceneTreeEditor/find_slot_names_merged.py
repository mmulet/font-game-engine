import bpy
from .find_slot_names import find_slot_names

def find_slot_names_merged(scene):
    # type: (bpy.Optional[bpy.types.Scene]) -> dict[int,str]
    out = find_slot_names(scene)
    return {slot: " and ".join(v) for slot, v in out.items()}
