
from ..Plugin import Plugin
from .CanCreateText import CanCreateText
from bpy.types import Operator
import bpy


class CreateTextOperator(Operator, Plugin, CanCreateText):
    """Turn an empty object into font text object"""
    bl_idname = "object.font_create_text"
    bl_label = "Create Text"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.create_text()
        return {'FINISHED'}

    def create_text(self):
        o = bpy.context.object
        if o.type != "EMPTY" or o.empty_display_type != "PLAIN_AXES":
            return
        if not 'font_text' in o:
            o['font_text'] = ""
        if not 'font_text_start_frame' in o:
            o['font_text_start_frame'] = 0
        if not 'font_text_line_width' in o:
            o['font_text_line_width'] = 25
        if not 'font_text_character_spacing' in o:
            o['font_text_character_spacing'] = 10
        if not 'font_text_top_line_location' in o:
            o['font_text_top_line_location'] = 0
        if not 'font_text_bottom_line_location' in o:
            o['font_text_bottom_line_location'] = -17
        if not 'font_text_word_based_frame' in o:
            o['font_text_word_based_frame'] = True
        if not 'font_text_use_current_frame_as_start' in o:
            o['font_text_use_current_frame_as_start'] = True
        if not 'font_text_end' in o:
            text_end = {
                'type': "OFFSET",
                'end_frame': 0,
                'length': 1,
                'end_offset': 0
            }  # type: bpy.TextEndType
            o['font_text_end'] = text_end
        return