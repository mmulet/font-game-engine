from ..Plugin import Plugin
import bpy
from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from ..Common import ToolPanel, ViewPanel, ItemsPanel


def draw_add_node_panel(layout, context, at_cursor):
    # type: (bpy.types.UILayout, bpy.ContextType, bool) -> None
    
    props = layout.operator("font.add_node_at_center",
                            text="FirstSceneNode",
                            icon="TRIA_RIGHT")
    props.type = "FirstSceneNode"
    props.use_transform = True

    props = layout.operator("font.add_node_at_center",
                            text="SceneNode",
                            icon="SCENE_DATA")
    props.type = "SceneNode"
    props.use_transform = True

    props = layout.operator("font.add_node_at_center",
                            text="ConditionNode",
                            icon="SORTALPHA")
    props.type = "ConditionNode"
    props.use_transform = True

    props = layout.operator(
        "font.add_node_at_center",
        icon="DECORATE_DRIVER",
        text="GotoLostNode",
    )
    props.type = "GotoLostNode"
    props.use_transform = True

    props = layout.operator("font.add_node_at_center",
                            icon="TRIA_LEFT",
                            text="EndSceneNode")
    props.type = "EndSceneNode"
    props.use_transform = True


class AddNodePanel(Panel, ToolPanel):
    """Add Node"""
    bl_label = "Add Node"
    bl_idname = "OBJECT_PT_add_node_panel_tool"
    bl_space_type = 'NODE_EDITOR'

    @classmethod
    def plug_in(cls):
        register_class(cls)
        AddNodeView.plug_in()
        AddNodeItem.plug_in()

    @classmethod
    def plug_out(cls):
        AddNodeItem.plug_out()
        AddNodeView.plug_out()
        unregister_class(cls)

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_add_node_panel(self.layout, context, at_cursor=False)


class AddNodeView(Panel, Plugin, ViewPanel):
    """Add Node"""
    bl_label = "Add Node"
    bl_idname = "OBJECT_PT_add_node_panel_view"
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_add_node_panel(self.layout, context, at_cursor=False)


class AddNodeItem(Panel, Plugin, ItemsPanel):
    """Add Node"""
    bl_label = "Add Node"
    bl_idname = "OBJECT_PT_add_node_panel_item"
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        # type: (bpy.ContextType) -> None
        draw_add_node_panel(self.layout, context, at_cursor=False)
