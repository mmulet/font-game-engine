import bpy
from math import ceil, floor


def get_nodeId_to_list_of_frame_blank_glyph_ID_map(game):
    # type: (bpy.SceneTreeOutputType) -> bpy.Tuple[bpy.NodeId_to_list_of_frame_blank_glyph_ID, list[str]]
    scenes = game['scenes']
    frameCount = 0
    nodeId_to_list_of_frame_blank_glyph_ID = {
    }  # type: bpy.NodeId_to_list_of_frame_blank_glyph_ID
    # each node is a different frame, even if two nodes share
    # the same scene.
    for nodeId, nodeInfo in game['nodes'].items():
        frames = scenes[nodeInfo['scene_name']]['frames']
        number_of_frames_in_node = len(frames)
        nodeId_to_list_of_frame_blank_glyph_ID[nodeId] = [
            f"b{str(frameCount + i).zfill(5)}"
            for i in range(number_of_frames_in_node)
        ]
        frameCount += number_of_frames_in_node
    number_of_frames = float(frameCount - 1)
    number_of_ranges = ceil(number_of_frames / 1000)
    blank_glyph_ranges = [
        f"b{str(i).zfill(2)}000-b{str(i).zfill(2)}999"
        for i in range(number_of_ranges - 1)
    ]
    last_place = str(int(floor(number_of_frames / 1000))).zfill(2)
    blank_glyph_ranges.append(
        f"b{last_place}000" if number_of_frames %
        1000 == 0 else f"b{last_place}000-b{str(int(number_of_frames)).zfill(5)}")
    return (nodeId_to_list_of_frame_blank_glyph_ID, blank_glyph_ranges)
