from ..GameToFont.GameToFontError import GameToFontError
from .export_scene_tree_to_info import export_scene_tree_to_info
from ..Plugin import Plugin
from .ExportError import ExportError
import bpy
from bpy.types import Operator
from .view_nodes import view_nodes
from .scene_tree_space import scene_tree_space
from .export_scene_tree_to_info import export_scene_tree_to_info
from ..GameToFont import gameToFont
from os.path import dirname, join
from bpy.path import abspath, ensure_ext


def get_feature_name(scene_tree):
    # type: (bpy.SceneTreeNodeTree) -> str
    if scene_tree.feature_type == "DLIG":
        return "dlig"
    if scene_tree.feature_type == "GAME":
        return "game"
    return scene_tree.custom_feature_name


class ExportSceneTreeToFont(Operator, Plugin):
    """Export scene tree to info"""
    bl_idname = "export.export_scene_tree_to_font"
    bl_label = "Export Scene Tree to font"

    filename_ext = ".otf"

    def get_charstring_directory(self, scene_tree):
        # type: (bpy.SceneTreeNodeTree) -> str
        if not scene_tree.use_home_base_images:
            return abspath(scene_tree.charstring_directory)
        return join(
            abspath(bpy.context.window_manager.converter_props.images_folder),
            "charStrings")

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]

        space_data = scene_tree_space(context.space_data)
        if space_data is None:
            self.report({'ERROR'}, "Not a scene tree editor")
            return {'FINISHED'}
        scene_tree = space_data.node_tree
        nodes = scene_tree.nodes
        charstring_directory = self.get_charstring_directory(scene_tree)
        output_file = ensure_ext(abspath(scene_tree.output_file), ".otf")

        try:
            file_path = abspath(__file__)
            SceneTreeEditorDir = dirname(file_path)
            addon_dir = dirname(SceneTreeEditorDir)
            ttxPath = join(addon_dir, "assets", "SourceFont.ttx")
            print(f"ttxPath is {ttxPath}")
            out = export_scene_tree_to_info(nodes)
            self.report({'INFO'}, f"Exported SceneTree. Creating font now!")
            gameToFont(charstring_directory_path=charstring_directory,
                       ttxFilePath=ttxPath,
                       out_path=output_file,
                       mutable_game=out,
                       smaller=scene_tree.smaller,
                       feature_name=get_feature_name(scene_tree))
            bpy.context.window_manager.converter_props.most_recent_otf_export_path = scene_tree.output_file
            bpy.context.window_manager.converter_props.export_number += 1
            self.report({'INFO'}, f"Saved {output_file}!")
        except ExportError as e:
            self.report({'ERROR'}, e.message)
            view_nodes(nodes, e.nodes)
        except GameToFontError as e:
            self.report({'ERROR'}, e.message)
        return {'FINISHED'}
