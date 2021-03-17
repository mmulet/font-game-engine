import bpy
from .parseGame import parseGame
from .get_nodeId_to_list_of_frame_blank_glyph_ID_map import get_nodeId_to_list_of_frame_blank_glyph_ID_map
from .createFeatureFile import createFeatureFile
from .addCharStringsToTTX import addCharStringsToTTX
from fontemon_blender_addon.fontTools.ttLib import TTFont
from fontemon_blender_addon.fontTools.feaLib import builder
from io import StringIO
from .add_code_relay_logo import add_code_relay_logo

def gameToFont(charstring_directory_path, ttxFilePath, out_path, mutable_game,
               smaller, feature_name):
    # type: (str,str, str, bpy.SceneTreeOutputType, bool, str) -> None
    
    # Don't be a jerk. Leave the logo intact
    # I've made the entire software 
    # free as in freedom, all I ask is that my logo stays in the front, so I 
    # can attract more people to work on open source software to make the 
    # world a better place.
    game = add_code_relay_logo(mutable_game)
    parseGame(out_game=game, smaller=smaller)
    nodeId_to_list_of_frame_blank_glyph_ID, blank_glyph_ranges = get_nodeId_to_list_of_frame_blank_glyph_ID_map(
        game)
    featureFile = createFeatureFile(game,
                                    nodeId_to_list_of_frame_blank_glyph_ID,
                                    blank_glyph_ranges, feature_name)

    xmlOutput = addCharStringsToTTX(charstring_directory_path,
                                    game,
                                    nodeId_to_list_of_frame_blank_glyph_ID,
                                    smaller,
                                    ttxFilePath=ttxFilePath)

    tt = TTFont()
    tt.importXML(StringIO(xmlOutput))
    builder.addOpenTypeFeaturesFromString(tt, featureFile)
    # set the required feature index to the one we will cre
    for scriptRecord in tt['GSUB'].table.ScriptList.ScriptRecord:
        scriptRecord.Script.DefaultLangSys.ReqFeatureIndex = 0

    cff = tt['CFF ']
    cffTable = cff.cff['Fontemon']
    cffTable.Private.defaultWidthX = 0
    cffTable.Private.nominalWidthX = 0
    tt.save(out_path)
