from ..Plugin import Plugin
from bpy.props import StringProperty, BoolProperty
import bpy
from bpy.types import Operator
from .scene_tree_space import scene_tree_space


# Base class for node 'Add' operators
# see https://developer.blender.org/diffusion/B/browse/master/release/scripts/startup/bl_operators/node.py$127
class AddNodeAtCenterOperator(Operator, Plugin):
    """Add node at center of tree"""
    bl_idname = "font.add_node_at_center"
    bl_label = "Add Node at center"
    type: StringProperty(
        name="Node Type",
        description="Node type",
    )
    use_transform: BoolProperty(
        name="Use Transform",
        description="Start transform operator after inserting the node",
        default=False,
    )

    # XXX explicit node_type argument is usually not necessary,
    # but required to make search operator work:
    # add_search has to override the 'type' property
    # since it's hardcoded in bpy_operator_wrap.c ...
    def create_node(self, context, node_type=None):
        # type: (bpy.ContextType, bpy.Optional[str]) -> bpy.AllNodeTypes

        maybeSpace = scene_tree_space(context.space_data)  # type: bpy.Any
        space = maybeSpace  # type: bpy.SceneTreeSpaceDataType
        tree = space.node_tree
        # tree = space.edit_tree

        if node_type is None:
            node_type = self.type

        # select only the new node
        for n in tree.nodes:
            n.select = False

        node = tree.nodes.new(type=node_type)

        node.select = True
        tree.nodes
        tree.nodes.active = node
        node.location = tree.view_center
        return node

    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        # space = context.space_data
        # needs active node editor and a tree to add nodes to
        return scene_tree_space(context.space_data) != None
        # return ((space.type == 'NODE_EDITOR') and space.edit_tree
        #         and not space.edit_tree.library)

    # Default execute simply adds a node
    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal['FINISHED', 'CANCELLED']]
        _ = self.create_node(context)
        return {'FINISHED'}

    # Default invoke stores the mouse position to place the node correctly
    # and optionally invokes the transform operator
    def invoke(self, context, event):
        # type: (bpy.ContextType, bpy.Any) -> set[bpy.Literal['FINISHED', 'CANCELLED']]
        # self.store_mouse_cursor(context, event)
        result = self.execute(context)
        if self.use_transform and ('FINISHED' in result):
            # removes the node again if transform is canceled
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

        return result