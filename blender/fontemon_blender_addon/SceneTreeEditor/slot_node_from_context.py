import bpy
from .nodes_from_context import nodes_from_context

def slot_node_from_context(name, context):
    # type: (bpy.Optional[str], bpy.ContextType) -> bpy.Optional[bpy.Tuple[bpy.SlotNodeType, bpy.types.Nodes]]
    if name is None:
        return
    nodes = nodes_from_context(context)
    if nodes is None:
        return
    if name not in nodes:
        return
    node = nodes[name]
    if node.bl_idname != "SlotNode":
        return
    return (node, nodes)
