import bpy
from .get_fcurve import get_fcurve


def image_is_visible(o, frame):
    # type: (bpy.types.Object, int) -> bool
    fcurve = get_fcurve(o, "show_empty_image_orthographic")
    if fcurve is None:
        return o.show_empty_image_orthographic
    return fcurve.evaluate(frame=frame) > 0