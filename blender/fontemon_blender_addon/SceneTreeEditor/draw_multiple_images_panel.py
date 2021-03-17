from .get_or_make_animation_pattern import get_animation_pattern_or_fake
import bpy
from .draw_load_animated_images_panel import draw_load_animated_images_panel

def draw_multiple_images_panel(layout, active_object,  image_objects, props):
    # type: (bpy.types.UILayout, bpy.EmptyImageObjectTypeWithData, list[bpy.EmptyImageObjectTypeWithData], bpy.AnimatedImagePropertiesType) -> None
    _ = layout.prop(props, "all_visible")
    layout.label(text="Load Animated Images:")
    draw_load_animated_images_panel(
        layout=layout.box(),
        pattern_info=get_animation_pattern_or_fake(active_object),
        number_of_objects=len(image_objects),
        props=props
    )

    layout.label(text="Animation:")
    box = layout.box()
    make_animation_props = box.operator("font.makeanimation")
    use_current_frame = ("font_animation_use_current_frame" not in active_object or
                            active_object["font_animation_use_current_frame"])
    make_animation_props.use_current_frame = use_current_frame
    make_animation_props.frame_number = (
        0 if not 'animation_frame_number' in active_object else active_object['font_animation_start_frame'])
    make_animation_props.key_before = props.animation_key_before
    make_animation_props.key_after = props.animation_key_after
    make_animation_props.repeat_times = props.animation_repeat_times
    _ = box.prop(props, "animation_key_before")
    _ = box.prop(props, "animation_key_after")
    _ = box.prop(props, "animation_repeat_times")
    _ = box.prop(props, "animation_use_current_frame")
    if not use_current_frame:
        _ = box.prop(props, "animation_frame_number")
   