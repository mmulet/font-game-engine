
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty
from .multiple_image_objects import multiple_image_objects


class MakeAnimationOperator(Operator, Plugin):
    """Set the visibility of several frames to make an animation"""
    bl_idname = "font.makeanimation"
    bl_label = "Make animation"
    bl_options = {'UNDO'}

    key_before: BoolProperty(
        name="Key before",
        description="Add a key, setting all frames to invisible, before the animation"
    )
    key_after: BoolProperty(
        name="Key After",
        description="Add a key, setting all frames to invisible, after the animation"
    )
    use_current_frame: BoolProperty(
        name="Use Current Frame",
        description="Use the current frame as the start of the animation"
    )
    frame_number: IntProperty(
        name="Frame Number",
        description="The frame number to start the animation"
    )
    repeat_times: IntProperty(
        name="Number of times",
        min=1,
        description="Play the animation this number of times. If you put 1, it will play once."
    )

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.makeAnimation(context)
        return {'FINISHED'}

    def makeAnimation(self, context):
        # type: (bpy.ContextType) -> None
        objects = multiple_image_objects(context)
        if objects is None:
            return
        objects.sort(key=lambda o: o.name)
        start_frame = (context.scene.frame_current
                       if self.use_current_frame
                       else self.frame_number)
        animation_length = len(objects)
        for o in objects:
            o.show_empty_image_orthographic = False
            o.keyframe_insert(
                "show_empty_image_orthographic", frame=start_frame - 1 if self.key_before else start_frame)
        for loop_index in range(self.repeat_times):
            for frame_index in range(len(objects)):
                frame = start_frame + frame_index + loop_index*animation_length
                o = objects[frame_index]
                o.show_empty_image_orthographic = True
                o.keyframe_insert("show_empty_image_orthographic", frame=frame)
                if (not self.key_after and
                    loop_index == (self.repeat_times - 1) and
                        frame_index == (animation_length - 1)):
                    continue
                o.show_empty_image_orthographic = False
                o.keyframe_insert(
                    "show_empty_image_orthographic", frame=frame + 1)
        for o in objects:
            o['font_animation_start_frame'] = start_frame
            o['font_animation_use_current_frame'] = False
            o['font_animation_key_before'] = self.key_before
            o['font_animation_key_after'] = self.key_after
            o['font_animation_repeat_times'] = self.repeat_times
