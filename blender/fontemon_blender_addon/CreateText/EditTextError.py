
class EditTextError(Exception):
    """Something went wrong while editing the text"""

    def __init__(self, message):
        # type: (str) -> None
        self.message = message
        Exception.__init__(self, message)
