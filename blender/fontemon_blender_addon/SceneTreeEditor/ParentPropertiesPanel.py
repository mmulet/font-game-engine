from ..Plugin import Plugin
import bpy
from bpy.types import Panel
from ..Common import (ObjectWindowPanel, ItemsPanel,
                      ObjectDataPanel, ToolPanel, ViewPanel, FontPanel, text_object)
from bpy.utils import register_class, unregister_class


def draw_parent_properties_panel(self, context):
    # type: (bpy.types.Panel, bpy.ContextType) -> None
    layout = self.layout
    o = context.active_object
    if o is None:
        return
    if o.children is None:
        return
    if text_object(o) is not None:
        return
    select_props = layout.operator("object.select_hierarchy", text="Select Children")
    select_props.direction = "CHILD"
    select_props.extend = False
    select_props = layout.operator("object.select_hierarchy", text="Select Animation")
    select_props.direction = "CHILD"
    select_props.extend = False
    layout.operator("font.clear_children")


class IsImageParent:
    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        if context.active_object is None:
            return False
        if context.active_object.children is None:
            return False
        # Don't dhow parent panel for text objects
        if text_object(context.active_object) is not None:
            return False
        return len(context.active_object.children) > 0


class ParentPropertiesPanel(Panel, IsImageParent, ObjectWindowPanel):
    """The panel to configure an image"""
    bl_label = "Parent Properties"
    bl_idname = "OBJECT_PT_parent_properties_panel"

    @classmethod
    def plug_in(cls):
        register_class(cls)
        ParentPropertiesItemsPanel.plug_in()
        ParentPropertiesFontPanel.plug_in()
        ParentPropertiesToolsPanel.plug_in()
        ParentPropertiesViewPanel.plug_in()
        ParentPropertiesDataPanel.plug_in()

    @classmethod
    def plug_out(cls):
        ParentPropertiesDataPanel.plug_out()
        ParentPropertiesViewPanel.plug_out()
        ParentPropertiesToolsPanel.plug_out()
        ParentPropertiesFontPanel.plug_out()
        ParentPropertiesItemsPanel.plug_out()
        unregister_class(cls)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_parent_properties_panel(self, context)


class ParentPropertiesItemsPanel(Panel, Plugin, IsImageParent, ItemsPanel):
    """The panel to configure an image"""
    bl_label = "Parent Properties"
    bl_idname = "OBJECT_PT_parent_properties_items_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_parent_properties_panel(self, context)


class ParentPropertiesFontPanel(Panel, Plugin, IsImageParent, FontPanel):
    """The panel to configure an image"""
    bl_label = "Parent Properties"
    bl_idname = "OBJECT_PT_parent_properties_font_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_parent_properties_panel(self, context)


class ParentPropertiesToolsPanel(Panel, Plugin, IsImageParent, ToolPanel):
    """The panel to configure an image"""
    bl_label = "Parent Properties"
    bl_idname = "OBJECT_PT_parent_properties_tools_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_parent_properties_panel(self, context)


class ParentPropertiesViewPanel(Panel, Plugin, IsImageParent, ViewPanel):
    """The panel to configure an image"""
    bl_label = "Parent Properties"
    bl_idname = "OBJECT_PT_parent_properties_view_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_parent_properties_panel(self, context)


class ParentPropertiesDataPanel(Panel, Plugin, IsImageParent, ObjectDataPanel):
    """The panel to configure an image"""
    bl_label = "Parent Properties"
    bl_idname = "OBJECT_PT_parent_properties_data_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_parent_properties_panel(self, context)
