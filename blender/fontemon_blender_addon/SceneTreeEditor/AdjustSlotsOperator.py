
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from .view_nodes import view_nodes
from .AdjustSlotsError import AdjustSlotsError
from .generate_object_slot_info import generate_object_slot_info
from .scene_tree_space import scene_tree_space

class AdjustSlotsOperator(Operator, Plugin):
    """Fix slot, make them match a node graph"""
    bl_idname = "font.adjustslots"
    bl_label = "Fix slots"

    node_name: StringProperty(name="Node name")

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.fix_slots(context)

        return {'FINISHED'}

    def fix_slots(self, context):
        # type: (bpy.ContextType) -> None
        if self.node_name is None:
            return
        space = scene_tree_space(context.space_data)
        if space is None:
            return
        nodes = space.node_tree.nodes
        try:
            node = nodes[self.node_name]
            if node.bl_idname != "SlotSceneNode":
                return
            for info in generate_object_slot_info(node):
                info.apply()
            self.report({'INFO'}, "Fixed")
        except AdjustSlotsError as e:
            self.report({'ERROR'}, e.message)
            view_nodes(nodes, e.nodes)
            return
