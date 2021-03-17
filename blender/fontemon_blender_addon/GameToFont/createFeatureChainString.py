import bpy
from collections import OrderedDict
from .GameToFontError import GameToFontError
from .defaultKey import defaultKey

def substituteFeaCommand(glyphId, nextGlyphId, condition="@input"):
    # type: (str, str, str) -> str
    return f"substitute {glyphId} {condition} by {nextGlyphId};\n"


def addSubstitutionGlyph(out_frameLookups, nodeGroupFrameNumber, glyphId,
                         nextGlyphId):
    # type: (bpy.FrameLookups, int, str, str) -> int
    frame_lookup = out_frameLookups[
        nodeGroupFrameNumber] if nodeGroupFrameNumber in out_frameLookups else ""
    out_frameLookups[
        nodeGroupFrameNumber] = frame_lookup + substituteFeaCommand(
            glyphId=glyphId, nextGlyphId=nextGlyphId)
    return nodeGroupFrameNumber + 1



def createLevelLookups(game, nodeId_to_list_of_frame_blank_glyph_ID, nodeGroups):
  # type: (bpy.SceneTreeOutputType, bpy.NodeId_to_list_of_frame_blank_glyph_ID, list[list[str]]) -> bpy.Tuple[bpy.FrameLookups, str]
  # all nodes on the same level are parallel to each other
  # so they can share a lookup
  frameLookups = {}  # type: bpy.FrameLookups
  conditionLookup = ""
  for nodeGroup in nodeGroups:
      nodeGroupFrameNumber = 0
      nodeGroupLength = len(nodeGroup)
      for nodeGroupIndex, nodeId in enumerate(nodeGroup):
          node = game["nodes"][nodeId]
          lastFrameNumber = len(game["scenes"][node['scene_name']]['frames']) - 1
          frameToGlyphIds = nodeId_to_list_of_frame_blank_glyph_ID[
              nodeId]
          # all but the last frame
          for frameNumber in range(lastFrameNumber):
              nodeGroupFrameNumber = addSubstitutionGlyph(
                  out_frameLookups=frameLookups,
                  nodeGroupFrameNumber=nodeGroupFrameNumber,
                  glyphId=frameToGlyphIds[frameNumber],
                  nextGlyphId=frameToGlyphIds[frameNumber + 1])
          # still in the node Group
          if nodeGroupIndex < nodeGroupLength - 1:
              nodeGroupFrameNumber = addSubstitutionGlyph(
                  out_frameLookups=frameLookups,
                  nodeGroupFrameNumber=nodeGroupFrameNumber,
                  glyphId=frameToGlyphIds[lastFrameNumber],
                  nextGlyphId=nodeId_to_list_of_frame_blank_glyph_ID[
                      nodeGroup[nodeGroupIndex + 1]][0])
              continue
          # STill in the node group or  an end node no more conditions
          condition_length = len(node['conditions'])
          if condition_length <= 0:
              continue
          if condition_length == 1:
              condition = node['conditions'][0]
              if condition['key'] != defaultKey:
                  raise GameToFontError(
                      f"Only one condition key, and it is not default it is ${condition['key']}"
                  )
              nodeGroupFrameNumber = addSubstitutionGlyph(
                  out_frameLookups=frameLookups,
                  nodeGroupFrameNumber=nodeGroupFrameNumber,
                  glyphId=frameToGlyphIds[lastFrameNumber],
                  nextGlyphId=nodeId_to_list_of_frame_blank_glyph_ID[
                      condition['node_id']][0])
              continue
          glyphId = frameToGlyphIds[lastFrameNumber]
          defaultCondition = next(
              (o for o in node['conditions'] if o['key'] == defaultKey),
              None)
          if defaultCondition is None:
              raise GameToFontError(f"No default condition for node {nodeId}")
          conditionLookup += substituteFeaCommand(
              glyphId=glyphId,
              nextGlyphId=nodeId_to_list_of_frame_blank_glyph_ID[
                  defaultCondition['node_id']][0]) + "\n"
          conditionLookup += "\n".join([
              substituteFeaCommand(
                  glyphId=glyphId,
                  nextGlyphId=nodeId_to_list_of_frame_blank_glyph_ID[
                      c['node_id']][0],
                  condition=c['key'])
              for c in node['conditions'] if c['key'] != defaultKey
          ]) + "\n"
  
  return (OrderedDict(sorted(frameLookups.items())), conditionLookup)


def createFeatureChainString(game, nodeId_to_list_of_frame_blank_glyph_ID,
                             levelToNodeGroups):
    # type: (bpy.SceneTreeOutputType, bpy.NodeId_to_list_of_frame_blank_glyph_ID, OrderedDict[int, list[list[str]]]) -> str
    out = ""
    for level, nodeGroups in levelToNodeGroups.items():
        frameLookups, conditionLookup = createLevelLookups(game, nodeId_to_list_of_frame_blank_glyph_ID, nodeGroups)
        for frameNumber,frameLookup in frameLookups.items():
          lookupName = f"level{level}Frame{frameNumber}"
          out += f"""lookup {lookupName}{{
            {frameLookup}
          }} {lookupName};\n"""
        if conditionLookup == "":
          continue
        lookupName = f"level{level}Conditions"
        out += f"""lookup {lookupName}{{
          {conditionLookup}
        }} {lookupName};\n"""
    return out
