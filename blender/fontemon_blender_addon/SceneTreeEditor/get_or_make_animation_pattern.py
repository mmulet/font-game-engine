import bpy


def create_new_animation_pattern_info():
    # type: () -> bpy.AnimationPatternInfoType
    temp = {
        "type": "INCREMENT",
        "num_digits": 2,
        "start_number": 0,
        "end_number": 1,
        "wrap_around": True,
        "pattern": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        "pattern_size": 2,
        "python": "",
        "extension": ".png",
        "filename": ""
    }  # type: bpy.AnimationPatternInfoType
    return temp


fake_info = create_new_animation_pattern_info()


def get_animation_pattern_or_fake(o):
    # type: (bpy.EmptyImageObjectTypeWithData) -> bpy.AnimationPatternInfoType
    if "font_animation_pattern_info" in o:
        return o["font_animation_pattern_info"]
    return fake_info


def get_or_make_animation_pattern(o):
    # type: (bpy.EmptyImageObjectTypeWithData) -> bpy.AnimationPatternInfoType
    if "font_animation_pattern_info" in o:
        return o["font_animation_pattern_info"]
    o["font_animation_pattern_info"] = create_new_animation_pattern_info()
    return o["font_animation_pattern_info"]
