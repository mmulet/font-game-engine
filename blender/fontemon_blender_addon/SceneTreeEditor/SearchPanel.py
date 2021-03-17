from ..Plugin import Plugin
import bpy
from bpy.types import Image, Panel, PropertyGroup
from bpy.props import BoolProperty, PointerProperty
from bpy.utils import register_class, unregister_class
from .draw_search_operators import draw_search_operators
from ..Common import ToolPanel, ViewPanel, ItemsPanel


class SearchProperties(PropertyGroup):
    """Properties for searching the font scene tree"""
    find_image: PointerProperty(name="Find", type=Image)
    replace_image: PointerProperty(name="Replace", type=Image)
    only_selected_nodes: BoolProperty(
        name="Only Selected nodes",
        description="Replace only in the nodes that have been selected",
        default=True)


def draw_search_panel(layout, context):
    # type: (bpy.types.UILayout, bpy.ContextType) -> None
    draw_search_operators(layout)
    box = layout.box()
    box.label(text="Replace Slot Images")
    props = context.window_manager.search_props
    _ = box.prop(props, "find_image")
    _ = box.prop(props, "replace_image")
    _ = box.prop(props, "only_selected_nodes")
    operator_props = box.operator("font.replaceslotimage")
    operator_props.only_selected_nodes = props.only_selected_nodes
    operator_props.find_image = props.find_image.name if props.find_image is not None else ""
    operator_props.replace_image = props.replace_image.name if props.replace_image is not None else ""


class SearchPanel(Panel, ToolPanel):
    """Font Search"""
    bl_label = "Font Search"
    bl_idname = "OBJECT_PT_searchpanel_tool"
    bl_space_type = 'NODE_EDITOR'

    @classmethod
    def plug_in(cls):
        register_class(SearchProperties),
        bpy.types.WindowManager.search_props = PointerProperty(
            name="Search Properties", type=SearchProperties)
        register_class(cls)
        SearchPanelView.plug_in()
        SearchPanelItem.plug_in()

    @classmethod
    def plug_out(cls):
        SearchPanelItem.plug_out()
        SearchPanelView.plug_out()
        unregister_class(cls)
        del bpy.types.WindowManager.search_props
        unregister_class(SearchProperties)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_search_panel(self.layout, context)


class SearchPanelView(Panel, Plugin, ViewPanel):
    """Font Search"""
    bl_label = "Font Search"
    bl_idname = "OBJECT_PT_searchpanel_view"
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_search_panel(self.layout, context)



class SearchPanelItem(Panel, Plugin, ItemsPanel):
    """Font Search"""
    bl_label = "Font Search"
    bl_idname = "OBJECT_PT_searchpanel_item"
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_search_panel(self.layout, context)
