import bpy
from .scene_tree_space import scene_tree_space


def nodes_from_context(context):
    # type: (bpy.Optional[bpy.ContextType]) -> bpy.Optional[bpy.types.Nodes]
    if context is None:
        return None
    space = scene_tree_space(context.space_data)
    if space is None:
        return None
    return space.node_tree.nodes
