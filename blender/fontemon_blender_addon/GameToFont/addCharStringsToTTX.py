import bpy
from .addAssetsAndWordsToSubroutineTable import addAssetsAndWordsToSubroutineTable
from .sceneToFrameCharStrings import sceneToFrameCharStrings
from xml.etree.ElementTree import parse, Element, tostring, SubElement
from .adjustSubroutineBias import adjustSubroutineBias
from .GameToFontError import GameToFontError

def addCharStringsToTTX(charstring_directory_path, game,
                        nodeId_to_list_of_frame_blank_glyph_ID, smaller,
                        ttxFilePath):
    # type: (str,bpy.SceneTreeOutputType, bpy.NodeId_to_list_of_frame_blank_glyph_ID, bool, str) -> str
    tree = parse(ttxFilePath)
    root = tree.getroot()
    lastChildId = int(root.findall("./GlyphOrder/*")[-1].attrib['id'])

    subroutineTable = root.find('./CFF/CFFFont/Private/Subrs')
    if subroutineTable is None:
        raise GameToFontError("Could not get subroutine table")

    assetToInfo, wordToInfo, sceneNameToFrameSubroutines = addAssetsAndWordsToSubroutineTable(
        charstring_directory_path, subroutineTable, game, smaller)
    mapper = sceneToFrameCharStrings(
        nodeId_to_list_of_frame_blank_glyph_ID,
        assetToInfo=assetToInfo,
        wordToInfo=wordToInfo,
        game=game,
        sceneNameToFrameSubroutines=sceneNameToFrameSubroutines)
    allGlyphs = [k for n in game['nodes'].items() for k in mapper(n)]
    htmx = root.find('./hmtx')
    glyphOrder = root.find('./GlyphOrder')
    charStringsTable = root.find('./CFF/CFFFont/CharStrings')
    cmapTable = root.find('cmap')

    if (htmx is None or glyphOrder is None or charStringsTable is None
            or cmapTable is None):
        raise GameToFontError(
            f"`Couldn't find htmx: {htmx}, glyphOrder: {glyphOrder}, CharStrings:${charStringsTable} table, cmap Table: {cmapTable}"
        )
    for elem in cmapTable:
        if elem.tag == "tableVersion":
            continue
        for child in elem:
            if 'name' not in child.attrib:
                continue
            name = child.attrib['name']
            if name == 'a':
                continue
            elif name == 'b':
                continue
            elif name == 'c':
                continue
            elif name == 'd':
                continue
            child.attrib['name'] = "A"

    for child in htmx:
        if 'name' not in child.attrib:
            continue
        if child.attrib['name'] != 'A':
            continue
        child.attrib['width'] = '0'
    for index, info in enumerate(allGlyphs):
        htmx.append(
            Element("mtx", {
                'name': info.glyphId,
                'width': "0",
                "lsb": "0"
            }))
        glyphOrder.append(
            Element("GlyphID", {
                'id': str(lastChildId + 1 + index),
                'name': info.glyphId
            }))
        SubElement(charStringsTable, "CharString", {
            'name': info.glyphId
        }).text = info.fileContent
    if smaller:
        fontMatrix = root.find("./CFF/CFFFont/FontMatrix")
        if fontMatrix is None:
            raise GameToFontError("Could not find the font matrix")
        fontMatrix.attrib['value'] = "0.00045 0 0 0.00045 0 0"

    xmlOutput = adjustSubroutineBias(tostring(root, encoding="unicode"),
                                     len(subroutineTable))

    return xmlOutput