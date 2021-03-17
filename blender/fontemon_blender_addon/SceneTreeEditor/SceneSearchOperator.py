
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from .view_nodes import view_nodes
from .nodes_from_context import nodes_from_context
from .is_a_scene_node import is_a_scene_node


class SceneSearchOperator(Operator, Plugin):
    '''Search for a scene node with a specific scene'''
    bl_idname = "font.scenesearch"
    bl_label = "Search For Scene"
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = "node_item"
    # see https://docs.blender.org/api/current/bpy.props.html?highlight=enumproperty#bpy.props.EnumProperty
    # There is a known bug with using a callback, Python must keep a reference to the strings returned by the callback or Blender will misbehave or even crash.
    _enum_item_hack = []  # type: list[bpy.EnumPropertyItem]

    # Create an enum list from node items
    def node_enum_items(self, context):
        # type: (bpy.Optional[bpy.ContextType]) -> list[bpy.EnumPropertyItem]
        enum_items = SceneSearchOperator._enum_item_hack
        enum_items.clear()
        nodes = nodes_from_context(context)
        if nodes is None:
            return []
        all_scenes = set()  # type: set[str]
        selected_scenes = set()  # type: set[str]
        for item in nodes:
            node = is_a_scene_node(item)
            if node is None:
                continue
            if node.node_scene is None:
                continue
            all_scenes.add(node.node_scene.name)
            if item.select:
                selected_scenes.add(node.node_scene.name)
        scenes = selected_scenes if len(selected_scenes) > 0 else all_scenes
        for index, scene_name in enumerate(scenes):
            enum_items.append((scene_name, scene_name, "", index))
        return enum_items

    node_item: EnumProperty(
        name="Node Type",
        description="Node type",
        items=node_enum_items,
    )

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal['FINISHED', 'CANCELLED']]
        scene_name = self.node_item
        nodes = nodes_from_context(context)
        if nodes is None:
            self.report({'ERROR'}, "Could find any nodes")
            return {'CANCELLED'}
        all_found_nodes = []  # type: list[bpy.AllSceneNodeTypes]
        selected_found_nodes = []  # type: list[bpy.AllSceneNodeTypes]
        for item in nodes:
            node = is_a_scene_node(item)
            if (node is None or
                    node.node_scene is None or
                    node.node_scene.name != scene_name):
                continue
            all_found_nodes.append(node)
            if node.select:
                selected_found_nodes.append(node)
        found_nodes = selected_found_nodes if len(
            selected_found_nodes) > 0 else all_found_nodes
        if len(found_nodes) <= 0:
            self.report({'ERROR'}, "Could find any nodes with matching scene")
            return {'CANCELLED'}
        view_nodes(nodes, found_nodes)
        return {'FINISHED'}

    def invoke(self, context, event):
        # type: (bpy.ContextType, bpy.Any) -> set[bpy.Literal["CANCELLED"]]
        # Delayed execution in the search popup
        context.window_manager.invoke_search_popup(self)
        return {'CANCELLED'}
