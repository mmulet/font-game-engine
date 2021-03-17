
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from .view_nodes import view_nodes
from .AdjustSlotsError import AdjustSlotsError
from .slot_node_from_context import slot_node_from_context
from .get_all_connected_slot_nodes import get_all_connected_slot_nodes
from .adjust_slot_numbers import adjust_slot_numbers


class RemoveSlotNodeOperator(Operator, Plugin):
    """Add a slot, adjusting all slot numbers below, downards"""
    bl_idname = "font.removeslotnode"
    bl_label = "Remove slot"
    bl_options = {'UNDO'}
    node_name: StringProperty(name="Node name")

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.remove_slot(context)

        return {'FINISHED'}

    def remove_slot(self, context):
        # type: (bpy.ContextType) -> None
        maybe_node = slot_node_from_context(self.node_name, context)
        if maybe_node is None:
            return
        node, nodes = maybe_node
        try:
            connected_nodes = get_all_connected_slot_nodes(node)
            for i in node.inputs:
                node.inputs.remove(i)
            adjust_slot_numbers(
                connected_nodes,
                new_slot_number=node.slot_number + 1,
                increase_slot_number=False
            )
            nodes.remove(node)

        except AdjustSlotsError as e:
            self.report({'ERROR'}, e.message)
            view_nodes(nodes, e.nodes)
            return
