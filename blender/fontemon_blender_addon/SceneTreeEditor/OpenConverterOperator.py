
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from webbrowser import open

class OpenConverterOperator(Operator, Plugin):
    """Open Converter in a browser window"""
    bl_idname = "font.open_converter"
    bl_label = "Image to CharString Converter"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        _ = open(url="http://localhost:8020/converter.html", new=0, autoraise=True)
        return {'FINISHED'}
