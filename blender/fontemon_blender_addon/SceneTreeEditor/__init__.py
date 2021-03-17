from .SceneTree import SceneTree
from .SceneInput import SceneInput
from .FirstSceneNode import FirstSceneNode
from .SceneNode import SceneNode
from .EndSceneNode import EndSceneNode
from .ConditionNode import ConditionNode
from .GotoLostNode import GotoLostNode
from .ExportSceneTreeToInfo import ExportSceneTreeToInfo
from .SceneTreeExportMenu import SceneTreeExportMenu
from .SceneTreeCategory import SceneTreeCategory
from .SelectSlotOperator import SelectSlotOperator
from ..Plugin import MultiplePluginHolder
from .JumpToSceneOperator import JumpToSceneOperator
from .ImagePropertiesPanel import ImagePropertiesPanel
from .MakeAnimationOperator import MakeAnimationOperator
from .LoadAnimatedImagesOperator import LoadAnimatedImagesOperator
from .SelectParentOperator import SelectParentOperator
from .SlotNode import SlotNode
from .SlotObjectNode import SlotObjectNode
from .SlotSceneNode import SlotSceneNode
from .FixSlotsOperator import FixSlotsOperator
from .AdjustSlotsOperator import AdjustSlotsOperator
from .AddSlotBelowOperator import AddSlotBelowOperator
from .AddSlotAboveOperator import AddSlotAboveOperator
from .RemoveSlotNodeOperator import RemoveSlotNodeOperator
from .SceneSearchOperator import SceneSearchOperator
from .SceneTreeSearchMenu import SceneTreeSearchMenu
from .SearchForSlotByName import SearchForSlotByNameOperator
from .SearchForImageInSlot import SearchForImageInSlotOperator
from .ReplaceSlotImagesOperator import ReplaceSlotImagesOperator
from .AssignSlotsInPatternOperator import AssignSlotsInPatternOperator
from .SearchPanel import SearchPanel
from .ExportScript import ExportScript
from .AddFontImageOperator import AddFontImageOperator
from .AddFontTextOperator import AddFontTextOperator
from .AddFontImageAndTextMenu import AddFontImageAndTextMenu
from .EmptyImageWithoutDataPropertiesPanel import EmptyImageWithoutDataPropertiesPanel
from .AlwaysOnFontPanel import AlwaysOnFontPanel
from .MakeParentOperator import MakeParentOperator
from .SelectChildrenAndShowOperator import SelectChildrenAndShowOperator
from .ParentPropertiesPanel import ParentPropertiesPanel
from .ClearChildrenOperator import ClearChildrenOperator
from .CreateAnimation import CreateAnimation
from .ExportSceneTreeToFont import ExportSceneTreeToFont
from .ExportPanel import ExportPanel
from .OpenTextPreviewOperator import OpenTextPreviewOperator
from .OpenConverterOperator import OpenConverterOperator
from .OpenTestFontOperator import OpenTestFontOperator
from .AddNodePanel import AddNodePanel
from .AddNodeAtCenterOperator import AddNodeAtCenterOperator

class SceneTreeEditor(MultiplePluginHolder):
    plugins = (
        AddNodeAtCenterOperator,
        AddNodePanel,
        AddFontImageOperator,
        AddFontTextOperator,
        AddFontImageAndTextMenu,
        CreateAnimation,
        OpenTextPreviewOperator,
        OpenConverterOperator,
        OpenTestFontOperator,
        AlwaysOnFontPanel,
        SceneTree,
        SceneInput,
        SelectParentOperator,
        SelectSlotOperator,
        JumpToSceneOperator,
        MakeAnimationOperator,
        LoadAnimatedImagesOperator,
        AssignSlotsInPatternOperator,
        AddSlotBelowOperator,
        AddSlotAboveOperator,
        RemoveSlotNodeOperator,
        AdjustSlotsOperator,
        FixSlotsOperator,
        FirstSceneNode,
        SceneNode,
        ConditionNode,
        EndSceneNode,
        GotoLostNode,
        ExportSceneTreeToFont,
        ExportSceneTreeToInfo,
        ExportScript,
        SceneTreeExportMenu,
        SceneTreeCategory,
        MakeParentOperator,
        ImagePropertiesPanel,
        SelectChildrenAndShowOperator,
        ClearChildrenOperator,
        ParentPropertiesPanel,
        SlotNode,
        SlotObjectNode,
        SlotSceneNode,
        SceneSearchOperator,
        ReplaceSlotImagesOperator,
        SearchForSlotByNameOperator,
        SearchForImageInSlotOperator,
        SceneTreeSearchMenu,
        SearchPanel,
        ExportPanel,
        EmptyImageWithoutDataPropertiesPanel
    )
