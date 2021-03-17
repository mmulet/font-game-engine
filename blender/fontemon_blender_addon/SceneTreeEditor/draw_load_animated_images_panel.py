import bpy
from .get_image_name_from_pattern import get_image_name_from_pattern


def draw_load_animated_images_panel(layout, pattern_info, number_of_objects, props):
    # type: (bpy.types.UILayout, bpy.AnimationPatternInfoType, int, bpy.AnimatedImagePropertiesType) -> None
    _ = layout.operator("font.loadanimatedimages")
    _ = layout.prop(props, "animation_number_of_objects")
    _ = layout.prop(props, "animation_pattern_type")
    type = pattern_info["type"]
    if type == "PYTHON":
        _ = layout.prop(props, "animation_python_snippet")
        return
    _ = layout.prop(props, "animation_file_name")
    _ = layout.prop(props, "animation_file_extension")
    _ = layout.prop(props, "animation_num_digits")
    if type == "INCREMENT" or type == "DECREMENT":
        _ = layout.prop(props, "animation_start_number")
        _ = layout.prop(props, "animation_wrap_around")
        if pattern_info["wrap_around"]:
            _ = layout.prop(props, "animation_end_number")
            if type == "INCREMENT" and props.animation_start_number > props.animation_end_number:
                _ = layout.label(
                    text=f"WARNING: Start Number is greater than the final number. {props.animation_start_number} > {props.animation_end_number}")
            elif type == "DECREMENT" and props.animation_end_number > props.animation_start_number:
                _ = layout.label(
                    text=f"WARNING: Start Number is less than the final number. {props.animation_start_number} < {props.animation_end_number}")
    elif type == "PATTERN":
        pattern_size = pattern_info["pattern_size"]
        _ = layout.prop(props, f"animation_pattern{pattern_size}")
        _ = layout.prop(props, "animation_pattern_size")
    layout.label(text="Preview:")
    _ = layout.prop(props, "animation_show_all_preview")
    if not props.animation_show_all_preview:
        _ = layout.prop(props, "animation_number_of_preview_name")

    for i in range(number_of_objects if props.animation_show_all_preview else props.animation_number_of_preview_name):
        layout.label(text=get_image_name_from_pattern(i, type, pattern_info))
