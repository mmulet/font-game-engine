

from .get_slot_info import get_slot_info
import bpy
from bpy.path import basename
from .get_fcurve import get_fcurve
from .image_is_visible import image_is_visible
from ..Common import image_object
from .missingDingNoSprite import missingDingNoSprite


class SceneFramesError(Exception):
    """What goes wrong during Scene Frames """

    def __init__(self, message):
        # type: (str) -> None
        self.message = message
        Exception.__init__(self, message)


def get_scene_frames(scene):
    # type: (bpy.types.Scene) -> bpy.SceneInfoType
    """Go through each frame one by one and 
    find the position and visibility of each sprite"""

    empty_images = [o for o in
                    [image_object(
                        o) for o in scene.objects]
                    if (o is not None and
                        not ('font_disable_export' in o and o['font_disable_export']))]
    out = []  # type: "list[bpy.FrameInfo]"
    highest_slot = 0  # type: int
    found_slots = set()  # type: set[int]

    for frame in range(scene.frame_start, scene.frame_end + 1, scene.frame_step):
        # using show_empty_image_orthographic instead of visibility
        # because visibility makes editing keyframes
        # very hard.
        # Edit show_empty_image_orthographic in
        # Properties > Object Data Properties > Empty > Show in > Orthographic
        # make sure you set it as a keyframe

        visible_images = [
            o for o in empty_images if image_is_visible(o, frame=frame)]

        # a frame can only position a maximum of 64 images
        # old warning we can have as many images as
        # we want now
        # if len(visible_images) > 64:
        #     raise SceneFramesError(
        #         f"Too many images in a frame #{frame}. Maximum is 64 but found {len(visible_images)} images")

        words = {}  # type: dict[int,bpy.SpriteWordInfo]
        sprites = {}  # type: bpy.SpriteList
        slots = {}  # type: bpy.SlotList

        for empty_image_o in visible_images:
            x, y = get_location(empty_image_o, frame=frame)
            if "font_word_id" in empty_image_o:
                word = empty_image_o["font_word"]
                if len(word) != 1:
                    word_id = empty_image_o["font_word_id"]
                    if word_id in words:
                        # already handled this word
                        continue
                    parent = empty_image_o.parent
                    if parent is None:
                        raise Exception(
                            f"Word {word} {word_id} does not have a parent, so can't find a location for it.\nObject: {empty_image_o.name}\nScene: {scene.name}")
                    word_position = empty_image_o["font_word_position"]
                    x_location = _get_location(
                        parent, frame=frame, accum=(word_position[0], 0))
                    # TODO This rely's on the assumption that all words are the same y position
                    words[word_id] = {"word": word, "x": x_location[0], "y": y}
                    continue
                # not really a word because there is only
                # one char. It's more of a sprite
                # so let's add it to sprites instead

            position = {'x': fea_position(x),
                        'y': fea_position(y)}  # type: bpy.FrameInfoPosition
            slot_info = get_slot_info(empty_image_o)
            if slot_info is not None:
                highest_slot = max(slot_info.number, highest_slot)
                found_slots.add(slot_info.number)
                key = f"slot{slot_info.number}"
                positions = slots.setdefault(str(slot_info.number), [])
                positions.append(position)
                continue
            key = (basename(empty_image_o.data.filepath)
                   if not empty_image_o.name.startswith(
                "MissingDingNo")
                else missingDingNoSprite())
            positions = sprites.setdefault(key, [])
            positions.append(position)

        out_words = {}  # type: bpy.SpriteList
        for word_info in words.values():
            positions = out_words.setdefault(word_info["word"], [])
            positions.append({
                "x": fea_position(word_info["x"]),
                "y": fea_position(word_info["y"])
            })
        out_info = {
            "sprites": sprites,
        }  # type: bpy.FrameInfoBaked
        if len(words) > 0:
            out_info["words"] = out_words
        if len(slots) > 0:
            out_info["slots"] = slots
        out.append(
            out_info
        )
    number_of_slots = len(found_slots)
    if number_of_slots > 0 and number_of_slots < (highest_slot + 1):
        raise SceneFramesError(
            f"Missing slot!. Go to slot number #{highest_slot} but there are only {number_of_slots} used. All found slots: ${found_slots}")
    return {'frames': out, 'slots': number_of_slots}


def fea_position(x):
    # type: (float) -> int
    return round(x*10)


def get_location_may_be_local(o, frame, type):
    # type: (bpy.types.Object, int, bpy.Literal["x"] | bpy.Literal["z"]) -> float
    index = 0 if type == "x" else 2
    fcurve = get_fcurve(o, "location", index)
    if fcurve is None:
        return o.location[index]
    return fcurve.evaluate(frame=frame)


def get_location(o, frame):
    # type: (bpy.types.Object, int) -> bpy.Tuple[float,float]
    return _get_location(o, frame, (0, 0))


def _get_location(o, frame, accum):
    # type: (bpy.types.Object, int, bpy.Tuple[float,float]) -> bpy.Tuple[float,float]
    parent_translation = ([0, 0, 0]
                          if o.parent is None
                          else o.matrix_parent_inverse.to_translation())
    # Not a typo. Parent translation ix [X,Z,Y]
    # but most things are [X,Y,Z] and I have no idea why
    maybeZ = parent_translation[1]
    maybeZ2 = parent_translation[2]

    newValue = (accum[0] + parent_translation[0] + get_location_may_be_local(o, frame=frame, type="x"),
                accum[1] + (maybeZ2 if abs(maybeZ2) > abs(maybeZ) else maybeZ) + get_location_may_be_local(o, frame=frame, type="z"))

    if o.parent is None:
        return newValue
    return _get_location(o.parent, frame=frame, accum=newValue)
