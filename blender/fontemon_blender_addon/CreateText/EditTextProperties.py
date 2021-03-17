import bpy
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, IntProperty, BoolProperty, StringProperty, FloatProperty
from .EditTextAccessors import *


class EditTextProperties(PropertyGroup):
    """Property for editing text"""

    text: StringProperty(name="Text",
                         description="The text to create",
                         get=lambda s: get_prop("font_text", ""),
                         set=lambda s, v: set_prop("font_text", v)
                         )

    top_line_location: FloatProperty(
        name="Top line location",
        description="Location of the top line, relative to the parent (this text object)",
        get=lambda s: get_prop("font_text_top_line_location", 0.0),
        set=lambda s, v: set_prop("font_text_top_line_location", v)
    )

    bottom_line_location: FloatProperty(
        name="Bottom line location",
        description="Location of the bottom line, relative to the parent (this text object)",
        get=lambda s: get_prop("font_text_bottom_line_location", 0.0),
        set=lambda s, v: set_prop("font_text_bottom_line_location", v)
    )

    character_spacing: FloatProperty(
        name="Character spacing",
        description="The space between the characters (there is no kerning). Only valid for character text (not word text)",
        get=lambda s: get_prop("font_text_character_spacing", 0.0),
        set=lambda s, v: set_prop("font_text_character_spacing", v)
    )

    line_width: IntProperty(
        name="Max # of characters per line",
        description="How many characters can appear in one line. If the line goes over this limit, the line will split into two lines.",
        get=lambda s: get_prop("font_text_line_width", 0),
        set=lambda s, v: set_prop("font_text_line_width", v)
    )

    word_based: BoolProperty(name="Word based",
                             description="Use a word based (one word per frame) otherwise use character based (one character per frame)",
                             get=lambda s: get_prop(
                                 "font_text_word_based_frame", False),
                             set=lambda s, v: set_prop(
                                 "font_text_word_based_frame", v)
                             )

    use_current_frame_as_start: BoolProperty(name="Use Current frame as start",
                                             description="Use the current frame (in the editor) as the starting point for the text.",
                                             get=lambda s: get_prop(
                                                 "font_text_use_current_frame_as_start", True),
                                             set=lambda s, v: set_prop(
                                                 "font_text_use_current_frame_as_start", v)
                                             )

    start_frame: IntProperty(
        name="Start Frame",
        description="The frame at which the text should appear",
        get=lambda s: get_prop("font_text_start_frame", 0),
        set=lambda s, v: set_prop("font_text_start_frame", v)
    )

    end_frame: IntProperty(
        name="end_frame",
        description="The text should disappear at this frame",
        get=lambda s: get_end_prop("end_frame"),
        set=lambda s, v: set_end_prop("end_frame", v)
    )

    length: IntProperty(
        name="length",
        min=0,
        description="The text should disappear after length frames",
        get=lambda s: get_end_prop("length"),
        set=lambda s, v: set_end_prop("length", v)
    )

    end_offset: IntProperty(
        name="Offset",
        min=0,
        description="The text should disappear at the end of the writing + End Offset frames (may be negative)",
        get=lambda s: get_end_prop("end_offset"),
        set=lambda s, v: set_end_prop("end_offset", v)
    )

    end_types = [
        ("END", "End Frame", "The text should disappear at this frame", 1),
        ("LENGTH", "Length", "The text should disappear after length frames", 2),
        ("OFFSET", "End Offset",
         "The text should disappear at the end of the writing + End Offset frames (may be negative)", 3),
        ("INFINITE", "Infinite", "The text should never disappear", 4)
    ]

    def get_end_type(self):
        # type: () -> int
        o = text_object(bpy.context.active_object)
        if o is None:
            return 1
        type = o['font_text_end']["type"]
        if type == "END":
            return 1
        if type == "LENGTH":
            return 2
        if type == "OFFSET":
            return 3
        if type == "INFINITE":
            return 4
        return 1

    def set_end_type(self, value):
        # type: (int) -> None
        o = text_object(bpy.context.active_object)
        if o is None:
            return
        end = o['font_text_end']
        outType = "END"
        if value == 1:
            outType = "END"
        elif value == 2:
            outType = "LENGTH"
        elif value == 3:
            outType = "OFFSET"
        elif value == 4:
            outType = "INFINITE"
        end["type"] = outType

    end_type: EnumProperty(items=end_types,
                           name="End Type",
                           get=get_end_type,
                           set=set_end_type)
