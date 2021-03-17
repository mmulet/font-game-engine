

from ..Plugin import Plugin
import bpy
from bpy.types import Panel
from ..Common import (ObjectWindowPanel, ItemsPanel,
                      ObjectDataPanel, ToolPanel, ViewPanel, FontPanel)
from bpy.utils import register_class, unregister_class


def draw_empty_image_without_data_properties(self, context):
    # type: (bpy.types.Panel, bpy.ContextType) -> None
    layout = self.layout
    o = context.object
    layout.template_ID(o, "data", open="image.open",
                       unlink="object.unlink_data")


class IsEmptyImageWithoutDataObject:
    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        o = context.object
        if o is None:
            return False
        if o.type != "EMPTY":
            return False
        if o.empty_display_type != "IMAGE":
            return False
        if o.data is not None:
            return False
        return True


class EmptyImageWithoutDataPropertiesPanel(Panel, Plugin, IsEmptyImageWithoutDataObject, ObjectWindowPanel):
    """The panel to configure an image"""
    bl_label = "New Image Properties"
    bl_idname = "OBJECT_PT_empty_image_without_data_properties_panel"

    @classmethod
    def plug_in(cls):
        register_class(cls)
        EmptyImageWithoutDataPropertiesItemsPanel.plug_in()
        EmptyImageWithoutDataPropertiesFontPanel.plug_in()
        EmptyImageWithoutDataPropertiesToolsPanel.plug_in()
        EmptyImageWithoutDataPropertiesViewPanel.plug_in()
        EmptyImageWithoutDataPropertiesDataPanel.plug_in()

    @classmethod
    def plug_out(cls):
        EmptyImageWithoutDataPropertiesDataPanel.plug_out()
        EmptyImageWithoutDataPropertiesViewPanel.plug_out()
        EmptyImageWithoutDataPropertiesToolsPanel.plug_out()
        EmptyImageWithoutDataPropertiesFontPanel.plug_out()
        EmptyImageWithoutDataPropertiesItemsPanel.plug_out()
        unregister_class(cls)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_empty_image_without_data_properties(self, context)


class EmptyImageWithoutDataPropertiesItemsPanel(Panel, Plugin, IsEmptyImageWithoutDataObject, ItemsPanel):
    """The panel to configure an image"""
    bl_label = "New Image Properties"
    bl_idname = "OBJECT_PT_empty_image_without_data_properties_items_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_empty_image_without_data_properties(self, context)

class EmptyImageWithoutDataPropertiesFontPanel(Panel, Plugin, IsEmptyImageWithoutDataObject, FontPanel):
    """The panel to configure an image"""
    bl_label = "Image Properties"
    bl_idname = "OBJECT_PT_empty_image_without_data_properties_font_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_empty_image_without_data_properties(self, context)


class EmptyImageWithoutDataPropertiesToolsPanel(Panel, Plugin, IsEmptyImageWithoutDataObject, ToolPanel):
    """The panel to configure an image"""
    bl_label = "Image Properties"
    bl_idname = "OBJECT_PT_empty_image_without_data_properties_tools_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_empty_image_without_data_properties(self, context)


class EmptyImageWithoutDataPropertiesViewPanel(Panel, Plugin, IsEmptyImageWithoutDataObject, ViewPanel):
    """The panel to configure an image"""
    bl_label = "Image Properties"
    bl_idname = "OBJECT_PT_empty_image_without_data_properties_view_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_empty_image_without_data_properties(self, context)

class EmptyImageWithoutDataPropertiesDataPanel(Panel, Plugin, IsEmptyImageWithoutDataObject, ObjectDataPanel):
    """The panel to configure an image"""
    bl_label = "New Image Properties"
    bl_idname = "OBJECT_PT_empty_image_without_data_properties_data_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_empty_image_without_data_properties(self, context)
