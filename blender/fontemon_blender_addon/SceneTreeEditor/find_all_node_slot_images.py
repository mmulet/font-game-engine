import bpy
from .nodes_from_context import nodes_from_context
from .is_a_scene_node import is_a_scene_node
from .get_slot_image import get_slot_image
from bpy.path import basename
from typing import NamedTuple

class SlotImages(NamedTuple):
    all: "set[str]"
    selected: "set[str]"


def find_all_node_slot_images(context, use_image_file_name=True):# type: (bpy.Optional[bpy.ContextType], bool) -> SlotImages
    """use_image_file_name will use the basename of the file path as opposed to the name of the image data block"""
    nodes = nodes_from_context(context)
    if nodes is None:
        return SlotImages(set(), set())
    all_image_names = set()  # type: set[str]
    selected_image_names = set()  # type: set[str]
    for item in nodes:
        node = is_a_scene_node(item)
        if node is None:
            continue
        if node.number_of_slots <= 0:
            continue
        for i in range(node.number_of_slots):
            image = get_slot_image(node, i + 1)
            if image is None:
                continue
            name = basename(
                image.filepath) if use_image_file_name else image.name
            all_image_names.add(name)
            if node.select:
                selected_image_names.add(name)
    return SlotImages(all_image_names, selected_image_names)
