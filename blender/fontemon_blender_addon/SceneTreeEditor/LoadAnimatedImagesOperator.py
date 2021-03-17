
from .get_or_make_animation_pattern import get_or_make_animation_pattern
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
# from bpy.props import StringProperty
from .multiple_image_objects import multiple_image_objects
from ..Common import get_image_data_block, image_object
from .evaluate_pattern import evaluate_pattern, PatternError
from .get_image_name_from_pattern import get_image_name_from_pattern


class LoadAnimatedImagesOperator(Operator, Plugin):
    """Load multiple images given a pattern. Use it to load several frames of an animation at once"""
    bl_idname = "font.loadanimatedimages"
    bl_label = "Load animated images"
    bl_options = {'UNDO'}

    # pattern: StringProperty(
    #     name="start_object_name",
    #     description="A python expression to return the filename given the index i"
    # )

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.load_animated_images(context)
        return {'FINISHED'}

    def get_image_name_from_pattern(self, i, pattern):
        # type: (int, bpy.AnimationPatternInfoType) -> bpy.Optional[str]
        type = pattern["type"]
        if type == "PYTHON":
            try:
                return evaluate_pattern(i, pattern["python"])
            except PatternError as e:
                self.report(
                    {'ERROR'}, f"Error while running your pattern on i={e.i}. Try your pattern out in the blender script editor.")
                return None
        return get_image_name_from_pattern(i, type, pattern)

    def load_animated_images(self, context):
        # type: (bpy.ContextType) -> None

        active_object = image_object(context.active_object)
        if active_object is None:
            return

        objects = multiple_image_objects(context)
        if objects is None:
            return
        objects.sort(key=lambda o: o.name)
        pattern_info = get_or_make_animation_pattern(active_object)

        for i in range(len(objects)):
            image_name = self.get_image_name_from_pattern(i, pattern_info)
            if image_name is None:
                return
            objects[i].data = get_image_data_block(image_name)
        for o in objects:
            o["font_animation_pattern_info"] = pattern_info
