
from ..Plugin import Plugin
from .ExportError import ExportError
import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from .view_nodes import view_nodes
from .export_scene_tree_to_script import export_scene_tree_to_script
from .scene_tree_space import scene_tree_space


class ExportScript(Operator,
                   ExportHelper,
                   Plugin):
    """Export game script"""
    bl_idname = "export.export_script"
    bl_label = "Export Script"

    filename_ext = ".json"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        space_data = scene_tree_space(context.space_data)
        if space_data is None:
            self.report({'ERROR'}, "Not a scene tree editor")
            return {'FINISHED'}
        nodes = space_data.node_tree.nodes
        try:
            export_scene_tree_to_script(
                nodes, self.filepath)
            self.report({'INFO'}, f"Saved {self.filepath}!")
        except ExportError as e:
            self.report({'ERROR'}, e.message)
            view_nodes(nodes, e.nodes)
        return {'FINISHED'}
