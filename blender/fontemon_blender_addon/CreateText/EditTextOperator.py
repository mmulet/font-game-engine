
from ..Common import text_object
from .validate_options import validate_options
from .setup_text_objects import setup_text_objects
from ..Plugin import Plugin
from .CanEditText import CanEditText
from .parse_text import parse_text, ParseState, WordParseState
from .EditTextError import EditTextError
from .remove_all_children import remove_all_children
import bpy
from bpy.types import Operator


class EditTextOperator(Operator, Plugin, CanEditText):
    """Edit an empty object into font text object"""
    bl_idname = "object.font_edit_text"
    bl_label = "Apply Text Changes"

    def execute(self, context):
        # type: (bpy.ContextType) -> set[bpy.Literal["FINISHED"]]
        self.edit_text(context)
        return {'FINISHED'}

    def edit_text(self, context):
        # type: (bpy.ContextType) -> None
        o = text_object(context.object)
        if o is None:
            self.report(
                {'ERROR'}, "Not a Text Object")
            return
        try:
            use_word_parser = o['font_text_word_based_frame']
            parser = WordParseState() if use_word_parser else ParseState()
            parse_text(o['font_text'], o['font_text_line_width'], parser)
            start_frame = context.scene.frame_current if o["font_text_use_current_frame_as_start"] else o['font_text_start_frame']
            if o['font_text_use_current_frame_as_start']:
                o['font_text_start_frame'] = start_frame
                o['font_text_use_current_frame_as_start'] = False
            validate_options(o, parser.number_of_frames(), start_frame)
            remove_all_children(o)
            setup_text_objects(context,
                               o,
                               parser.parsed_text,
                               "Word" if use_word_parser else "Character",
                               start_frame
                               )

            # change the current frame, then change it back
            # to force a redraw
            context.scene.frame_current += 1
            context.scene.frame_current -= 1
        except EditTextError as e:
            self.report({'ERROR'}, e.message)
            return
        return
