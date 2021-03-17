import bpy
from ..Common import image_object, text_object
from .image_is_visible import image_is_visible


def get_scene_script(scene):
    # type: (bpy.types.Scene) -> bpy.SceneScriptType
    word_images = [o for o in [image_object(
        o) for o in scene.objects] if o is not None and "font_word_id" in o]

    texts = {}  # type: dict[str, bpy.SceneScriptInfo]
    for frame in range(scene.frame_start, scene.frame_end + 1, scene.frame_step):
        visible_words = [
            o for o in word_images if image_is_visible(o, frame=frame)]
        for o in visible_words:
            parent = o.parent
            if parent is None:
                raise Exception(
                    f"Word {o['font_word']} {o['font_word_id']} does not have a parent, so can't find a location for it.\nObject: {o.name}\nScene: {scene.name}")
            if parent.name in texts:
                continue
            text_o = text_object(parent)
            if text_o is None:
                raise Exception(
                    f"Word {o['font_word']} {o['font_word_id']} parent is not a text object, .\nObject: {o.name}\n Parent: {parent.name}\nScene: {scene.name}")
            # Can't just pass end info in directly
            # because blender adds properties to it
            # that make it un-serializeable
            end_info = text_o["font_text_end"]
            texts[parent.name] = {
                "text": text_o["font_text"],
                "start_frame": text_o["font_text_start_frame"],
                "end": {
                    'type': end_info['type'],
                    'end_frame': end_info['end_frame'],
                    'length': end_info['length'],
                    'end_offset': end_info['end_offset']
                }
            }
    return {'texts':  sorted(list(texts.values()), key=lambda i: i['start_frame'])}
