import bpy

def is_a_linked_node(node):
    # type: (bpy.AllNodeTypes) -> bpy.LinkedNodeTypes | None
    if node.bl_idname == "SceneNode":
        return node
    if node.bl_idname == "EndSceneNode":
        return node
    if node.bl_idname == "GotoLostNode":
        return node
    return None