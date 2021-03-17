
from ..Common.text_object import text_object
import bpy


class CanEditText:
    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        return text_object(context.object) is not None
