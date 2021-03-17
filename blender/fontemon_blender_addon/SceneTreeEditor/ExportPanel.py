from ..Plugin import Plugin
import bpy
from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from ..Common import ToolPanel, ViewPanel, ItemsPanel
from .scene_tree_space import scene_tree_space
from .draw_open_test_font_button import draw_open_test_font_button

def draw_search_panel(layout, context):
    # type: (bpy.types.UILayout, bpy.ContextType) -> None
    space_data = scene_tree_space(bpy.context.space_data)
    if space_data is None:
        return
    props = space_data.node_tree

    layout.label(text="CharString Directory")
    _ = layout.prop(props, "use_home_base_images")
    if not props.use_home_base_images:
        _ = layout.prop(props, "charstring_directory")
    layout.label(text="Output File Name")
    _ = layout.prop(props, "output_file")

    layout.label(text="Output options")
    box = layout.box()
    layout.label(text="For web: smaller->Unchecked, type->dlig")
    layout.label(text="For word: smaller->Checked, type->game")
    layout.label(text="See the website for more info")
    _ = box.prop(props, "smaller")
    _ = box.prop(props, "feature_type")
    if props.feature_type == "CUSTOM":
        _ = box.prop(props, "custom_feature_name")
    layout.operator("export.export_scene_tree_to_font")
    draw_open_test_font_button(layout, context)


class ExportPanel(Panel, ToolPanel):
    """Font Export"""
    bl_label = "Font Export"
    bl_idname = "OBJECT_PT_exportpanel_tool"
    bl_space_type = 'NODE_EDITOR'

    @classmethod
    def plug_in(cls):
        register_class(cls)
        ExportPanelView.plug_in()
        ExportPanelItem.plug_in()

    @classmethod
    def plug_out(cls):
        ExportPanelItem.plug_out()
        ExportPanelView.plug_out()
        unregister_class(cls)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_search_panel(self.layout, context)


class ExportPanelView(Panel, Plugin, ViewPanel):
    """Font Export"""
    bl_label = "Font Export"
    bl_idname = "OBJECT_PT_exportpanel_view"
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_search_panel(self.layout, context)


class ExportPanelItem(Panel, Plugin, ItemsPanel):
    """Font Export"""
    bl_label = "Font Export"
    bl_idname = "OBJECT_PT_exportpanel_item"
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_search_panel(self.layout, context)
