# pyright: reportUnusedImport=false

from typing import Any, Literal, NamedTuple, Optional,  Protocol, Sequence, Type, TypeVar, TypedDict, ValuesView,  overload, Callable, Tuple,

from typing_extensions import Literal
from . import types
from . import app
from . import data
from . import ops
from . import props
from . import utils
from . import context_test
# Context is technically a module too, but it gets passed around
# enough it's easier to type it as a variable
context: ContextType

# Types that I've added from https://docs.blender.org/api/2.91/index.html
# I've only added the types that I've used, as I've come accross them.
# The types are not complete, and may not even be completely accurate.
# Refer to the docs for the actual types

class SaveFileInput(TypedDict):
    # should be a base64 dataURL
    pngURL: str
    # JSON.stringify of a parse-bdf/CharStringWithoutInitialPosition
    charStringInfo: str
    # name without extension
    name: str

class ShouldReloadInput(TypedDict):
    export_number: int

class ShouldReloadOutput(TypedDict):
    should_reload: bool
    export_num: int

class NextImageInput(TypedDict):
    imageFilePath: str

class LoadImageInput(TypedDict):
    filePath: str


class Position(TypedDict):
    x: float
    y: float

class WordCharacterChar(Protocol):
    type: Literal["char"]
    char: str

class WordCharacterSpace(Protocol):
    type: Literal["space"]
    length: int

WordCharacter = WordCharacterChar | WordCharacterSpace

class CharStringWithoutInitialPosition(TypedDict):
    commands: str
    initialPosition: Position
    endPosition: Position

FrameNumber = int

FrameLookups = dict[FrameNumber, str]

NodeId = str

SceneName = str

GlyphId = str

NodeId_to_list_of_frame_blank_glyph_ID = dict[NodeId, list[GlyphId]]

FeatureName = Literal["game"] | Literal["dlig"]

ExportSceneType = Literal["first_scene"] | Literal["lost_scene"] | Literal[False]


class TextEndPropTypes:
    end_type: str


class FrameInfoPosition(TypedDict):
    x: float
    y: float


class FrameInfoPositionListable(Protocol):
    def values(self) -> ValuesView[list[FrameInfoPosition]]: ...

SpriteList: Type[dict[str, list[FrameInfoPosition]]]

SlotList: Type[dict[str, list[FrameInfoPosition]]]


class FrameInfoRequired(TypedDict):
    sprites: SpriteList


class FrameInfoBaked(FrameInfoRequired, total=False):
    words: SpriteList
    slots: SlotList


class SpriteWordInfo(TypedDict):
    word: str
    x: float
    y: float


FrameInfo = FrameInfoBaked


class WordInfo(TypedDict):
    word: list[str]
    ascii_word: str


# FrameInfo: Type[dict[str, list[FrameInfoPosition]]]


class ParserType(Protocol):
    def get_mightBeNewLine(self) -> bool: ...
    def set_mightBeNewLine(self, m: bool) -> Any: ...
    def addLine(self) -> Any: ...
    def addChar(self, ascii_character: str, char: str,
                width: int, skip_space: bool) -> Any: ...

    def shouldSkipDoubleNewline(self, width: int) -> Any: ...
    def currentLineIsEmpty(self) -> bool: ...
    def number_of_frames(self) -> int: ...


class Word:
    type: Literal["Word"] = "Word"

    def __init__(self, lines):
        # type: (list[list[list[str]]]) -> None
        self.lines = lines


class Character:
    type: Literal["Character"] = "Character"

    def __init__(self, lines) -> None:
        # type: (list[list[str]]) -> None
        self.lines = lines


LineType = Word | Character


class PluginType(Protocol):
    @classmethod
    def plug_in(cls) -> None: ...
    @classmethod
    def plug_out(cls) -> None: ...


class ConditionType(TypedDict):
    key: str
    node_id: NodeId


class SceneNodeInfoType(TypedDict):
    conditions: list[ConditionType]
    scene_name: str
    slots: list[str]


class SceneInfoType(TypedDict):
    frames: list[FrameInfo]
    slots: int


class SceneTreeOutputType(TypedDict):
    nodes: SceneNodeInfosType
    scenes: SceneInfosType

NodeGroupInputs = dict[NodeId, set[NodeId]]
class SceneScriptInfo(TypedDict):
    text: str
    start_frame: int
    end: TextEndType


class SceneScriptType(TypedDict):
    texts: list[SceneScriptInfo]


SceneNodeInfosType: Type[dict[NodeId, SceneNodeInfoType]]

SceneInfosType: Type[dict[SceneName, SceneInfoType]]

SceneScriptsType: Type[dict[SceneName, SceneScriptType]]


class ParsedCharacter(TypedDict):
    type: Literal["character"]
    image: str | Literal["space"]


ParsedResult = Optional[str | Literal["space"]]


class SceneTreeNodeInput:
    number_of_inputs: int
    inputs: types.NodeInputs


class NotEmptyObjectType(types.Object):
    """NOT a real type, only a stub"""
    type: Literal["SomethingElse"]


class EmptyObjectType(types.Object):
    type: Literal["EMPTY"]


TextEndTypeType = Literal["END", "LENGTH", "OFFSET", "INFINITE"]


class TextEndType(TypedDict):
    type: TextEndTypeType
    end_frame: int
    length: int
    end_offset: int


TextEndTypeFields = Literal["end_frame", "length", "end_offset"]

EmptyTextTypeBoolFields = Literal["font_text_word_based_frame",
                                  "font_text_use_current_frame_as_start"]

EmptyTextTypeStrFields = Literal["font_text"]

EmptyTextTypeIntFields = Literal["font_text_start_frame",
                                 "font_text_line_width",
                                 ]

EmptyTextTypeFloatFields = Literal["font_text_character_spacing",
                                   "font_text_top_line_location",
                                   "font_text_bottom_line_location"]

EmptyTextEndField = Literal["font_text_end"]


class EmptyTextType(EmptyObjectType):
    empty_display_type: Literal["PLAIN_AXES"]

    @overload
    def __getitem__(
        self, key: EmptyTextEndField) -> TextEndType: ...

    @overload
    def __getitem__(
        self, key: EmptyTextTypeStrFields) -> str: ...

    @overload
    def __getitem__(self, key: EmptyTextTypeIntFields) -> int: ...

    @overload
    def __getitem__(self, key: EmptyTextTypeFloatFields) -> float: ...

    @overload
    def __getitem__(
        self, key: EmptyTextTypeBoolFields) -> bool: ...

    @overload
    def __setitem__(
        self, key: EmptyTextTypeStrFields, value: str) -> None: ...

    @overload
    def __setitem__(self, key: EmptyTextTypeIntFields, value: int) -> None: ...

    @overload
    def __setitem__(self, key: EmptyTextTypeFloatFields,
                    value: float) -> None: ...

    @overload
    def __setitem__(self, key: EmptyTextTypeBoolFields,
                    value: bool) -> None: ...

    @overload
    def __setitem__(
        self, key: EmptyTextEndField, value: TextEndType) -> None: ...

    def __contains__(self, key: EmptyTextTypeStrFields |
                     EmptyTextTypeBoolFields |
                     EmptyTextTypeIntFields |
                     EmptyTextTypeFloatFields |
                     EmptyTextEndField
                     ) -> bool: ...


EmptyImageStrFields = Literal["font_word",
                              "font_slot_name",
                              ]

EmptyImageDontSizeMeFields = Literal["font_dont_size_me",
                                     "font_disable_export"]

EmptyImageBoolFields = EmptyImageDontSizeMeFields | Literal[
    "font_is_a_slot",
    "font_animation_use_current_frame",
    "font_animation_key_before",
    "font_animation_key_after",
]
EmptyImageIntFields = Literal["font_word_id",
                              "font_slot_number", 
                              "font_animation_start_frame",
                              "font_animation_repeat_times"
                              ]

EmptyImageValueFields = EmptyImageStrFields | EmptyImageBoolFields | EmptyImageIntFields

EmptyImageAnimationPatternInfoField = Literal["font_animation_pattern_info"]

EasyAnimationPatternTypeType = Literal["INCREMENT", "DECREMENT", "PATTERN"]

AnimationPatternTypeType = Literal["PYTHON"] | EasyAnimationPatternTypeType


AnimationPatternIntKeys = Literal[
    "num_digits",
    "start_number",
    "end_number",
    "pattern_size"
]

AnimationPatternBoolKeys = Literal["wrap_around"]
AnimationPatternStrKeys = Literal["python", "filename", "extension"]
AnimationPatternIntVectorKeys = Literal["pattern"]
AnimationPatternInfoKeys = Literal["type"] | AnimationPatternIntKeys | AnimationPatternBoolKeys | AnimationPatternStrKeys


class AnimationPatternInfoType(TypedDict):
    type: AnimationPatternTypeType
    num_digits: int
    start_number: int
    end_number: int
    wrap_around: bool
    pattern: list[int]
    pattern_size: int
    filename: str
    extension: str
    python: str


class CameraObjectType(types.Object):
    type: Literal["CAMERA"]
    data: types.Camera


class EmptyImageObjectType(EmptyObjectType):
    empty_display_type: Literal["IMAGE"]
    data: Optional[types.Image]

    @overload
    def __getitem__(
        self,
        key: EmptyImageAnimationPatternInfoField) -> AnimationPatternInfoType: ...

    @overload
    def __getitem__(
        self, key: EmptyImageBoolFields) -> bool: ...

    @overload
    def __getitem__(
        self, key: EmptyImageIntFields) -> int: ...

    @overload
    def __getitem__(
        self, key: Literal["font_word_position"]) -> list[float]: ...

    @overload
    def __getitem__(
        self, key: EmptyImageStrFields) -> str: ...

    @overload
    def __setitem__(
        self, key: EmptyImageBoolFields, value: bool) -> None: ...

    @overload
    def __setitem__(
        self, key: EmptyImageIntFields, value: int) -> None: ...

    @overload
    def __setitem__(
        self, key: EmptyImageStrFields, value: str) -> None: ...

    @overload
    def __setitem__(
        self, key: Literal["font_word_position"], value: list[float]) -> None: ...

    @overload
    def __setitem__(
        self, key: EmptyImageAnimationPatternInfoField,
        value: AnimationPatternInfoType) -> None: ...

    def __contains__(
        self, key: EmptyImageStrFields |
        EmptyImageBoolFields |
        EmptyImageIntFields |
        EmptyImageAnimationPatternInfoField |
        Literal[
            "font_word_position"]) -> bool: ...


class EmptyImageObjectTypeWithData(EmptyImageObjectType):
    data: types.Image


class NotImageEmptyObjectType(EmptyObjectType):
    """NOT a real type, only a stub"""
    empty_display_type: Literal["NotImage"]


ALLEmptyObjectTypes = EmptyImageObjectType | NotImageEmptyObjectType | EmptyTextType

AllObjectTypes = NotEmptyObjectType | ALLEmptyObjectTypes | CameraObjectType


class HasParent(Protocol):
    parent: Optional[AllObjectTypes]


class GotoLostNodeType(types.Node):
    bl_idname: Literal["GotoLostNode"]


class CommonSceneNodeType(types.Node):
    node_scene: Optional[types.Scene]
    number_of_slots: int
    node_slot1: Optional[types.Image]
    node_slot2: Optional[types.Image]
    node_slot3: Optional[types.Image]
    node_slot4: Optional[types.Image]
    node_slot5: Optional[types.Image]
    node_slot6: Optional[types.Image]
    node_slot7: Optional[types.Image]
    node_slot8: Optional[types.Image]
    node_slot9: Optional[types.Image]
    node_slot10: Optional[types.Image]
    node_slot11: Optional[types.Image]
    node_slot12: Optional[types.Image]
    node_slot13: Optional[types.Image]
    node_slot14: Optional[types.Image]
    node_slot15: Optional[types.Image]
    node_slot16: Optional[types.Image]
    node_slot17: Optional[types.Image]
    node_slot18: Optional[types.Image]
    node_slot19: Optional[types.Image]
    node_slot20: Optional[types.Image]


class OutputSceneNodeType(CommonSceneNodeType):
    outputs: list[types.NodeSocket]


class FirstSceneNodeType(OutputSceneNodeType):
    bl_idname: Literal["FirstSceneNode"]


class SceneNodeType(OutputSceneNodeType):
    bl_idname: Literal["SceneNode"]


class EndSceneNodeType(CommonSceneNodeType):
    bl_idname: Literal["EndSceneNode"]


class ConditionNodeType(types.Node):
    bl_idname: Literal["ConditionNode"]
    condition_key: Optional[str]
    outputs: list[types.NodeSocket]


class SlotSceneNodeType(types.Node):
    bl_idname: Literal["SlotSceneNode"]
    node_scene: types.Scene


class SlotObjectNodeType(types.Node):
    bl_idname: Literal['SlotObjectNode']
    object: types.Object
    parent_name: str


class SlotNodeType(types.Node):
    bl_idname: Literal['SlotNode']
    slot_number: int
    slot_name: str
    number_of_inputs: int


class SlotObjectsList(TypedDict):
    names: set[str]
    objects: list[EmptyImageObjectTypeWithData]


AllOutputSceneNodeTypes = FirstSceneNodeType | SceneNodeType
AllSceneNodeTypes = AllOutputSceneNodeTypes | EndSceneNodeType
# The nodes types a scene node can link to, ie, what the output of
# of a scene node can link to
AllInputNodeTypes = SceneNodeType | EndSceneNodeType | ConditionNodeType | GotoLostNodeType | SlotNodeType | SlotObjectNodeType
# The node types that a scene node can link to excluding ConditionNode
LinkedNodeTypes = SceneNodeType | EndSceneNodeType | GotoLostNodeType


SlotNodeTypes = SlotSceneNodeType | SlotObjectNodeType | SlotNodeType

AllInputSlotNodeTypes = SlotNodeType | SlotObjectNodeType

AllNodeTypes = AllSceneNodeTypes | ConditionNodeType | GotoLostNodeType | SlotNodeTypes


class SceneTreeNodeTree(types.NodeTree):
    charstring_directory: str
    use_home_base_images: bool
    view_center: list[float]
    output_file: str
    smaller: bool
    # Literal["GAME", "CUSTOM", "DLIG"]
    feature_type: str
    custom_feature_name: str


class SceneTreeSpaceDataType(types.SpaceNodeEditor):
    tree_type: Literal["SceneTreeType"]
    node_tree: SceneTreeNodeTree
    cursor_location: list[float]


class CompositorNodeTreeSpaceDataType(types.SpaceNodeEditor):
    tree_type: Literal["CompositorNodeTree"]
    node_tree: CompositorNodeTree


CompositorNode = str


class CompositorNodeTree:
    bl_idname: str
    nodes: list[CompositorNode]


class View3dAreaSpaces(NamedTuple):
    not_a_real_named_tuple: types.SpaceView3d


class NodeEditorAreaSpaces(NamedTuple):
    not_a_real_named_tuple: SceneTreeSpaceDataType | CompositorNodeTreeSpaceDataType


class View3DArea:
    type: Literal["VIEW_3D"]
    spaces: View3dAreaSpaces


class NodeEditorArea:
    type: Literal["NODE_EDITOR"]
    spaces: NodeEditorAreaSpaces


AllSpaceData = SceneTreeSpaceDataType | CompositorNodeTreeSpaceDataType | types.SpaceView3d


class AnimatedImagePropertiesType(Protocol):
    animation_key_before: bool
    animation_key_after: bool
    animation_repeat_times: int
    animation_show_all_preview: bool
    animation_number_of_preview_name: int
    animation_start_number: int
    animation_end_number: int
    all_slot_start: int
    all_slot_name_pattern: str

class ImagePropertiesType:
    animation_key_before: bool
    animation_key_after: bool
    animation_repeat_times: int
    animation_show_all_preview: bool
    animation_number_of_preview_name: int
    animation_start_number: int
    animation_end_number: int
    all_slot_start: int
    all_slot_name_pattern: str



class SearchPropertiesType:
    only_selected_nodes: bool
    find_image: Optional[types.Image]
    replace_image: Optional[types.Image]


class SizePropertiesType:
    global_enable: bool
    poll_every_seconds: float
    lock_viewport_to_camera: bool
    keep_sidebar_on_at_all_times: bool
    regenerate_deleted_camera: bool
    lock_camera_position: bool
    size_images: bool
    reset_image_offset: bool
    reset_image_y_location: bool
    lock_image_scale: bool
    lock_image_rotation: bool


class DontSizeMePropertiesType:
    disable_automatic_size: bool
    disable_export: bool

class ExportPropertiesType:
    charstring_directory: str

class ConverterPropertiesType:
    images_folder: str
    otf_file_path: str
    use_most_recent_export: bool
    most_recent_otf_export_path: str
    export_number: int

class TextPropertiesType:
    ...

class WindowManagerType:
    text_props: TextPropertiesType
    image_props: ImagePropertiesType
    search_props: SearchPropertiesType
    size_props: SizePropertiesType
    export_props: ExportPropertiesType
    dontsize_props: DontSizeMePropertiesType
    converter_props: ConverterPropertiesType
    def progress_begin(self,min: float, max: float) -> None:...
    def progress_update(self,value: float) -> None:...
    def progress_end(self) -> None:...
    def invoke_search_popup(self, s: Any) -> None: ...
    def invoke_props_dialog(self, s: Any) -> None: ...

class ContextOverride:
    @overload
    def __setitem__(
        self, key: Literal["active_object"], value: AllObjectTypes) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["selected_objects"], value: list[Any]) -> None: ...

class ContextType:
    object: AllObjectTypes
    active_object: Optional[AllObjectTypes]
    scene: types.Scene
    view_layer: types.ViewLayer
    selected_objects: Sequence[AllObjectTypes]
    space_data: Optional[AllSpaceData]
    window: types.Window
    window_manager: WindowManagerType
    screen: types.Screen
    def copy(self) -> ContextOverride: ...

    


class SelectSlotOperatorType:
    nodeSceneName: str
    slotNumber: int


class JumpToSceneOperatorType:
    nodeSceneName: str


class MakeAnimationOperatorType:
    key_before: bool
    key_after: bool
    use_current_frame: bool
    frame_number: int
    repeat_times: int


# class LoadAnimatedImageOperatorType:
#     pattern_info:

class AddNodeOperatorType:
    type: str
    use_transform: bool


class AssignSlotsInPatternOperatorType:
    pattern: str
    slot_start: int


class SelectSlottable(Protocol):
    node_scene: types.Scene
    number_of_slots: int
    node_slot1: types.Image
    node_slot2: types.Image
    node_slot3: types.Image
    node_slot4: types.Image
    node_slot5: types.Image
    node_slot6: types.Image
    node_slot7: types.Image
    node_slot8: types.Image
    node_slot9: types.Image
    node_slot10: types.Image
    node_slot11: types.Image
    node_slot12: types.Image
    node_slot13: types.Image
    node_slot14: types.Image
    node_slot15: types.Image
    node_slot16: types.Image
    node_slot17: types.Image
    node_slot18: types.Image
    node_slot19: types.Image
    node_slot20: types.Image


class HasNodeScene(Protocol):
    node_scene: types.Scene


EnumPropertyItem = Tuple[str, str, str, int]
