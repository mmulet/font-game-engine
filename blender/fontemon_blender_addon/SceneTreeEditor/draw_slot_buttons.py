import bpy
from .find_slot_names_merged import find_slot_names_merged

def draw_slot_buttons(menu, layout):
    # type: (bpy.SelectSlottable, bpy.types.UILayout) -> None
    _ = layout.prop(menu, "number_of_slots", text="Slots")
    if menu.number_of_slots > 0:
        props = layout.operator("font.generatefixslots")
        if menu.node_scene:
            props.node_scene_name = menu.node_scene.name
    slot_names = find_slot_names_merged(menu.node_scene)
    for i in range(menu.number_of_slots):
        slot_prop = f"node_slot{i + 1}"
        row = layout.row()
        if i in slot_names:
            _ = row.prop(menu, slot_prop, text=slot_names[i])
        else:
            _ = row.prop(menu, slot_prop)
        select_slot_operator = row.operator("font.selectslot", text="", icon="SELECT_SET")
        select_slot_operator.slotNumber = i
        select_slot_operator.nodeSceneName = menu.node_scene.name
        
        