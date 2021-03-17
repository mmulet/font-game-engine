 
import bpy

class SceneTreeNode:
    """Mix-in class for all custom nodes in this tree type.
    Defines a poll function to enable instantiation."""
    @classmethod
    def poll(cls, ntree):
        # type: (bpy.types.NodeTree) -> bool
        return ntree.bl_idname == 'SceneTreeType'
