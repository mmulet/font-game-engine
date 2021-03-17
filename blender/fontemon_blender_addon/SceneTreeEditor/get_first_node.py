import bpy
from .ExportError import ExportError


def get_first_node(nodes):
    # type: (list[bpy.AllNodeTypes]) -> bpy.FirstSceneNodeType
    first_nodes = [n for n in nodes if n.bl_idname == "FirstSceneNode"]
    if len(first_nodes) > 1:
        raise ExportError("More than 1 first scene!", first_nodes)
    if len(first_nodes) <= 0:
        raise ExportError("No first scene node!", [])
    return first_nodes[0]
