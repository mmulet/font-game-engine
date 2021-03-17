 
import bpy

def has_all_text_attributes(o):
    # type: (bpy.EmptyTextType) -> bool
    if not ('font_text' in o and
            'font_text_start_frame' in o and
            'font_text_line_width' in o and
            'font_text_character_spacing' in o and
            'font_text_top_line_location' in o and
            'font_text_end' in o and
            'font_text_use_current_frame_as_start' in o and
            'font_text_bottom_line_location' in o and
            'font_text_word_based_frame' in o):
            return False
    end = o['font_text_end']
    if not ('type' in end and
        'end_frame' in end and
        'length' in end and
        'end_offset' in end):
        return False
    return True
