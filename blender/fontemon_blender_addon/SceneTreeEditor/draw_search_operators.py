import bpy


def draw_search_operators(layout):
    # type: (bpy.types.UILayout) -> None
    layout.operator("font.scenesearch")
    layout.operator("font.slotnamesearch")
    layout.operator("font.slotimagesearch")
