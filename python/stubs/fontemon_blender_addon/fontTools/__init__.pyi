# pyright: reportUnusedImport=false

# Taken partiall from https://fonttools.readthedocs.io/en/latest/
# This is a stub in the fullest sense of the word. It is definitely not complete.
# I've just been adding types as I have been using them

from typing import Sequence

from typing_extensions import Literal
from . import ttLib
from . import feaLib

class DefaultLangSysType:
    ReqFeatureIndex: int


class ScriptType:
    DefaultLangSys: DefaultLangSysType


class ScriptRecordType:
    Script: ScriptType


class ScriptListType:
    ScriptRecord: Sequence[ScriptRecordType]


class TableType:
    ScriptList: ScriptListType


class GSUB_GPOSType:
    table: TableType


class CFFTablePrivateType:
    defaultWidthX: int
    nominalWidthX: int


class CFFTableType:
    Private: CFFTablePrivateType


class CFFType:
    def __getitem__(self, key: Literal["Fontemon"]) -> CFFTableType: ...


class CFF_Type:
    cff: CFFType