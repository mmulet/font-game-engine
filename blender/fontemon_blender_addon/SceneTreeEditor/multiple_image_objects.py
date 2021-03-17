import bpy
from ..Common import image_object

def multiple_image_objects(context):
    # type: (bpy.ContextType) -> bpy.Optional[list[bpy.EmptyImageObjectTypeWithData]]
    image_objects = []  # type: list[bpy.EmptyImageObjectTypeWithData]
    if context.selected_objects is None:
        return None
    for o in context.selected_objects:
        image_o = image_object(o)
        if image_o is None:
            # if any are not an image object then
            # quite
            return None
        image_objects.append(image_o)
    if len(image_objects) < 2:
        return None
    return image_objects
