
from ..Plugin import Plugin
import bpy
from bpy.types import Operator
from webbrowser import open

class OpenTextPreviewOperator(Operator, Plugin):
    """Open Text Preview in a browser window"""
    bl_idname = "font.open_text_preview"
    bl_label = "Text Preview tool"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        _ = open(url="http://localhost:8020/textPreview.html", new=0, autoraise=True)
        return {'FINISHED'}
