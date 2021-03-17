from ..Common import (FontPanel, ItemsPanel, ToolPanel, ViewPanel)
from ..Plugin import Plugin
from bpy.types import Panel
import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Panel, PropertyGroup
from bpy.props import StringProperty, PointerProperty, BoolProperty, IntProperty
from .draw_open_test_font_button import draw_open_test_font_button


class ConverterProperties(PropertyGroup):
    """Properties for searching the font scene tree"""
    images_folder: StringProperty(
        name="Images Folder",
        default="//../../images",
        subtype="DIR_PATH",
        description="""Where to save converted images.
        This is where:
        - The Converter will save images
        - The text will grab text images
        - Animations will get images""",
    )
    otf_file_path: StringProperty(name=".otf file",
                                  description="The path of your otf file",
                                  default="//font_game.otf",
                                  subtype="FILE_PATH")
    use_most_recent_export: BoolProperty(
        name="Use latest export",
        description=
        "Use the path of the most recent export as the path of the otf file",
        default=True,
    )
    most_recent_otf_export_path: StringProperty(
        name="Most recent .otf file",
        description="The path of your otf file",
        default="//font_game.otf",
        subtype="FILE_PATH")
    export_number: IntProperty(name="Export number", default=1)


def draw_always_on_font_panel(self, context):
    # type: (bpy.types.Panel, bpy.ContextType) -> None
    layout = self.layout
    layout.operator("font.add_font_image", icon="IMAGE_DATA")
    layout.operator("font.add_font_text", icon="SYNTAX_OFF")
    layout.operator("font.add_font_animation", icon="RENDER_ANIMATION")

    box4 = layout.box()
    props = context.window_manager.converter_props
    box4.label(text="Images folder")
    _ = box4.prop(props, "images_folder")
    box = layout.box()
    box.label(text="Tools:")
    box.operator("font.open_text_preview")
    box.operator("font.open_converter")
    draw_open_test_font_button(box, context)


class AlwaysOn:
    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        return True


class AlwaysOnFontPanel(Panel, AlwaysOn, FontPanel):
    """This panel is always on, so the user doesn't have to navigate away from the Font Tab"""
    bl_label = "Home Base"
    bl_idname = "OBJECT_PT_always_on_font_panel"

    @classmethod
    def plug_in(cls):
        register_class(ConverterProperties)
        bpy.types.WindowManager.converter_props = PointerProperty(
            name="Converter Properties", type=ConverterProperties)
        register_class(cls)
        AlwaysOnToolPanel.plug_in()
        AlwaysOnItemsPanel.plug_in()
        AlwaysOnViewPanel.plug_in()

    @classmethod
    def plug_out(cls):
        AlwaysOnViewPanel.plug_out()
        AlwaysOnItemsPanel.plug_out()
        AlwaysOnToolPanel.plug_out()
        unregister_class(cls)
        del bpy.types.WindowManager.converter_props
        unregister_class(ConverterProperties)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_always_on_font_panel(self, context)


class AlwaysOnToolPanel(Panel, Plugin, AlwaysOn, ToolPanel):
    """This panel is always on, so the user doesn't have to navigate away from the Font Tab"""
    bl_label = "Home Base"
    bl_idname = "OBJECT_PT_always_on_tool_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_always_on_font_panel(self, context)


class AlwaysOnItemsPanel(Panel, Plugin, AlwaysOn, ItemsPanel):
    """This panel is always on, so the user doesn't have to navigate away from the Font Tab"""
    bl_label = "Home Base"
    bl_idname = "OBJECT_PT_always_on_items_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_always_on_font_panel(self, context)


class AlwaysOnViewPanel(Panel, Plugin, AlwaysOn, ViewPanel):
    """This panel is always on, so the user doesn't have to navigate away from the Font Tab"""
    bl_label = "Home Base"
    bl_idname = "OBJECT_PT_always_on_view_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_always_on_font_panel(self, context)
