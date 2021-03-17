
import bpy
from bpy.types import Panel, PropertyGroup
from bpy.props import BoolProperty, FloatProperty, PointerProperty
from bpy.utils import register_class, unregister_class


class SizeProperties(PropertyGroup):
    """AutomaticSizing Properities"""
    global_enable: BoolProperty(name="Enabled", default=True)
    poll_every_seconds: FloatProperty(
        default=1.0,
        name="Time Interval", description="Check every {this number} seconds for changes. Increase this number to increase performance.")
    lock_viewport_to_camera: BoolProperty(
        name="Lock Viewport To Camera", default=True)
    keep_sidebar_on_at_all_times: BoolProperty(
        name="Keep Sidebar On at all times", default=True)
    reset_image_y_location: BoolProperty(
        name="Reset Image Y Location", default=True)
    lock_camera_position: BoolProperty(
        name="Lock Camera Position", default=True)
    regenerate_deleted_camera: BoolProperty(
        name="Regenerate Deleted Camera", default=True)
    size_images: BoolProperty(name="Size Images", default=True)
    reset_image_offset: BoolProperty(name="Reset Image Offset", default=True)
    lock_image_scale: BoolProperty(name="Lock Image Scale", default=True)
    lock_image_rotation: BoolProperty(name="Lock Image Rotation", default=True)


class SizePanel(Panel):
    """Automatic sizing"""
    bl_label = "Font Automatic Adjustments"
    bl_idname = "OBJECT_PT_sizepanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "Auto Settings"
    bl_region_type = "UI"

    @classmethod
    def plug_in(cls):
        register_class(SizeProperties),
        bpy.types.WindowManager.size_props = PointerProperty(
            name="Size Properties", type=SizeProperties)
        register_class(cls)

    @classmethod
    def plug_out(cls):
        unregister_class(cls)
        del bpy.types.WindowManager.size_props
        unregister_class(SizeProperties)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        layout = self.layout
        props = context.window_manager.size_props
        layout.label(
            text="These are the settings for automatic adjustments made by the addon.")
        layout.label(
            text="These adjustments ensure that 'what you see is what you get'.")
        layout.label(
            text="If you turn any of these off, weird things will happen,")
        layout.label(
            text="so don't do turn them off unless you know what you are doing.")
        _ = layout.prop(props, "global_enable")
        _ = layout.prop(props, "poll_every_seconds")
        _ = layout.prop(props, "lock_viewport_to_camera")
        _ = layout.prop(props, "keep_sidebar_on_at_all_times")
        _ = layout.prop(props, "reset_image_y_location")
        _ = layout.prop(props, "lock_camera_position")
        _ = layout.prop(props, "regenerate_deleted_camera")
        _ = layout.prop(props, "size_images")
        _ = layout.prop(props, "reset_image_offset")
        _ = layout.prop(props, "lock_image_scale")
        _ = layout.prop(props, "lock_image_rotation")
