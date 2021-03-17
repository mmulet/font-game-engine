import bpy
from .charCodeToAssetName import charCodeToAssetName
from .charToCode import charToCode


def findUsedInfo(game):
    # type: (bpy.SceneTreeOutputType) -> bpy.Tuple[set[str], set[str]]
    assets = set()  # type: set[str]
    allwords = set()  # type: set[str]
    for scene in game['scenes'].values():
        for frame in scene['frames']:
            for assetName in frame['sprites']:
                assets.add(assetName)
            if 'words' in frame:
                for word in frame['words']:
                    allwords.add(word)
                    for character in word:
                        if character == " ":
                            continue
                        assets.add(charCodeToAssetName(charToCode(character)))

    for node in game['nodes'].values():
        for assetName in node['slots']:
            assets.add(assetName)
    return (assets, allwords)
