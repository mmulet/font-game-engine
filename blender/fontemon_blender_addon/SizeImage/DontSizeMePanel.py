from bpy.props import BoolProperty, PointerProperty
import bpy
from bpy.types import Panel, PropertyGroup
from ..Common import image_object
from ..Common import ObjectWindowPanel
from bpy.utils import register_class, unregister_class



def get_prop( field):
    # type: (bpy.EmptyImageDontSizeMeFields) -> bool
    o = image_object(bpy.context.active_object)
    if (o is None or field not in o):
        return False
    return o[field]

def set_prop(field, value):
    # type: (bpy.EmptyImageDontSizeMeFields, bool) -> None
    o = image_object(bpy.context.active_object)
    if o is None:
        return
    o[field] = value

class DontSizeMeProperties(PropertyGroup):
    """Dont size me properties """


    disable_automatic_size: BoolProperty(
        name="Disable Automatic Sizing",
        get=lambda s: get_prop("font_dont_size_me"),
        set=lambda s,v: set_prop("font_dont_size_me", v),
    )
    disable_export: BoolProperty(
        name="Disable Export",
        description="When Disabled, this image will not be part of the final export",
        get=lambda s: get_prop("font_disable_export"),
        set=lambda s,v: set_prop("font_disable_export", v),
    )


class DontSizeMePanel(Panel, ObjectWindowPanel):
    """Add the button to edit text in object_data_properties"""
    bl_label = "Don't Size Me"
    bl_idname = "OBJECT_PT_dont_size_me_panel"

    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        return image_object(context.object) is not None

    @classmethod
    def plug_in(cls):
        register_class(DontSizeMeProperties),
        bpy.types.WindowManager.dontsize_props = PointerProperty(
            name="Don's Size Me Properties", type=DontSizeMeProperties)
        register_class(cls)

    @classmethod
    def plug_out(cls):
        unregister_class(cls)
        del bpy.types.WindowManager.dontsize_props
        unregister_class(DontSizeMeProperties)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        layout = self.layout
        props = context.window_manager.dontsize_props
        layout.label(text="WARNING: If you disable automatic sizing, then ")
        layout.label(text="What you see, will NOT be what you get!")
        _ = layout.prop(props, "disable_automatic_size")
        layout.label(text="Disable export if this image will not be in the font.")
        _ = layout.prop(props, "disable_export")
