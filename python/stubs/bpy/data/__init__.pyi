from typing import overload
from bpy import CameraObjectType, EmptyImageObjectType, EmptyImageObjectTypeWithData
from bpy.types import Camera, Image
import bpy
filepath: str


class ObjectsType:
    @overload
    def new(self, name: str, object_data: None) -> EmptyImageObjectType: ...
    @overload
    def new(self, name: str, object_data: Camera) -> CameraObjectType: ...
    @overload
    def new(self, name: str, object_data: Image) -> EmptyImageObjectTypeWithData: ...


objects: ObjectsType

class ImagesType:
    def new(self, name: str, width: int, height: int, alpha: bool=..., float_buffer: bool=...) -> Image : ...

    def load(self, path: str, check_existing: bool) -> bpy.types.Image: ...

    def __getitem__(
        self, key: str) -> bpy.types.Image: ...

    def __contains__(self, key: str
                     ) -> bool: ...


images: ImagesType


class ScenesType:
    def __setitem__(
        self, key: str, value: bpy.types.Scene) -> None: ...

    def __getitem__(
        self, key: str) -> bpy.types.Scene: ...


scenes: ScenesType


class cameras:
    @classmethod
    def new(cls, name: str) -> Camera: ...
