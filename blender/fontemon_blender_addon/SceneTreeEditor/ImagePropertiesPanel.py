from .draw_multiple_images_panel import draw_multiple_images_panel
from ..Plugin import Plugin
import bpy
from bpy.types import Panel
from ..Common import image_object
from ..Common import (ObjectWindowPanel, ItemsPanel,
                      ObjectDataPanel, ToolPanel, ViewPanel, FontPanel)
from bpy.utils import register_class, unregister_class
from bpy.props import PointerProperty
from .ImageProperties import ImageProperties
from .get_slot_info import get_slot_info
from .multiple_image_objects import multiple_image_objects
from .all_objects_have_slots import all_objects_have_slots
from .draw_parent_info import draw_parent_info


def draw_image_properties_panel(self, context):
    # type: (bpy.types.Panel, bpy.ContextType) -> None
    layout = self.layout
    o = image_object(context.object)
    if o is None:
        return

    props = context.window_manager.image_props

    image_objects = multiple_image_objects(context)
    if image_objects is not None:
        _ = layout.prop(props, "is_visible", text="Active Object Visible")
    else:
        layout.template_ID(o, "data", open="image.open",
                           unlink="object.unlink_data")
        _ = layout.prop(props, "is_visible")
    parent_box = layout.box()
    if 'font_word_id' in o:
        _ = layout.operator("font.selectparent", text="Select Word Root")
    else:
        draw_parent_info(parent_box, o, image_objects)

    if image_objects is not None:
        # if all objects in image_objects do not have a parent, then
        # show the make_parent operator
        if next((False for o in image_objects if o.parent is not None), True):
            parent_box.operator("font.make_parent")
        else:
            clear_props = parent_box.operator(
                "object.parent_clear", text="Remove Parent object")
            clear_props.type = "CLEAR_KEEP_TRANSFORM"

        draw_multiple_images_panel(layout=layout,
                                   active_object=o,
                                   image_objects=image_objects,
                                   props=props
                                   )

    layout.label(text="Slot properties")
    box = layout.box()
    if image_objects is None:
        is_a_slot = get_slot_info(o) is not None
        _ = box.prop(props, "is_slot", text="Slot")
        if is_a_slot:
            _ = box.prop(props, "slot_number")
            _ = box.prop(props, "slot_name")
    else:
        _ = box.prop(props, "all_are_slots")
        if all_objects_have_slots(image_objects):
            _ = box.prop(props, "all_slot_numbers")
            _ = box.prop(props, "all_slot_names")
            box.label(text="Assign slots with a pattern")
            _ = box.prop(props, "all_slot_start")
            _ = box.prop(props, "all_slot_name_pattern")
            op = box.operator("font.assignslotsinpattern")
            op.pattern = props.all_slot_name_pattern
            op.slot_start = props.all_slot_start


class IsImageObject:
    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        return image_object(context.object) is not None


class ImagePropertiesPanel(Panel, IsImageObject, ObjectWindowPanel):
    """The panel to configure an image"""
    bl_label = "Font Image Properties"
    bl_idname = "OBJECT_PT_image_properties_panel"

    @classmethod
    def plug_in(cls):
        register_class(ImageProperties),
        bpy.types.WindowManager.image_props = PointerProperty(
            name="Image Properties", type=ImageProperties)
        register_class(cls)
        ImagePropertiesItemsPanel.plug_in()
        ImagePropertiesFontPanel.plug_in()
        ImagePropertiesToolsPanel.plug_in()
        ImagePropertiesViewPanel.plug_in()
        ImagePropertiesDataPanel.plug_in()

    @classmethod
    def plug_out(cls):
        ImagePropertiesDataPanel.plug_out()
        ImagePropertiesViewPanel.plug_out()
        ImagePropertiesToolsPanel.plug_out()
        ImagePropertiesFontPanel.plug_out()
        ImagePropertiesItemsPanel.plug_out()
        unregister_class(cls)
        del bpy.types.WindowManager.image_props
        unregister_class(ImageProperties)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_image_properties_panel(self, context)


class ImagePropertiesItemsPanel(Panel, Plugin, IsImageObject, ItemsPanel):
    """The panel to configure an image"""
    bl_label = "Font Image Properties"
    bl_idname = "OBJECT_PT_image_properties_items_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_image_properties_panel(self, context)


class ImagePropertiesFontPanel(Panel, Plugin, IsImageObject, FontPanel):
    """The panel to configure an image"""
    bl_label = "Font Image Properties"
    bl_idname = "OBJECT_PT_image_properties_font_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_image_properties_panel(self, context)


class ImagePropertiesToolsPanel(Panel, Plugin, IsImageObject, ToolPanel):
    """The panel to configure an image"""
    bl_label = "Font Image Properties"
    bl_idname = "OBJECT_PT_image_properties_tools_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_image_properties_panel(self, context)


class ImagePropertiesViewPanel(Panel, Plugin, IsImageObject, ViewPanel):
    """The panel to configure an image"""
    bl_label = "Font Image Properties"
    bl_idname = "OBJECT_PT_image_properties_view_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_image_properties_panel(self, context)


class ImagePropertiesDataPanel(Panel, Plugin, IsImageObject, ObjectDataPanel):
    """The panel to configure an image"""
    bl_label = "Font Image Properties"
    bl_idname = "OBJECT_PT_image_properties_data_panel"

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_image_properties_panel(self, context)
