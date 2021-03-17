from ..Plugin import Plugin
from bpy.types import NodeTree

from bpy.props import StringProperty, EnumProperty, BoolProperty


class SceneTree(NodeTree, Plugin):
    '''A show the flow of the scenes from the tree'''
    bl_idname = 'SceneTreeType'
    bl_label = "Font Scene Tree"
    bl_icon = 'NODETREE'

    use_home_base_images: BoolProperty(name="Use Home Base image folder",
                                       description="""
        Use the images folder that you selected in the Home Base. 
        The charstring folder will be a subfolder of images folder.
         Example: //../../images/charStrings""",
                                       default=True)

    charstring_directory: StringProperty(
        name="Charstring Folder",
        description="The folder where you keep all of the .charstring files",
        default="//../../images/charStrings/",
        subtype="DIR_PATH",
    )

    output_file: StringProperty(
        name="Output file (.otf)",
        description="The name of the file output .otf file, where to save it",
        default="//font_game.otf",
        subtype="FILE_PATH")

    smaller: BoolProperty(
        name="Smaller",
        default=False,
        description="Adjust the size of the game to fit into different places")

    feature_types = [
        ("DLIG", "dlig", "Put the game in the discretionary ligatures feature",
         1),
        ("GAME", "game", "Put the game in the game feature", 2),
        ("CUSTOM", "custom", "Put the game in a feature that you choose", 3),
    ]

    feature_type: EnumProperty(
        items=feature_types,
        name="Feature Name",
    )
    custom_feature_name: StringProperty(
        name="Custom Feature",
        description=
        "The name of you custom feature, usually the name should be 4 characters long"
    )
