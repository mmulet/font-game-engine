import bpy

def draw_node_scene(menu, layout):
    # type: (bpy.HasNodeScene, bpy.types.UILayout) -> None
    row = layout.row()
    _ = row.prop(menu, "node_scene")
    jump_properties = row.operator(
        "font.jumptoscene", text="", icon="RIGHTARROW")
    jump_properties.nodeSceneName = (
        "" if menu.node_scene is None else menu.node_scene.name)