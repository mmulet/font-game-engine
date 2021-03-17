
from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories
import bpy
from .scene_tree_space import scene_tree_space
from bpy.types import Menu

def menu_func_export(self, context):
    # type: (Menu, bpy.ContextType) -> None
    layout = self.layout
    props = layout.operator("node.add_node",
                            text="FirstSceneNode",
                            icon="TRIA_RIGHT")
    props.type = "FirstSceneNode"
    props.use_transform = True

    props = layout.operator("node.add_node",
                            text="SceneNode",
                            icon="SCENE_DATA")
    props.type = "SceneNode"
    props.use_transform = True

    props = layout.operator("node.add_node",
                            text="ConditionNode",
                            icon="SORTALPHA")
    props.type = "ConditionNode"
    props.use_transform = True

    props = layout.operator(
        "node.add_node",
        icon="DECORATE_DRIVER",
        text="GotoLostNode",
    )
    props.type = "GotoLostNode"
    props.use_transform = True

    props = layout.operator("node.add_node",
                            icon="TRIA_LEFT",
                            text="EndSceneNode")
    props.type = "EndSceneNode"
    props.use_transform = True


class SceneTreeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        return scene_tree_space(context.space_data) != None

    @classmethod
    def plug_in(cls):
        bpy.types.NODE_MT_add.append(menu_func_export)
        register_node_categories(
            'SCENE_TREE_NODES', node_categories)

    @classmethod
    def plug_out(cls):
        unregister_node_categories('SCENE_TREE_NODES')
        bpy.types.NODE_MT_add.remove(menu_func_export)


# all categories in a list
node_categories = [
    # identifier, label, items list
    SceneTreeCategory('SOMENODES', "All Nodes", items=[
        # our basic node
        NodeItem("FirstSceneNode"),
        NodeItem("SceneNode"),
        NodeItem("ConditionNode"),
        NodeItem("GotoLostNode"),
        NodeItem("EndSceneNode")
    ])
]
