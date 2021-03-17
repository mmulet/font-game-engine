
from .get_slot_image import get_slot_image
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from .view_nodes import view_nodes
from .nodes_from_context import nodes_from_context
from .is_a_scene_node import is_a_scene_node
from bpy.path import basename
from .find_all_node_slot_images import find_all_node_slot_images


class SearchForImageInSlotOperator(Operator, Plugin):
    '''Search for a scene node with using an image'''
    bl_idname = "font.slotimagesearch"
    bl_label = "Search For Image in a slot"
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = "node_item"
    # see https://docs.blender.org/api/current/bpy.props.html?highlight=enumproperty#bpy.props.EnumProperty
    # There is a known bug with using a callback, Python must keep a reference to the strings returned by the callback or Blender will misbehave or even crash.
    _enum_item_hack = []  # type: list[bpy.EnumPropertyItem]

    # Create an enum list from node items
    def node_enum_items(self, context):
        # type: (bpy.Optional[bpy.ContextType]) -> list[bpy.EnumPropertyItem]
        enum_items = SearchForImageInSlotOperator._enum_item_hack
        enum_items.clear()
        names = find_all_node_slot_images(context)
        image_names = names.selected if len(names.selected) > 0 else names.all
        for index, image_name in enumerate(image_names):
            enum_items.append((image_name, image_name, "", index))
        return enum_items

    node_item: EnumProperty(
        name="Node Type",
        description="Node type",
        items=node_enum_items,
    )

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal['FINISHED', 'CANCELLED']]
        image_name = self.node_item
        nodes = nodes_from_context(context)
        if nodes is None:
            self.report({'ERROR'}, "Could find any nodes")
            return {'CANCELLED'}
        all_found_nodes = []  # type: list[bpy.AllSceneNodeTypes]
        found_selected_nodes = []  # type: list[bpy.AllSceneNodeTypes]
        for item in nodes:
            node = is_a_scene_node(item)
            if (node is None or
                node.number_of_slots <= 0
                ):
                continue
            found_match = False
            for i in range(node.number_of_slots):
                image = get_slot_image(node, i + 1)
                if image is None:
                    continue
                name = basename(image.filepath)
                if image_name != name:
                    continue
                found_match = True
                break
            if not found_match:
                continue
            all_found_nodes.append(node)
            if node.select:
                found_selected_nodes.append(node)
        found_nodes = found_selected_nodes if len(
            found_selected_nodes) > 0 else all_found_nodes
        if len(found_nodes) <= 0:
            self.report(
                {'ERROR'}, "Could find any nodes with matching image name")
            return {'CANCELLED'}
        view_nodes(nodes, found_nodes)
        return {'FINISHED'}

    def invoke(self, context, event):
        # type: (bpy.ContextType, bpy.Any) -> set[bpy.Literal["CANCELLED"]]
        # Delayed execution in the search popup
        context.window_manager.invoke_search_popup(self)
        return {'CANCELLED'}
