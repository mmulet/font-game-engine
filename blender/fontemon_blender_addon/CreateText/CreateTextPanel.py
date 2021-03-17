 
from ..Common import ObjectWindowPanel, ItemsPanel
from ..Plugin import Plugin
from .CanCreateText import CanCreateText
import bpy
from bpy.types import Panel

def draw_create_text_panel(self, context):
    # type: (bpy.types.Panel, bpy.ContextType) -> None
    layout = self.layout
    row = layout.row()
    row.operator("object.font_create_text")

class CreateTextPanel(Panel, Plugin, CanCreateText, ObjectWindowPanel):
    """Add the button to create text in object_data_properties"""
    bl_label = "Create Font Text Image"
    bl_idname = "OBJECT_PT_create_text_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_create_text_panel(self, context)

class CreateTextItemsPanel(Panel, Plugin, CanCreateText, ItemsPanel):
    """Add the button to create text in object_data_properties"""
    bl_label = "Create Font Text Image"
    bl_idname = "OBJECT_PT_create_text_items_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_create_text_panel(self, context)
