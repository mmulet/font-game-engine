 
class GameToFontError(Exception):
    """What goes wrong during an game to font.  """

    def __init__(self, message):
        # type: (str) -> None
        self.message = message
        Exception.__init__(self, message)
