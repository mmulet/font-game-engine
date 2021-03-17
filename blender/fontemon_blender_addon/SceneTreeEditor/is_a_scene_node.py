import bpy

def is_a_scene_node(node):
    # type: (bpy.AllNodeTypes) -> bpy.AllSceneNodeTypes | None
    if node.bl_idname == "FirstSceneNode":
        return node
    if node.bl_idname == "SceneNode":
        return node
    if node.bl_idname == "EndSceneNode":
        return node
    return None