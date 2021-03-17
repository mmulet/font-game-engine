import bpy
from ..Common import image_object
from .get_slot_info import get_slot_info


def find_slot_names(scene, merged = True):
    # type: (bpy.Optional[bpy.types.Scene], bool) -> dict[int, set[str]]
    if scene is None:
        return {}
    out = {}  # type: dict[int, set[str]]
    for o in scene.objects:
        image_o = image_object(o)
        if image_o is None:
            continue
        slot_info = get_slot_info(image_o)
        if slot_info is None or slot_info.name == "":
            continue
        names = out.setdefault(slot_info.number, set())
        names.add(slot_info.name)
    return out

    
