from .SizePanel import SizePanel
from .DontSizeMePanel import DontSizeMePanel
from .remove_keyframes import remove_keyframes
from ..Common import image_object
import bpy
from bpy.app.handlers import persistent
from ..Plugin import MultiplePluginHolder
from math import radians


def size_images_in_context():
    # type: () -> float | None
    props = bpy.context.window_manager.size_props
    if not props.global_enable:
        return props.poll_every_seconds

    for area in bpy.context.screen.areas:
        if area.type == "NODE_EDITOR":
            node_space = area.spaces[0]
            if props.keep_sidebar_on_at_all_times:
                node_space.show_region_ui = True
            continue
        if area.type != "VIEW_3D":
            continue
        space = area.spaces[0]
        if props.lock_viewport_to_camera:
            space.region_3d.view_perspective = "CAMERA"
        if props.keep_sidebar_on_at_all_times:
            space.show_region_ui = True
    camera = bpy.context.scene.camera
    if camera is None and props.regenerate_deleted_camera:
        new_camera = bpy.data.cameras.new("Camera")
        new_camera.type = "ORTHO"
        new_camera.ortho_scale = 250.0
        camera = bpy.data.objects.new(name="Camera", object_data=new_camera)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(
            camera)
        bpy.context.scene.camera = camera
    if props.lock_camera_position and camera is not None:
        camera.location[0] = 125
        camera.location[1] = -2
        camera.location[2] = -125
        camera.rotation_euler[0] = radians(90)
        camera.rotation_euler[1] = 0
        camera.rotation_euler[2] = 0
        camera.scale[0] = 1.0
        camera.scale[1] = 1.0
        camera.scale[2] = 1.0
        remove_keyframes(camera, "rotation_euler")
        remove_keyframes(camera, "location")
        remove_keyframes(camera, "scale")

    for o in bpy.context.scene.objects:

        image_o = image_object(o)
        if image_o is None:
            continue

        if 'font_dont_size_me' in image_o and image_o['font_dont_size_me']:
            continue

        # data should be the image that the empty image displays
        if props.size_images:
            remove_keyframes(image_o, "empty_display_size")
            size = image_o.data.size
            longest_side = max(size[0], size[1])
            # 1.2075 found by trial and error
            image_o.empty_display_size = longest_side * 1.2075
        if props.reset_image_offset:
            remove_keyframes(image_o, "empty_image_offset")
            image_o.empty_image_offset[0] = 0.0
            image_o.empty_image_offset[1] = -1.0

        # if image_o.parent is None:
        if props.reset_image_y_location:
            remove_keyframes(image_o, "location", 1)
            image_o.location[1] = 0
        if props.lock_image_scale:
            remove_keyframes(image_o, "scale")
            image_o.scale[0] = 1.0
            image_o.scale[1] = 1.0
            image_o.scale[2] = 1.0
            image_o.lock_scale[0] = True
            image_o.lock_scale[1] = True
            image_o.lock_scale[2] = True
        if props.lock_image_rotation:
            remove_keyframes(image_o, "rotation_euler")
            image_o.rotation_euler[0] = radians(90)
            image_o.rotation_euler[1] = 0
            image_o.rotation_euler[2] = 0
            image_o.lock_rotation[0] = True
            image_o.lock_rotation[1] = True
            image_o.lock_rotation[2] = True
    return props.poll_every_seconds


@persistent
def after_load(_):
    # type: (bpy.Any) -> None
    if not (bpy.app.timers.is_registered(size_images_in_context)):
        bpy.app.timers.register(size_images_in_context)


class SizeImagesInContext:
    @classmethod
    def plug_in(cls):
        bpy.app.handlers.load_post.append(after_load)
        # run this now, so that everything will work
        # immediately after installing the addon
        after_load(False)

    @classmethod
    def plug_out(cls):
        bpy.app.handlers.load_post.remove(after_load)
        if bpy.app.timers.is_registered(size_images_in_context):
            bpy.app.timers.unregister(size_images_in_context)


class SizeImage(MultiplePluginHolder):
    plugins = (DontSizeMePanel, SizePanel, SizeImagesInContext)
