import bpy


def get_image_number_from_pattern(i, type,  pattern):
    # type: (int, bpy.EasyAnimationPatternTypeType, bpy.AnimationPatternInfoType) -> int
    if type == "INCREMENT":
        difference = pattern["end_number"] - pattern["start_number"]
        if difference < 0:
            return 0
        k = i % (difference +
                 1) if pattern["wrap_around"] else i
        return k + pattern["start_number"]
    elif type == "DECREMENT":
        difference = pattern["start_number"] - pattern["end_number"]
        if difference < 0:
            return 0
        k = (i % (difference + 1)
             )if pattern["wrap_around"] else i
        return pattern["start_number"] - k
    elif type == "PATTERN":
        int_pattern = pattern["pattern"]
        return int_pattern[i % pattern["pattern_size"]]
    return 0


def get_image_name_from_pattern(i, type, pattern):
    # type: (int, bpy.EasyAnimationPatternTypeType, bpy.AnimationPatternInfoType) -> str
    number = get_image_number_from_pattern(i, type, pattern)
    return f"{pattern['filename']}{str(number).zfill(pattern['num_digits'])}{pattern['extension']}"
