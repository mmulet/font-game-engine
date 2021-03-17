
import bpy


def remove_keyframes(o, data_path, index=None):
    # type: (bpy.types.Object, bpy.types.Known_Data_Path, bpy.Optional[int]) -> None
    if o.animation_data is None:
        return
    if o.animation_data.action is None:
        return
    if o.animation_data.action.fcurves is None:
        return
    fcurves = o.animation_data.action.fcurves
    if index is not None:
        fcurve = fcurves.find(data_path, index=index)
        if fcurve is None:
            return
        fcurves.remove(fcurve)
        return
    # index is none, so remove all indices
    for fcurve in fcurves:
        if fcurve.data_path != data_path:
            continue
        fcurves.remove(fcurve)
