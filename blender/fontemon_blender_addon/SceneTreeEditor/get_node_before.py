import bpy

def get_node_before(node):
    # type: (bpy.AllNodeTypes) -> bpy.Optional[bpy.AllNodeTypes]
    input = node.inputs[0]
    if len(input.links) <= 0:
        return None
        
    link = input.links[0]
    return link.from_node