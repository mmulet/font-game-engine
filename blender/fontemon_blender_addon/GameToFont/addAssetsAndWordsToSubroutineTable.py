from .wordToCharStringInfo import wordToCharStringInfo
from .addCharStringToSubroutineTable import addCharStringToSubroutineTable
from functools import reduce
import bpy
from xml.etree import ElementTree
from .findUsedInfo import findUsedInfo
from .assetIdToCharStringPath import assetIdToCharStringPath
from .rawCharStringToPixelCharStringInfo import rawCharStringToPixelCharStringInfo
from json import load
from .CharStringInfo import CharStringInfo
from .findSubroutineNumberAndIndex import findSubroutineNumberAndIndex
from .addRepeatedPixelSubroutines import addRepeatedPixelSubroutines
from .AddSubroutineState import AddSubroutineState
from .addRepeatedSceneFramesAsSubroutines import addRepeatedSceneFramesAsSubroutines, SceneNameToFrameSubroutines
from .SubroutineInfoMap import SubroutineInfoMap
from .code_relay_charstrings import code_relay_charstrings
from .GameToFontError import GameToFontError


def addAssetsAndWordsToSubroutineTable(charstring_directory_path,
                                       out_subroutineTable, game, smaller):
    # type: (str,ElementTree.Element, bpy.SceneTreeOutputType, bool) -> bpy.Tuple[SubroutineInfoMap[str], SubroutineInfoMap[str], SceneNameToFrameSubroutines]
    assets, allWords = findUsedInfo(game)
    assetsWithCharStringInfo = {}  # type: dict[str, CharStringInfo]
    for assetId in assets:
        if assetId.endswith(".coderelay.png"):
            if assetId not in code_relay_charstrings:
                raise GameToFontError(f"Missing Asset {assetId}")
            assetsWithCharStringInfo[
                assetId] = rawCharStringToPixelCharStringInfo(
                    code_relay_charstrings[assetId])
            continue
        with open(assetIdToCharStringPath(charstring_directory_path,
                                          assetId)) as f:
            charStringInfo = load(
                f)  # type: bpy.CharStringWithoutInitialPosition
            assetsWithCharStringInfo[
                assetId] = rawCharStringToPixelCharStringInfo(charStringInfo)
    startSubroutineNumber, startSubroutineIndex = findSubroutineNumberAndIndex(
        out_subroutineTable)
    out1 = addRepeatedPixelSubroutines(
        out_subroutineTable,
        startSubroutineIndex=startSubroutineIndex,
        startSubroutineNumber=startSubroutineNumber,
        smaller=smaller)

    def get_asset(assetId: str):
        return assetsWithCharStringInfo[assetId]

    out2 = reduce(
        addCharStringToSubroutineTable(get_asset, out_subroutineTable), assets,
        AddSubroutineState[str]({},
                                index=out1.index,
                                subroutineNumber=out1.subroutineNumber))
    assetToInfo = out2.subroutineInfoMap

    def get_word(word: str):
        return wordToCharStringInfo(word, assetToInfo)

    out3 = reduce(
        addCharStringToSubroutineTable(get_word,
                                       out_subroutineTable), allWords,
        AddSubroutineState[str]({},
                                index=out2.index,
                                subroutineNumber=out2.subroutineNumber))
    wordToInfo = out3.subroutineInfoMap

    sceneNameToFrameSubroutines = addRepeatedSceneFramesAsSubroutines(
        game,
        assetToInfo,
        wordToInfo,
        out_subroutineTable,
        subroutineIndex=out3.index,
        subroutineNumber=out3.subroutineNumber)
    return (assetToInfo, wordToInfo, sceneNameToFrameSubroutines)
