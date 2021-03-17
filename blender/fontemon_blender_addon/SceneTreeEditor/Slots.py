from bpy.props import IntProperty, PointerProperty, StringProperty
from bpy.types import Image


class Slots:
    number_of_slots: IntProperty(
        default=0, min=0, max=20)

    node_slot1: PointerProperty(name="Slot 1", type=Image)
    node_slot2: PointerProperty(name="Slot 2", type=Image)
    node_slot3: PointerProperty(name="Slot 3", type=Image)
    node_slot4: PointerProperty(name="Slot 4", type=Image)
    node_slot5: PointerProperty(name="Slot 5", type=Image)
    node_slot6: PointerProperty(name="Slot 6", type=Image)
    node_slot7: PointerProperty(name="Slot 7", type=Image)
    node_slot8: PointerProperty(name="Slot 8", type=Image)
    node_slot9: PointerProperty(name="Slot 9", type=Image)
    node_slot10: PointerProperty(name="Slot 10", type=Image)
    node_slot11: PointerProperty(name="Slot 11", type=Image)
    node_slot12: PointerProperty(name="Slot 12", type=Image)
    node_slot13: PointerProperty(name="Slot 13", type=Image)
    node_slot14: PointerProperty(name="Slot 14", type=Image)
    node_slot15: PointerProperty(name="Slot 15", type=Image)
    node_slot16: PointerProperty(name="Slot 16", type=Image)
    node_slot17: PointerProperty(name="Slot 17", type=Image)
    node_slot18: PointerProperty(name="Slot 18", type=Image)
    node_slot19: PointerProperty(name="Slot 19", type=Image)
    node_slot20: PointerProperty(name="Slot 20", type=Image)

    number_of_word_slots: IntProperty(
        default=0, min=0, max=20)

    node_word_slot1: StringProperty(name="Word Slot 1")
    node_word_slot2: StringProperty(name="Word Slot 2")
    node_word_slot3: StringProperty(name="Word Slot 3")
    node_word_slot4: StringProperty(name="Word Slot 4")
    node_word_slot5: StringProperty(name="Word Slot 5")
    node_word_slot6: StringProperty(name="Word Slot 6")
    node_word_slot7: StringProperty(name="Word Slot 7")
    node_word_slot8: StringProperty(name="Word Slot 8")
    node_word_slot9: StringProperty(name="Word Slot 9")
    node_word_slot10: StringProperty(name="Word Slot 10")
    node_word_slot11: StringProperty(name="Word Slot 11")
    node_word_slot12: StringProperty(name="Word Slot 12")
    node_word_slot13: StringProperty(name="Word Slot 13")
    node_word_slot14: StringProperty(name="Word Slot 14")
    node_word_slot15: StringProperty(name="Word Slot 15")
    node_word_slot16: StringProperty(name="Word Slot 16")
    node_word_slot17: StringProperty(name="Word Slot 17")
    node_word_slot18: StringProperty(name="Word Slot 18")
    node_word_slot19: StringProperty(name="Word Slot 19")
    node_word_slot20: StringProperty(name="Word Slot 20")
