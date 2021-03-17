from bpy.path import basename
from .node_to_scene_path_id import node_to_scene_path_id
from .get_scene_frames import SceneFramesError, get_scene_frames
from .get_node_scene import get_node_scene
from .ExportError import ExportError
from .is_an_end_node import cast_to_not_an_end_node
from .get_slot_image import get_slot_image
import bpy
from re import compile
from typing import cast, Any
from ..GameToFont import defaultKey

def get_node_slots(inNode, num_slots):
    # type: (bpy.AllSceneNodeTypes, int) -> list[str]
    slots = []  # type: list[str]
    for i in range(num_slots):
        slot_num = i + 1
        image = get_slot_image(inNode, slot_num)
        if image is None:
            raise SceneFramesError(f"There is no image for slot #{slot_num}")
        image_name = basename(image.filepath)
        if image_name == "":
            raise SceneFramesError(f"There is no image for slot #{slot_num}")
        slots.append(image_name)
    return slots


has_whitespace = compile("\\s")


def create_scene_info(inNode, out_scene_infos):
    # type: (bpy.AllSceneNodeTypes, bpy.SceneInfosType) -> bpy.SceneNodeInfoType
    """Grab the scene info (frames and conditions) from a node,
        as well as compute each sprite position in a scene"""
    scene = get_node_scene(inNode)
    if has_whitespace.search(scene.name) is not None:
        raise ExportError(
            f"Scene name has whitespace in it. Not allowed! {scene.name}",
            [inNode])
    try:
        if scene.name not in out_scene_infos:
            out_scene_infos[scene.name] = get_scene_frames(scene)
        scene_info = out_scene_infos[scene.name]
        num_slots = scene_info['slots']
        if inNode.number_of_slots < num_slots:
            raise ExportError(
                f"Not enough slots in a scene Node, Need {num_slots} slots, but only have f{inNode.number_of_slots} ",
                [inNode])
        slots = get_node_slots(inNode, num_slots)

    except SceneFramesError as e:
        raise ExportError(e.message, [inNode])

    maybeOutputSceneNode = cast_to_not_an_end_node(inNode)

    if maybeOutputSceneNode is None:
        # is an end node
        return {'conditions': [], 'scene_name': scene.name, 'slots': slots}
    node = maybeOutputSceneNode  # type: bpy.AllOutputSceneNodeTypes
    condition_keys = {}  # type: "dict[str, bpy.LinkedNodeTypes]"
    conditions = []  # type: "list[bpy.ConditionType]"

    def create_condition(key, scene_node) -> None:
        # type: (str, bpy.LinkedNodeTypes) -> bpy.Literal[True]
        if key in condition_keys:
            raise ExportError("Multiple conditions satisfied!",
                              [scene_node, node, condition_keys[key]])
        node_id = 'lost_scene' if scene_node.bl_idname == "GotoLostNode" else node_to_scene_path_id(
            scene_node)
        conditions.append({'key': key, 'node_id': node_id})
        condition_keys[key] = scene_node

    if len(node.outputs[0].links) <= 0:
        raise ExportError("Node is not connected to anything!", [node])

    for l in node.outputs[0].links:
        destination_node = l.to_node
        if (destination_node.bl_idname == "SceneNode"
                or destination_node.bl_idname == "EndSceneNode"
                or destination_node.bl_idname == "GotoLostNode"):
            create_condition(defaultKey, destination_node)
        elif destination_node.bl_idname == "ConditionNode":
            key = destination_node.condition_key
            if not key or key == "":
                raise ExportError("Missing condition!", [destination_node])
            links = destination_node.outputs[0].links
            if len(links) > 1:
                raise ExportError("Only one output is allowed",
                                  [l.to_node for l in links])
            if len(links) <= 0:
                raise ExportError("Condition not connected to anything!",
                                  [destination_node])
            to_node = links[0].to_node
            if (to_node.bl_idname != "SceneNode"
                    and to_node.bl_idname != "EndSceneNode"
                    and to_node.bl_idname != "GotoLostNode"):
                e = "Condition Node is not connected to a scene node"
                raise ExportError(e, [destination_node, to_node])
            create_condition(key, to_node)
        else:
            raise ExportError("Unrecognized node type",
                              [cast(Any, destination_node)])
    if not defaultKey in condition_keys:
        conditions.append({"key": defaultKey, 'node_id': 'lost_scene'})
    return {'conditions': conditions, 'scene_name': scene.name, 'slots': slots}
