import bpy

class AdjustSlotsError(Exception):
    """What goes wrong during an export. 
    Pass the message and the nodes that we will highlight """

    def __init__(self, message, nodes):
        # type: (str, bpy.Sequence[bpy.AllNodeTypes]) -> None
        self.message = message
        self.nodes = nodes
        Exception.__init__(self, message)
