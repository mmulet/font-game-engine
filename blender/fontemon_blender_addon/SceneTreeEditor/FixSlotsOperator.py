
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from ..Common import image_object
from .get_slot_info import get_slot_info
from .scene_tree_space import scene_tree_space

def _get_parent_name(o, n):
    # type: (bpy.types.Object, list[str]) -> str
    p = o.parent
    if p is None:
        return " -> ".join(n)
    n.append(p.name)
    return _get_parent_name(p, n)


def get_parent_name(o):
    # type: (bpy.types.Object) -> str
    return _get_parent_name(o, [])


class FixSlotsOperator(Operator, Plugin):
    """Generate a node graph to fix slots"""
    bl_idname = "font.generatefixslots"
    bl_label = "Make Slots Node Tree"

    node_scene_name: StringProperty(name="Scene Name")

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.fix_slots(context)
        return {'FINISHED'}

    def fix_slots(self, context):
        # type: (bpy.ContextType) -> None
        if not self.node_scene_name:
            return
        
        space = scene_tree_space(context.space_data)
        if space is None:
            return
        node_tree = space.node_tree
        slot_scene_node = node_tree.nodes.new("SlotSceneNode")
        slot_scene_node.select = True
        x_position = space.cursor_location[0]
        y_position = space.cursor_location[1] - 300

        slot_scene_node.location = [x_position, y_position]
        y_position += 300
        scene = bpy.data.scenes[self.node_scene_name]
        slot_scene_node.node_scene = scene
        slot_objects = {}  # type: dict[int,bpy.SlotObjectsList]
        for o in scene.objects:
            image_o = image_object(o)
            if image_o is None:
                continue
            slot_info = get_slot_info(image_o)
            if slot_info is None:
                continue
            objects_with_this_slot = slot_objects.setdefault(
                slot_info.number, {"names": set(), "objects": []})
            objects_with_this_slot["objects"].append(image_o)
            objects_with_this_slot["names"].add(slot_info.name)

        for slot_number, info in sorted(slot_objects.items()):
            slot_node = space.node_tree.nodes.new("SlotNode")
            slot_node.slot_name = " and ".join(info["names"])
            slot_node.slot_number = slot_number
            new_location =  [x_position + 300, y_position] # type: list[float]
            slot_node.location = new_location
            slot_node.select = True
            slot_node.width = 250

            objects = info["objects"]

            for (i, o) in enumerate(objects):
                o_node = space.node_tree.nodes.new("SlotObjectNode")
                o_node.object = o
                o_node.parent_name = get_parent_name(o)
                o_node.width = 250
                if i > (len(slot_node.inputs) - 1):
                    _ = slot_node.inputs.new('SceneInputSocket', "Object")
                    slot_node.number_of_inputs += 1
                _ = node_tree.links.new(o_node.outputs[0], slot_node.inputs[i])
                _ = node_tree.links.new(
                    slot_scene_node.outputs[0], o_node.inputs[0])
                o_node.location = [x_position, y_position]
                slot_node.select = True

                y_position += -200
