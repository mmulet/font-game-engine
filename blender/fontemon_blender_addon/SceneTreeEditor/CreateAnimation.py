
from ..Plugin import Plugin
from bpy.types import Operator
import bpy


class CreateAnimation(Operator, Plugin):
    """CreateAnAnimation"""
    bl_idname = "font.add_font_animation"
    bl_label = "Add Font Image Animation"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.create_animation(context)
        return {'FINISHED'}

    def create_animation(self, context):
        # type: (bpy.ContextType) -> None
        image = (
            bpy.data.images['fake_animation_image']
            if 'fake_animation_image' in bpy.data.images
            else bpy.data.images.new(
                'fake_animation_image', 1, 1)
        )
        parent_object = bpy.data.objects.new(
            name="Animation",
            object_data=None
        )
        children = list(map(lambda i: bpy.data.objects.new(
            name="Animation",
            object_data=None
        ), range(2)))

        objects = [parent_object, *children]
        for o in objects:
            context.view_layer.active_layer_collection.collection.objects.link(
                o)
        for o in children:
            o.data = image
            o.empty_display_type  = "IMAGE"
            o.parent = parent_object

        for o in context.selected_objects:
            o.select_set(False)
        for o in children:
            o.select_set(True)
        
        context.view_layer.objects.active = children[0]
