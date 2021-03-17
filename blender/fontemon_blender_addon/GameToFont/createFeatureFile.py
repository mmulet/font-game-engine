import bpy
from .computeNodeGroupLevels import computeNodeGroupLevels
from .createFeatureChainString import createFeatureChainString
from .constants import firstNodeId

def createFeatureFile(game, nodeId_to_list_of_frame_blank_glyph_ID, blank_glyph_ranges, feature_name):
  # type: (bpy.SceneTreeOutputType, bpy.NodeId_to_list_of_frame_blank_glyph_ID, list[str], str) -> str
  levelToNodeGroups = computeNodeGroupLevels(game['nodes'])
  featureChain = createFeatureChainString(game, nodeId_to_list_of_frame_blank_glyph_ID, levelToNodeGroups)
  return f"""@input = [A a b c d];
  @all = [@input {" ".join(blank_glyph_ranges)} ];
  feature {feature_name} {{
    lookup findSceneChain {{
      ignore substitute @all @input';
      substitute @input' by {nodeId_to_list_of_frame_blank_glyph_ID[firstNodeId][0]};
    }} findSceneChain;
    {featureChain}

  }} {feature_name};

  """
