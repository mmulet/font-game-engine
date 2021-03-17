import json
from .export_scene_tree_to_info import export_scene_tree_to_info
from ..Plugin import Plugin
from .ExportError import ExportError
import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from .view_nodes import view_nodes
from .scene_tree_space import scene_tree_space


class ExportSceneTreeToInfo(Operator, ExportHelper, Plugin):
    """Export scene tree to info"""
    bl_idname = "export.export_scene_tree_to_info"
    bl_label = "Export Scene Tree to Info"

    filename_ext = ".json"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        space_data = scene_tree_space(context.space_data)
        if space_data is None:
            self.report({'ERROR'}, "Not a scene tree editor")
            return {'FINISHED'}
        nodes = space_data.node_tree.nodes
        try:
            out = export_scene_tree_to_info(nodes)
            with open(self.filepath, 'w') as f:
                _ = f.write(json.dumps(out))
            self.report({'INFO'}, f"Saved {self.filepath}!")
        except ExportError as e:
            self.report({'ERROR'}, e.message)
            view_nodes(nodes, e.nodes)
        return {'FINISHED'}
