
from ..Plugin import Plugin
from .CanEditText import CanEditText
from ..Common import ObjectWindowPanel, ItemsPanel
import bpy
from bpy.types import Panel
from ..Common import (ObjectWindowPanel, ItemsPanel,
                      ObjectDataPanel, ToolPanel, ViewPanel, FontPanel)
from ..Plugin import Plugin
from ..Common import text_object
from .CanEditText import CanEditText
from .EditTextProperties import EditTextProperties
from bpy.types import Panel
from bpy.props import PointerProperty
from bpy.utils import register_class, unregister_class

def draw_edit_text_panel(self, context):
    # type: (bpy.types.Panel, bpy.ContextType) -> None
    layout = self.layout
    layout.operator("object.font_edit_text")
    o = text_object(context.active_object)
    if o is None:
        return
    props = context.window_manager.text_props
    layout.label(text="Text")
    box = layout.box()
    _ = box.prop(props, "text")
    word_based = o["font_text_word_based_frame"]
    _ = box.prop(props, "word_based", text=(
        "Advance one word per frame" if word_based else "Advance one character per frame"))
    if not word_based:
        # only show if we are not word based
        _ = box.prop(props, "character_spacing")
        
    layout.label(text="Line info")
    box = layout.box()
    _ = box.prop(props, "line_width")
    _ = box.prop(props, "top_line_location")
    _ = box.prop(props, "bottom_line_location")
    layout.label(text="Timing")
    box = layout.box()
    _ = box.prop(props, "use_current_frame_as_start")
    if not o["font_text_use_current_frame_as_start"]:
        _ = box.prop(props, "start_frame")
    _ = box.prop(props, "end_type")
    type = o["font_text_end"]["type"]
    if type == "END":
        _ = box.prop(props, "end_frame")
    elif type == "LENGTH":
        _ = box.prop(props, "length")
    elif type == "OFFSET":
        _ = box.prop(props, "end_offset")


class EditTextPanel(Panel, CanEditText, ObjectWindowPanel):
    """Add the button to edit text in object_data_properties"""
    bl_label = "Edit Font Text"
    bl_idname = "OBJECT_PT_edit_text_panel"

    @classmethod
    def plug_in(cls):
        register_class(EditTextProperties),
        bpy.types.WindowManager.text_props = PointerProperty(
            name="End Type", type=EditTextProperties)
        register_class(cls)
        EditTextItemsPanel.plug_in()
        EditTextFontPanel.plug_in()
        EditTextToolsPanel.plug_in()
        EditTextViewPanel.plug_in()
        EditTextDataPanel.plug_in()

    @classmethod
    def plug_out(cls):
        EditTextDataPanel.plug_out()
        EditTextViewPanel.plug_out()
        EditTextToolsPanel.plug_out()
        EditTextFontPanel.plug_out()
        EditTextItemsPanel.plug_out()
        unregister_class(cls)
        del bpy.types.WindowManager.text_props
        unregister_class(EditTextProperties)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_edit_text_panel(self, context)


class EditTextItemsPanel(Panel, Plugin, CanEditText, ItemsPanel):
    """Add the button to edit text in object_data_properties"""
    bl_label = "Edit Font Text"
    bl_idname = "OBJECT_PT_edit_text_items_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_edit_text_panel(self, context)

class EditTextFontPanel(Panel, Plugin, CanEditText, FontPanel):
    """The panel to configure an image"""
    bl_label = "Image Properties"
    bl_idname = "OBJECT_PT_edit_text_font_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_edit_text_panel(self, context)


class EditTextToolsPanel(Panel, Plugin, CanEditText, ToolPanel):
    """The panel to configure an image"""
    bl_label = "Image Properties"
    bl_idname = "OBJECT_PT_edit_text_tools_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_edit_text_panel(self, context)


class EditTextViewPanel(Panel, Plugin, CanEditText, ViewPanel):
    """The panel to configure an image"""
    bl_label = "Image Properties"
    bl_idname = "OBJECT_PT_edit_text_view_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_edit_text_panel(self, context)


class EditTextDataPanel(Panel, Plugin, CanEditText, ObjectDataPanel):
    """Add the button to edit text in object_data_properties"""
    bl_label = "Edit Font Text"
    bl_idname = "OBJECT_PT_edit_text_data_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_edit_text_panel(self, context)
