
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from .view_nodes import view_nodes
from .nodes_from_context import nodes_from_context
from .is_a_scene_node import is_a_scene_node
from .find_slot_names import find_slot_names


class SearchForSlotByNameOperator(Operator, Plugin):
    '''Search for a scene node with a slot named this'''
    bl_idname = "font.slotnamesearch"
    bl_label = "Search For slot by name"
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = "node_item"
    # see https://docs.blender.org/api/current/bpy.props.html?highlight=enumproperty#bpy.props.EnumProperty
    # There is a known bug with using a callback, Python must keep a reference to the strings returned by the callback or Blender will misbehave or even crash.
    _enum_item_hack = []  # type: list[bpy.EnumPropertyItem]

    # Create an enum list from node items
    def node_enum_items(self, context):
        # type: (bpy.Optional[bpy.ContextType]) -> list[bpy.EnumPropertyItem]
        enum_items = SearchForSlotByNameOperator._enum_item_hack
        enum_items.clear()
        nodes = nodes_from_context(context)
        if nodes is None:
            return []
        all_slot_names = set()  # type: set[str]
        selected_slot_names = set()  # type: set[str]
        for item in nodes:
            node = is_a_scene_node(item)
            if node is None:
                continue
            if node.number_of_slots <= 0:
                continue
            slots = find_slot_names(node.node_scene)
            for names in slots.values():
                for name in names:
                    all_slot_names.add(name)
                    if node.select:
                        selected_slot_names.add(name)
        slot_names = selected_slot_names if len(
            selected_slot_names) > 0 else all_slot_names
        for index, slot_name in enumerate(slot_names):
            enum_items.append((slot_name, slot_name, "", index))
        return enum_items

    node_item: EnumProperty(
        name="Node Type",
        description="Node type",
        items=node_enum_items,
    )

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal['FINISHED', 'CANCELLED']]
        slot_name = self.node_item
        nodes = nodes_from_context(context)
        if nodes is None:
            self.report({'ERROR'}, "Could find any nodes")
            return {'CANCELLED'}
        all_found_nodes = []  # type: list[bpy.AllSceneNodeTypes]
        selected_found_nodes = []  # type: list[bpy.AllSceneNodeTypes]
        for item in nodes:
            node = is_a_scene_node(item)
            if (node is None or
                        node.number_of_slots <= 0
                    ):
                continue
            slots = find_slot_names(node.node_scene)
            found_match = False
            for names in slots.values():
                for name in names:
                    if name != slot_name:
                        continue
                    found_match = True
                    break
                if found_match:
                    break
            if not found_match:
                continue
            all_found_nodes.append(node)
            if node.select:
                selected_found_nodes.append(node)
        found_nodes = selected_found_nodes if len(
            selected_found_nodes) > 0 else all_found_nodes
        if len(found_nodes) <= 0:
            self.report(
                {'ERROR'}, "Could find any nodes with matching sclot name")
            return {'CANCELLED'}
        view_nodes(nodes, found_nodes)
        return {'FINISHED'}

    def invoke(self, context, event):
        # type: (bpy.ContextType, bpy.Any) -> set[bpy.Literal["CANCELLED"]]
        # Delayed execution in the search popup
        context.window_manager.invoke_search_popup(self)
        return {'CANCELLED'}
