import bpy

def get_fcurve(o, data_path, index=0):
    # type: (bpy.types.Object, bpy.types.Known_Data_Path, int) -> bpy.Optional[bpy.types.FCurve]
    if (o.animation_data is None or
        o.animation_data.action is None or
            o.animation_data.action.fcurves is None):
        return None
    return o.animation_data.action.fcurves.find(data_path=data_path, index=index)