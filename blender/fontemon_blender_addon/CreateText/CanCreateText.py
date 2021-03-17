 
import bpy
from ..Common import has_all_text_attributes


class CanCreateText:
    @classmethod
    def poll(cls, context):
        # type: (bpy.ContextType) -> bool
        if context.object is None:
            return False
        o = context.object
        if (o.type != 'EMPTY' or
            o.empty_display_type != 'PLAIN_AXES' or
                has_all_text_attributes(o)):
            return False
        return True
