
from .EditTextError import EditTextError
from ..Common import get_image_data_block
from math import pi
import bpy
from random import randint
from typing import cast, List

class NewObjectWordInfo:
    def __init__(self, word_id, ascii_word, position):
        # type: (int, str, list[float]) -> None
        self.word_id = word_id
        self.ascii_word = ascii_word
        self.position = position


def setup_text_objects(context, o, lines, linesType, start_frame):
    # type: (bpy.ContextType, bpy.EmptyTextType, list[list[bpy.WordInfo]] | list[list[str]], bpy.Literal["Word"] | bpy.Literal["Character"], int ) -> None
    view_layer = context.view_layer
    character_spacing_x = 10 if o['font_text_word_based_frame'] else o['font_text_character_spacing']
    top_line_y_location = o['font_text_top_line_location']
    bottom_line_y_location = o['font_text_bottom_line_location']

    invisible_keyframe = -1 if start_frame >= 0 else start_frame - 1

    
    line_state = "first_line" # type: bpy.Literal["first_line"] | bpy.Literal["second_line"] | bpy.Literal["other_line"]
    top_line = []  # type: list[bpy.EmptyImageObjectType]
    bottom_line = []  # type: list[bpy.EmptyImageObjectType]
    current_frame = start_frame

    def line_state_to_y_location(line_state):
        # type: (bpy.Literal["first_line"] | bpy.Literal["second_line"] | bpy.Literal["other_line"]) -> float
        return (top_line_y_location if
                line_state == "first_line" else
                bottom_line_y_location)

    def character_index_to_x_location(character_index):
        # type: (int) -> float
        return character_index*character_spacing_x

    def create_new_object(imageName, xLocation, yLocation, word_info=None):
        # type: (str, float,float, NewObjectWordInfo | None) -> bpy.EmptyImageObjectType
        new_object = bpy.data.objects.new(
            name=imageName, object_data=None)
        new_object.data = get_image_data_block(imageName)
        view_layer.active_layer_collection.collection.objects.link(
            new_object)
        new_object.rotation_euler[0] = pi/2
        new_object.parent = o
        new_object.empty_display_type = "IMAGE"
        new_object.show_empty_image_orthographic = False
        new_object.keyframe_insert(
            "show_empty_image_orthographic", frame=invisible_keyframe)
        new_object.location = [
            xLocation, 0, yLocation]
        new_object.keyframe_insert("location", frame=invisible_keyframe)

        new_object.show_empty_image_orthographic = True
        new_object.keyframe_insert(
            "show_empty_image_orthographic", frame=current_frame)
        if word_info is not None:
            new_object["font_word_id"] = word_info.word_id
            new_object["font_word"] = word_info.ascii_word
            new_object["font_word_position"] = word_info.position
        return new_object

    for line in lines:
        this_line = []  # type: list[bpy.EmptyImageObjectType]
        # Make the whole line above dissapear
        if line_state == "other_line":
            for object in top_line:
                object.show_empty_image_orthographic = False
                object.keyframe_insert(
                    "show_empty_image_orthographic", frame=current_frame)
            for object in bottom_line:
                object.keyframe_insert("location", frame=current_frame - 1)
                object.location[2] = top_line_y_location
                object.keyframe_insert("location", frame=current_frame)
            # current_frame += 1
            top_line = bottom_line
        character_index = 0
        if linesType == "Word":
            a = line  # type: bpy.Any
            word_list = a  # type: list[bpy.WordInfo]
            y_position = line_state_to_y_location(line_state=line_state)
            for word_info in word_list:
                list_of_image_names = word_info["word"]
                new_object_word_info = NewObjectWordInfo(
                    word_id=randint(0, 10000000),
                    ascii_word=word_info["ascii_word"],
                    position=[
                        character_index_to_x_location(character_index),
                        y_position
                    ]
                )
                for imageName in list_of_image_names:
                    if imageName == "space":
                        character_index += 1
                        continue
                    this_line.append(create_new_object(
                        imageName,
                        xLocation=character_index_to_x_location(
                            character_index),
                        yLocation=y_position,
                        word_info=new_object_word_info
                    ))
                    character_index += 1
                # advance the character index to make a "space" character
                character_index += 1
                current_frame += 1
        elif linesType == "Character":
            characters = cast(List[str], line)
            y_position = line_state_to_y_location(line_state=line_state)
            for imageName in characters:
                if imageName == "space":
                    character_index += 1
                    continue
                this_line.append(create_new_object(
                    imageName,
                    xLocation=character_index_to_x_location(character_index),
                    yLocation=y_position))
                character_index += 1
                current_frame += 1

        if line_state == "first_line":
            line_state = "second_line"
            top_line = this_line
            bottom_line = []
            continue
        if line_state == "second_line":
            line_state = "other_line"
            top_line = top_line
            bottom_line = this_line
            continue
        top_line = bottom_line
        bottom_line = this_line

    end_frame = get_end_frame(o["font_text_end"], current_frame, start_frame)
    if end_frame is not None:
        for object in top_line:
            object.show_empty_image_orthographic = False
            object.keyframe_insert(
                "show_empty_image_orthographic", frame=end_frame)
        for object in bottom_line:
            object.show_empty_image_orthographic = False
            object.keyframe_insert(
                "show_empty_image_orthographic", frame=end_frame)


def get_end_frame(text_end, current_frame, start_frame):
    # type: (bpy.TextEndType, int, int) -> bpy.Optional[int]
    type = text_end["type"]
    if type == "INFINITE":
        return None
    if type == "END":
        return text_end["end_frame"]
    if type == "OFFSET":
        return current_frame + text_end["end_offset"]
    if type == "LENGTH":
        length = text_end["length"]
        return start_frame + length
    raise EditTextError(f"Unrecognized end type {type}")
