
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from .view_nodes import view_nodes
from .AdjustSlotsError import AdjustSlotsError
from .slot_node_from_context import slot_node_from_context
from .get_all_connected_slot_nodes import get_all_connected_slot_nodes
from .add_new_slot_node_and_adjust_slots import add_new_slot_node_and_adjust_slots


class AddSlotAboveOperator(Operator, Plugin):
    """Add a slot above, moving all number below upwards"""
    bl_idname = "font.addslotabove"
    bl_label = "Add Slot Above"
    bl_options = {'UNDO'}
    node_name: StringProperty(name="Node name")

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.add_slot_above(context)

        return {'FINISHED'}

    def add_slot_above(self, context):
        # type: (bpy.ContextType) -> None
        maybe_node = slot_node_from_context(self.node_name, context)
        if maybe_node is None:
            return
        node, nodes = maybe_node
        try:
            connected_nodes = get_all_connected_slot_nodes(node)
            add_new_slot_node_and_adjust_slots(
                nodes=nodes,
                connected_nodes=connected_nodes,
                new_slot_number=node.slot_number,
                position=node.location
            )

        except AdjustSlotsError as e:
            self.report({'ERROR'}, e.message)
            view_nodes(nodes, e.nodes)
            return
