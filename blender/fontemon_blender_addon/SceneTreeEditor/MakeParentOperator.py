
from ..Plugin import Plugin
from bpy.types import Operator
import bpy
from .multiple_image_objects import multiple_image_objects
from re import compile

without_num = compile(r"(.+?)\.?\d+$")


class MakeParentOperator(Operator, Plugin):
    """Groups a bunch of objects under a common parent"""
    bl_idname = "font.make_parent"
    bl_label = "Add a parent object"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]

        self.make_parent(context)
        return {'FINISHED'}

    def make_parent(self, context):
        # type: (bpy.ContextType) -> None
        objects = multiple_image_objects(context)
        if objects is None:
            return

        names = set()  # type: set[str]
        for o in objects:
            if o.parent is not None:
                self.report(
                    {'ERROR'}, f"Could not make parent {o.name} already has a parent!")
                return
            match = without_num.search(o.name)
            names.add(o.name if match is None else match[1])
        parent = bpy.data.objects.new(
            name=" and ".join(names),
            object_data=None
        )
        context.view_layer.active_layer_collection.collection.objects.link(
            parent)
        first_object = objects[0]
        parent.location[0] = first_object.location[0]
        parent.location[2] = first_object.location[2]
        parent.select_set(True)
        context.view_layer.objects.active = parent
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)