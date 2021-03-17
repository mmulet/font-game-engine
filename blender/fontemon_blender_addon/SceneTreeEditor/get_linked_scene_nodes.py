import bpy
from .is_an_end_node import cast_to_not_an_end_node
from .is_a_linked_node import is_a_linked_node
from .ExportError import ExportError
from typing import cast, Any

def get_linked_scene_nodes(node):
    # type: (bpy.AllSceneNodeTypes) -> list[bpy.AllSceneNodeTypes]
    maybeNotAndEndNode = cast_to_not_an_end_node(node)
    if not maybeNotAndEndNode:
        return []
    outputNode = maybeNotAndEndNode  # type: bpy.OutputSceneNodeType

    # We know everything is valid because we already
    #  checked everything in create_scene_info

    def linked_node(node):
        # type: (bpy.AllNodeTypes) -> bpy.LinkedNodeTypes
        if node.bl_idname == "ConditionNode":
            newNode = node.outputs[0].links[0].to_node
            if newNode.bl_idname == "ConditionNode":
                # This should never happen because we already checked this
                # in create scene info
                raise ExportError(
                    "Condition node connected to condition node!", [cast(Any, outputNode), node])
            linked_node = is_a_linked_node(newNode)
            if linked_node is None:
                raise ExportError(
                    "Condition node connected to an invalid node", [cast(Any, outputNode), node])
            return linked_node
        if (node.bl_idname == "SceneNode" or
            node.bl_idname == "EndSceneNode" or
                node.bl_idname == "GotoLostNode"):
            return node
        # This should never happen
        raise ExportError("Linked to an first sene node", [cast(Any, outputNode), node])

    next_scene_nodes = []  # type: list[bpy.AllSceneNodeTypes]
    for l in outputNode.outputs[0].links:
        n = linked_node(l.to_node)
        # Don't need to export the lost node scene.
        # this is done automatically
        if n.bl_idname == "GotoLostNode":
            continue
        next_scene_nodes.append(n)
    return next_scene_nodes

