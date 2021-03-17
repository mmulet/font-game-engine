from typing import Any, Callable, List, Literal, Optional,  Sequence, Tuple, overload
from bpy import (AddNodeOperatorType, AllObjectTypes, ContextType, AllNodeTypes, AllInputNodeTypes,
                 MakeAnimationOperatorType, NodeEditorArea, SelectSlotOperatorType,
                 AssignSlotsInPatternOperatorType,
                 JumpToSceneOperatorType, SlotNodeType, SlotObjectNodeType, SlotSceneNodeType, View3DArea)
from typing_extensions import Literal


class WorkSpaceTool:
    ...


class Panel:
    layout: UILayout


TOPBAR_MT_file_export: list[Callable[[
    Panel, ContextType], None]]


class Screen:
    areas: list[View3DArea | NodeEditorArea]


class Window:
    scene: Scene


class Image:
    size: list[float]
    filepath: str
    name: str


class Menu:
    layout: UILayout
    draw_preset: Any


class WindowManager:
    text_props: Any
    image_props: Any
    search_props: Any
    size_props: Any
    dontsize_props: Any
    converter_props: Any


class PropertyGroup:
    ...


class GenerateFixSlotOperatorType:
    node_scene_name: str


class AdjustSlotsOperatorType:
    node_name: str


class AddSlotBelowOperatorType:
    node_name: str


class AddSlotAboveOperatorType:
    node_name: str


class RemoveSlotNodeOperatorType:
    node_name: str


class ReplaceSlotImageOperatorType:
    only_selected_nodes: bool
    replace_image: str
    find_image: str

class RemoveParentObjectOperatorType:
    type: Literal["CLEAR_KEEP_TRANSFORM"]

class SelectHierarchyOperatorType:
    direction: Literal["CHILD"]
    extend: bool

class UILayout:

    def template_ID(self, data: Any, property: str, new: str=..., open: str=..., unlink: str=...) -> None: ...

    def row(self) -> UILayout: ...

    def box(self) -> UILayout: ...

    def prop_search(self, data: Any, property: str,
                    search_data: Any, search_property: str) -> None: ...

    @overload
    def operator(self, operator_bl_idname: Literal["object.select_hierarchy"],
                 text: str = ..., icon: str = ...) -> SelectHierarchyOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["object.parent_clear"],
                 text: str = ..., icon: str = ...) -> RemoveParentObjectOperatorType: ...
    @overload
    def operator(self, operator_bl_idname: Literal["font.add_node_at_center"],
                 text: str = ..., icon: str = ...) -> AddNodeOperatorType: ...
    @overload
    def operator(self, operator_bl_idname: Literal["node.add_node"],
                 text: str = ..., icon: str = ...) -> AddNodeOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.assignslotsinpattern"],
                 text: str = ..., icon: str = ...) -> AssignSlotsInPatternOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.replaceslotimage"],
                 text: str = ..., icon: str = ...) -> ReplaceSlotImageOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.removeslotnode"],
                 text: str = ..., icon: str = ...) -> RemoveSlotNodeOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.addslotabove"],
                 text: str = ..., icon: str = ...) -> AddSlotAboveOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.addslotbelow"],
                 text: str = ..., icon: str = ...) -> AddSlotBelowOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.adjustslots"],
                 text: str = ..., icon: str = ...) -> AdjustSlotsOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.generatefixslots"],
                 text: str = ..., icon: str = ...) -> GenerateFixSlotOperatorType: ...

    # @overload
    # def operator(self, operator_bl_idname: Literal["font.loadanimatedimages"],
    #              text: str = ..., icon: str = ...) -> LoadAnimatedImageOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.makeanimation"],
                 text: str = ..., icon: str = ...) -> MakeAnimationOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.selectslot"],
                 text: str = ..., icon: str = ...) -> SelectSlotOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: Literal["font.jumptoscene"],
                 text: str = ..., icon: str = ...) -> JumpToSceneOperatorType: ...

    @overload
    def operator(self, operator_bl_idname: str,
                 text: str = ..., icon: str = ...) -> Any: ...

    def menu(self, id: str) -> None: ...
    def label(self, *, text: str = ...) -> None: ...

    def prop(self, self_again: Any, prop_name: str,
             text: str = ...) -> str: ...


NODE_MT_editor_menus: list[Callable[[
    Menu, ContextType], None]]


class TestList(list[Callable[[
        Menu, ContextType], None]]):
    def prepend(self, bob: Callable[[
        Menu, ContextType], None]) -> None: ...


VIEW3D_MT_add: TestList
NODE_MT_add: TestList


class Keyframe:
    co: list[float]


class FCurveKeyframePoints(list[Keyframe]):
    pass


class FCurve:
    data_path: str
    keyframe_points: FCurveKeyframePoints
    def evaluate(self, frame: int) -> float: ...


Known_Data_Path = Literal["location",
                          "empty_image_offset",
                          "show_empty_image_orthographic",
                          "empty_display_size",
                          "scale",
                          "rotation_euler"
                          ]


class ActionFCurves(list[FCurve]):
    def find(self, data_path: Known_Data_Path,
             index: int = ...) -> Optional[FCurve]: ...


class Action:
    fcurves: Optional[ActionFCurves]


class AnimData:
    action: Optional[Action]


class Camera:
    type: Literal["PERSP", "ORTHO", "PANO"]
    ortho_scale: float


class Scene:
    objects: list[AllObjectTypes]
    name: str
    frame_current: int
    frame_start: int
    frame_end: int
    frame_step: int
    camera: Optional[Object]
    def frame_set(self, frame: int) -> None: ...


class Nodes(list[AllNodeTypes]):
    active: AllNodeTypes
    def __getitem__(
        self, key: str) -> AllNodeTypes: ...

    @overload
    def new(self, type: Literal["SlotObjectNode"]
            = ...) -> SlotObjectNodeType: ...

    @overload
    def new(self, type: Literal["SlotNode"]
            = ...) -> SlotNodeType: ...

    @overload
    def new(self, type: Literal["SlotSceneNode"]
            = ...) -> SlotSceneNodeType: ...

    @overload
    def new(self, type: str = ...) -> AllNodeTypes: ...


class ColorRampElement:
    color: Optional[list[float]]
    position: float


class ColorRamp:
    elements: list[ColorRampElement]
    def evaluate(self, position: float) -> list[float]: ...


class CompositorNodeValToRGB:
    bl_idname: Literal["CompositorNodeValToRGB"]
    color_ramp: ColorRamp


class NodeInputs(Sequence[NodeSocket]):
    def new(self, type: str, name: str) -> NodeSocket: ...
    def remove(self, socket: NodeSocket) -> None: ...


class NodeOutputs(Sequence[NodeSocket]):
    def new(self, type: str, name: str) -> NodeSocket: ...
    def remove(self, socket: NodeSocket) -> None: ...


class Node:
    inputs: NodeInputs
    outputs: NodeOutputs
    select: bool
    # two floats
    location: list[float]
    # a unique identifier
    name: str
    width: float
    height: float


class NodeLink:
    to_node: AllInputNodeTypes
    from_node: AllNodeTypes


class NodeLinks(list[NodeLink]):
    def new(self, input: NodeSocket, output: NodeSocket) -> NodeLink: ...
   


class NodeTree:
    bl_idname: str
    nodes: Nodes
    links: NodeLinks
    active: AllNodeTypes


class RegionView3D:
    view_perspective: Literal["PERSP", "ORTHO", "CAMERA"]


class SpaceNodeEditor:
    type: Literal["NODE_EDITOR"]
    show_region_ui: bool


class SpaceView3d:
    type: Literal["VIEW_3D"]
    region_3d: RegionView3D
    show_region_ui: bool


class Object:
    animation_data: Optional[AnimData]
    name: str
    empty_image_offset: list[float]
    empty_display_size: float
    children: list[AllObjectTypes]
    rotation_euler: list[float]
    location: list[float]
    scale: list[float]
    parent: Optional[AllObjectTypes]
    lock_scale: list[bool]
    lock_rotation: list[bool]
    show_empty_image_orthographic: bool
    # Inverse of object’s parent matrix at time of parenting
    # The key phrase here is "at time of parenting"
    # The matrix does not change between frames,
    # so you can use it to calculate the world position
    # at an arbitrary frame
    matrix_parent_inverse: MatrixArrayType

    def select_set(self, state: bool) -> None: ...

    def keyframe_delete(self, data_path: str, frame: float) -> None: ...
    def keyframe_insert(self, data_path: str, frame: int) -> None: ...


class MatrixArrayType:
    @classmethod
    def to_translation(cls) -> Tuple[float, float, float]: ...


class NodeSocket:
    links: list[NodeLink]
    is_linked: bool


class Operator:
    def report(self, type: set[Literal["ERROR", "INFO"]],
               message: str) -> None: ...


class CollectionObjects(Sequence[Object]):
    @classmethod
    def link(cls, o: AllObjectTypes) -> None: ...

    @classmethod
    def unlink(cls, o: AllObjectTypes) -> None: ...


class Collection:
    objects: CollectionObjects


class LayerCollection:
    collection: Collection


class LayerObjects(List[AllObjectTypes]):
    active: AllObjectTypes


class ViewLayer:
    active_layer_collection: LayerCollection
    objects: LayerObjects
