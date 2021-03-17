
from .get_slot_image import get_slot_image, set_slot_image
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, StringProperty
from .view_nodes import view_nodes
from .nodes_from_context import nodes_from_context
from .is_a_scene_node import is_a_scene_node


class ReplaceSlotImagesOperator(Operator, Plugin):
    '''Replace an image'''
    bl_idname = "font.replaceslotimage"
    bl_label = "Replace slot image"
    bl_options = {'REGISTER', 'UNDO'}
    # see https://docs.blender.org/api/current/bpy.props.html?highlight=enumproperty#bpy.props.EnumProperty
    # There is a known bug with using a callback, Python must keep a reference to the strings returned by the callback or Blender will misbehave or even crash.
    _enum_item_hack = []  # type: list[bpy.EnumPropertyItem]

    only_selected_nodes: BoolProperty(name="Only Selected nodes",
                                      description="Replace only in the nodes that have been selected.",
                                      default=True
                                      )

    replace_image: StringProperty(name="Replace")
    find_image: StringProperty(name="Find")

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal['FINISHED', 'CANCELLED']]
        if self.replace_image == "" or self.find_image == "":
            self.report({'ERROR'}, "No images to find or replace!")
            return {'CANCELLED'}

        nodes = nodes_from_context(context)
        if nodes is None:
            self.report({'ERROR'}, "Could find any nodes")
            return {'CANCELLED'}
        found_nodes = []  # type: list[bpy.AllSceneNodeTypes]
        for item in nodes:
            if self.only_selected_nodes and not item.select:
                continue
            node = is_a_scene_node(item)
            if (node is None or
                node.number_of_slots <= 0
                ):
                continue
            found_match = False
            for i in range(node.number_of_slots):
                slot_number = i + 1
                image = get_slot_image(node, slot_number)
                if image is None:
                    continue
                if self.find_image != image.name:
                    continue
                set_slot_image(node, slot_number,
                               bpy.data.images[self.replace_image])
                found_match = True
                break
            if not found_match:
                continue
            found_nodes.append(node)
        if len(found_nodes) <= 0:
            self.report(
                {'ERROR'}, "Could find any nodes with matching image name")
            return {'CANCELLED'}
        view_nodes(nodes, found_nodes)
        return {'FINISHED'}
