import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, IntVectorProperty, StringProperty, IntProperty, EnumProperty
from .get_slot_info import get_slot_info
from .image_is_visible import image_is_visible
from .ImagePropertiesAccessors import *
from .multiple_image_objects import multiple_image_objects
from .all_objects_have_slots import all_objects_have_slots
from ..Common import image_object
from .get_or_make_animation_pattern import get_or_make_animation_pattern
default_animation_pattern = 'f"filename{iz(3)}.png"'


def set_visible(o, value):
    # type: (bpy.EmptyImageObjectTypeWithData, bool) -> None
    o.show_empty_image_orthographic = value
    o.keyframe_insert(
        "show_empty_image_orthographic",
        frame=bpy.context.scene.frame_current
    )


def set_is_a_slot(o, value):
    # type: (bpy.EmptyImageObjectTypeWithData, bool) -> None
    if not value:
        o["font_is_a_slot"] = False
        return
    o["font_is_a_slot"] = True
    if "font_slot_number" not in o:
        o['font_slot_number'] = 0
    if "font_slot_name" not in o:
        o['font_slot_name'] = ""


class ImageProperties(PropertyGroup):
    """Property for editing images"""

    def get_number_of_objects(self):
        # type: () -> int
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return 0
        return len(objects)

    def set_number_of_objects(self, value):
        # type: (int) -> None
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return
        num_objects = len(objects)
        if num_objects == value:
            return
        if num_objects < value:
            number_to_create = value - num_objects
            last_object = objects[num_objects - 1]
            for _ in range(number_to_create):
                o = bpy.data.objects.new(
                    name=last_object.name,
                    object_data=None
                )
                bpy.context.view_layer.active_layer_collection.collection.objects.link(
                    o)
                o.data = last_object.data
                o.empty_display_type = "IMAGE"
                o.parent = last_object.parent
                o.location[0] = last_object.location[0]
                o.location[2] = last_object.location[2]
                o.select_set(True)
            return
        for o in objects[value:]:
            o.parent = None
            o.select_set(False)
            bpy.context.view_layer.active_layer_collection.collection.objects.unlink(o)

    animation_number_of_objects: IntProperty(
        name="Number of Images",
        description="The number of images in this animation",
        min=2,
        get=get_number_of_objects,
        set=set_number_of_objects
    )

    animation_show_all_preview: BoolProperty(
        name="Preview all selected names",
        description="Preview all selected names",
        default=True
    )

    animation_number_of_preview_name: IntProperty(
        name="Number of images to preview",
        description="Number of images to preview",
        min=0,
        default=1
    )

    animation_types = [
        ("INCREMENT", "Increment", "Load files counting upwards", 1),
        ("DECREMENT", "Decrement", "Load files counting downwards", 2),
        ("PATTERN", "Pattern",
         "Load files in a pattern", 3),
        ("PYTHON", "Python", "Load files in a pattern given a python script", 4)
    ]

    def get_animation_pattern_type(self):
        # type: () -> int
        o = image_object(bpy.context.active_object)
        if o is None or "font_animation_pattern_info" not in o:
            return 1
        type = o["font_animation_pattern_info"]["type"]
        if type == "INCREMENT":
            return 1
        if type == "DECREMENT":
            return 2
        if type == "PATTERN":
            return 3
        if type == "PYTHON":
            return 4
        return 1

    def set_animation_pattern_type(self, value):
        # type: (int) -> None
        o = image_object(bpy.context.active_object)
        if o is None:
            return
        pattern = get_or_make_animation_pattern(o)

        if value == 1:
            pattern["type"] = "INCREMENT"
        elif value == 2:
            pattern["type"] = "DECREMENT"
        elif value == 3:
            pattern["type"] = "PATTERN"
        elif value == 4:
            pattern["type"] = "PYTHON"

    animation_pattern_type: EnumProperty(
        items=animation_types,
        name="Pattern Type",
        get=get_animation_pattern_type,
        set=set_animation_pattern_type)

    animation_num_digits: IntProperty(
        name="Number of Digits",
        get=lambda s: pattern_get_prop("num_digits", 2),
        set=lambda s, v: pattern_set_prop("num_digits", v)
    )

    animation_start_number: IntProperty(
        name="First Number",
        min=0,
        get=lambda s: pattern_get_prop("start_number", 0),
        set=lambda s, v: pattern_set_prop("start_number", v)
    )
    animation_end_number: IntProperty(
        name="Last Number",
        min=0,
        get=lambda s: pattern_get_prop("end_number", 0),
        set=lambda s, v: pattern_set_prop("end_number", v)
    )

    animation_wrap_around: BoolProperty(
        name="Wrap Around",
        description="After you go above end number, start again from the beginning",
        get=lambda s: pattern_get_prop("wrap_around", True),
        set=lambda s, v: pattern_set_prop("wrap_around", v)
    )

    animation_file_name: StringProperty(
        name="Filename pattern",
        description="The name of the file, don't include the number at the end. or the extension Example: if your file is image_000, then type in image_",
        get=lambda s: pattern_get_prop("filename", ""),
        set=lambda s, v: pattern_set_prop("filename", v)
    )
    animation_file_extension: StringProperty(
        name="File extension",
        description="The name of the file extension. Please include the .beforehand, like .png",
        get=lambda s: pattern_get_prop("extension", ".png"),
        set=lambda s, v: pattern_set_prop("extension", v)
    )

    animation_python_snippet: StringProperty(
        name="Python Snippet",
        description="A python expression to return the filename given the index i (starting at zero).\n Look at the docs for the list of helper functions",
        get=lambda s: pattern_get_prop(
            "python", ""),
        set=lambda s, v: pattern_set_prop("python", v)
    )

    animation_pattern_size: IntProperty(
        name="Pattern Size",
        min=1,
        max=14,
        get=lambda s: pattern_get_prop("pattern_size", 1),
        set=lambda s, v: pattern_set_prop("pattern_size", v)
    )

    animation_pattern1: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=1,
        get=lambda s: get_pattern_of_length(1),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern2: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=2,
        get=lambda s: get_pattern_of_length(2),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern3: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=3,
        get=lambda s: get_pattern_of_length(3),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern4: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=4,
        get=lambda s: get_pattern_of_length(4),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern5: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=5,
        get=lambda s: get_pattern_of_length(5),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern6: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=6,
        get=lambda s: get_pattern_of_length(6),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern7: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=7,
        get=lambda s: get_pattern_of_length(7),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern8: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=8,
        get=lambda s: get_pattern_of_length(8),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern9: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=9,
        get=lambda s: get_pattern_of_length(9),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern10: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=10,
        get=lambda s: get_pattern_of_length(10),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern11: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=11,
        get=lambda s: get_pattern_of_length(11),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern12: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=12,
        get=lambda s: get_pattern_of_length(12),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern13: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=13,
        get=lambda s: get_pattern_of_length(13),
        set=lambda s, v: set_pattern_of_length(v),
    )
    animation_pattern14: IntVectorProperty(
        name="Pattern",
        min=0,
        description="A pattern of numbers like [0,3,2] will load filename00, filename03, filename02, filename00, filename003 and so on",
        size=14,
        get=lambda s: get_pattern_of_length(14),
        set=lambda s, v: set_pattern_of_length(v),
    )

    animation_key_before: BoolProperty(
        name="Invisible before",
        get=lambda s: get_prop("font_animation_key_before", True),
        set=lambda s, v: set_prop("font_animation_key_before", v),
        description="Add a key, setting all frames to invisible, before the animation"
    )
    animation_key_after: BoolProperty(
        name="Invisible After",
        get=lambda s: get_prop("font_animation_key_after", True),
        set=lambda s, v: set_prop("font_animation_key_after", v),
        description="Add a key, setting all frames to invisible, after the animation"
    )

    animation_repeat_times: IntProperty(
        name="Number Of Times",
        min=1,
        description="Play the animation this number of times. If you put 1, it will play once.",
        get=lambda s: get_prop("font_animation_repeat_times", 1),
        set=lambda s, v: set_prop("font_animation_repeat_times", v),
    )

    animation_use_current_frame: BoolProperty(
        name="Use Current Frame",
        description="Use the current frame as the start of the animation",
        get=lambda s: get_prop(
            "font_animation_use_current_frame", default=True),
        set=lambda s, v: set_prop("font_animation_use_current_frame", v)
    )

    animation_frame_number: IntProperty(
        name="Frame Number",
        description="The frame number to start the animation",
        get=lambda s: get_prop(
            "font_animation_start_frame", 0),
        set=lambda s, v: set_prop("font_animation_start_frame", v)
    )

    slot_name: StringProperty(
        name="Slot Name",
        description="(Optional) The name of the slot, only for your convenience.\nThis name will appear in the scene tree editor",
        get=lambda s: get_prop("font_slot_name", ""),
        set=lambda s, v: set_prop(
            "font_slot_name", v)
    )

    slot_number: IntProperty(
        name="Slot Number",
        description="All slots that share this slot number will be replaced by the same image",
        get=lambda s: get_prop("font_slot_number", 0),
        set=lambda s, v: set_prop("font_slot_number", v)
    )

    def get_is_slot(self):
        # type: () -> bool
        o = image_object(bpy.context.active_object)
        if o is None:
            return False
        return get_slot_info(o) is not None

    def set_is_slot(self, value):
        # type: (bool) -> None
        o = image_object(bpy.context.active_object)
        if o is None:
            return
        set_is_a_slot(o, value=value)

    is_slot: BoolProperty(
        name="Slot",
        description="If this is image is a slot, then the template image will be replaced by 'slot' image when you export the scene",
        get=get_is_slot,
        set=set_is_slot)

    def get_is_visible(self):
        # type: () -> bool
        o = image_object(bpy.context.active_object)
        if o is None:
            return False
        return image_is_visible(o, bpy.context.scene.frame_current)

    def set_is_visible(self, value):
        # type: (bool) -> None
        o = image_object(bpy.context.active_object)
        if o is None:
            return
        set_visible(o, value=value)

    is_visible: BoolProperty(
        name="Visible",
        description="If the image is visible or invisible at this frame.",
        get=get_is_visible,
        set=set_is_visible)

    def get_all_are_visible(self):
        # type: () -> bool
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return False
        for o in objects:
            if not image_is_visible(o, bpy.context.scene.frame_current):
                return False
        return True

    def set_all_are_visible(self, value):
        # type: (bool) -> None
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return
        for o in objects:
            set_visible(o, value=value)

    all_visible: BoolProperty(
        name="All Visible",
        description="If all selected images are visible.",
        get=get_all_are_visible,
        set=set_all_are_visible)

    def get_all_are_slots(self):
        # type: () -> bool
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return False
        return all_objects_have_slots(objects)

    def set_all_are_slots(self, value):
        # type: (bool) -> None
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return
        for o in objects:
            set_is_a_slot(o, value=value)

    all_are_slots: BoolProperty(
        name="Are all slots",
        description="If these is images are slots, then the template image will be replaced by 'slot' image when you export the scene",
        get=get_all_are_slots,
        set=set_all_are_slots)

    def get_all_slot_numbers(self):
        # type: () -> int
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return -1
        slot_num = -1
        for o in objects:
            slot_info = get_slot_info(o)
            if slot_info is None:
                return -1
            if slot_info.number == slot_num:
                continue
            if slot_num != -1:
                return -1
            slot_num = slot_info.number
        return slot_num

    def set_all_slot_numbers(self, value):
        # type: (int) -> None
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return
        for o in objects:
            o["font_slot_number"] = value

    all_slot_numbers: IntProperty(
        name="All Slot Numbers (-1 if they disagree)",
        description="All slots that share this slot number will be replaced by the same image",
        get=get_all_slot_numbers,
        set=set_all_slot_numbers
    )

    def get_all_slot_names(self):
        # type: () -> str
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return "No names"
        names = {o['font_slot_name']
                 for o in objects if 'font_slot_name' in o and o['font_slot_name'] != ""}
        if len(names) <= 0:
            return "No names"
        return " & ".join(names)

    def set_all_slot_names(self, value):
        # type: (str) -> None
        objects = multiple_image_objects(bpy.context)
        if objects is None:
            return
        for o in objects:
            o["font_slot_name"] = value

    all_slot_names: StringProperty(
        name="All Slot Names",
        description="(Optional) The name of the slot, only for your convenience.\nThis name will appear in the scene tree editor",
        get=get_all_slot_names,
        set=set_all_slot_names
    )

    all_slot_start: IntProperty(name="Starting at slot number", default=0)
    all_slot_name_pattern: StringProperty(
        name="Pattern",
        description="A python expression to return the filename given the index i (starting at zero).",
        default="f\"slot{i}\""
    )
