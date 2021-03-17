import bpy
from ..Common import has_all_text_attributes
from .EditTextError import EditTextError


def validate_options(o, number_of_frames, start_frame):
    # type: (bpy.EmptyTextType, int, int) -> None
    if not has_all_text_attributes(o):
        raise EditTextError(
            "Missing a property! Run Create text on this object!")
    end = o["font_text_end"]
    type = end["type"]
    if type == "END":
        end_frame = end["end_frame"]
        if end_frame <= start_frame:
            raise EditTextError(
                "End frame is less than or equal to start frame!")
        if (end_frame - start_frame + 1) < number_of_frames:
            raise EditTextError(
                f"""End frame is less than the length of the animation! 
    Should be {number_of_frames + start_frame} or higher but it is {end_frame}.
    Animation is {number_of_frames} long""")
        return  # return end_frame
    if type == "INFINITE":
        return
    if type == "LENGTH":
        length = end["length"]
        if length <= 0:
            raise EditTextError(
                f"Invalid text length, should be greater than or equal to 1, but it is {length}")
        if length < number_of_frames:
            raise EditTextError(
                f"Invalid text length, Length is less than the length of the animation.\nit is {length} but it needs to bye {number_of_frames} or greater.")
        return  # return start_frame + length
    if type == "OFFSET":
        offset = end["end_offset"]
        if offset < 0 and abs(offset) > number_of_frames:
            raise EditTextError(
                f"The offset should be greater than or equal to 0, it is {offset}")
        return  # return number_of_frames + offset - start_frame
    raise EditTextError(f"Unrecognized end type: {type} ")
