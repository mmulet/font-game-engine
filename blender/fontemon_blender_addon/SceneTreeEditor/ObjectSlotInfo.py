import bpy
from .SlotInfo import SlotInfo

class ObjectSlotInfo:
    def __init__(self, object, slot) -> None:
        # type: (bpy.EmptyImageObjectTypeWithData, bpy.Optional[SlotInfo]) -> None
        self.object = object
        self.slot = slot

    def apply(self):
        if self.slot is None:
            self.object["font_is_a_slot"] = False
            return
        self.object["font_is_a_slot"] = True
        self.object["font_slot_number"] = self.slot.number
        self.object["font_slot_name"] = self.slot.name