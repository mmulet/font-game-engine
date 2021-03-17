import bpy

def is_a_slot_node(node):
    # type: (bpy.AllInputNodeTypes) -> bpy.AllInputSlotNodeTypes | None
    if node.bl_idname == "SlotNode":
        return node
    if node.bl_idname == "SlotObjectNode":
        return node
    return None