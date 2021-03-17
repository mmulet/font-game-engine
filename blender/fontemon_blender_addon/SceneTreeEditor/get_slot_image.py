import bpy


def get_slot_image(slottable, slot_number_one_based):
    # type: (bpy.AllSceneNodeTypes, int) -> bpy.Optional[bpy.types.Image]
    if(slot_number_one_based == 1):
        return slottable.node_slot1
    if(slot_number_one_based == 2):
        return slottable.node_slot2
    if(slot_number_one_based == 3):
        return slottable.node_slot3
    if(slot_number_one_based == 4):
        return slottable.node_slot4
    if(slot_number_one_based == 5):
        return slottable.node_slot5
    if(slot_number_one_based == 6):
        return slottable.node_slot6
    if(slot_number_one_based == 7):
        return slottable.node_slot7
    if(slot_number_one_based == 8):
        return slottable.node_slot8
    if(slot_number_one_based == 9):
        return slottable.node_slot9
    if(slot_number_one_based == 10):
        return slottable.node_slot10
    if(slot_number_one_based == 11):
        return slottable.node_slot11
    if(slot_number_one_based == 12):
        return slottable.node_slot12
    if(slot_number_one_based == 13):
        return slottable.node_slot13
    if(slot_number_one_based == 14):
        return slottable.node_slot14
    if(slot_number_one_based == 15):
        return slottable.node_slot15
    if(slot_number_one_based == 16):
        return slottable.node_slot16
    if(slot_number_one_based == 17):
        return slottable.node_slot17
    if(slot_number_one_based == 18):
        return slottable.node_slot18
    if(slot_number_one_based == 19):
        return slottable.node_slot19
    if(slot_number_one_based == 20):
        return slottable.node_slot20
    return None


def set_slot_image(slottable, slot_number_one_based, image):
    # type: (bpy.AllSceneNodeTypes, int, bpy.types.Image) -> None
    if(slot_number_one_based == 1):
        slottable.node_slot1 = image
        return
    if(slot_number_one_based == 2):
        slottable.node_slot2 = image
        return
    if(slot_number_one_based == 3):
        slottable.node_slot3 = image
        return
    if(slot_number_one_based == 4):
        slottable.node_slot4 = image
        return
    if(slot_number_one_based == 5):
        slottable.node_slot5 = image
        return
    if(slot_number_one_based == 6):
        slottable.node_slot6 = image
        return
    if(slot_number_one_based == 7):
        slottable.node_slot7 = image
        return
    if(slot_number_one_based == 8):
        slottable.node_slot8 = image
        return
    if(slot_number_one_based == 9):
        slottable.node_slot9 = image
        return
    if(slot_number_one_based == 10):
        slottable.node_slot10 = image
        return
    if(slot_number_one_based == 11):
        slottable.node_slot11 = image
        return
    if(slot_number_one_based == 12):
        slottable.node_slot12 = image
        return
    if(slot_number_one_based == 13):
        slottable.node_slot13 = image
        return
    if(slot_number_one_based == 14):
        slottable.node_slot14 = image
        return
    if(slot_number_one_based == 15):
        slottable.node_slot15 = image
        return
    if(slot_number_one_based == 16):
        slottable.node_slot16 = image
        return
    if(slot_number_one_based == 17):
        slottable.node_slot17 = image
        return
    if(slot_number_one_based == 18):
        slottable.node_slot18 = image
        return
    if(slot_number_one_based == 19):
        slottable.node_slot19 = image
        return
    if(slot_number_one_based == 20):
        slottable.node_slot20 = image
        return
    return None
