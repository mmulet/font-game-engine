import bpy


def draw_open_test_font_button(layout, context):
    # type: (bpy.types.UILayout, bpy.ContextType) -> None
    box = layout.box()
    props = context.window_manager.converter_props
    box.label(text="Path of the .otf file you want to test")
    _ = box.prop(props, "use_most_recent_export")
    if not props.use_most_recent_export:
        _ = box.prop(props, "otf_file_path")
    box.operator("font.open_test_font")
