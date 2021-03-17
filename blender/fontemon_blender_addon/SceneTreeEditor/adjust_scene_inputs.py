
import bpy


def adjust_inputs(self, context):
    # type: (bpy.SceneTreeNodeInput, bpy.ContextType) -> None
    """Adjust the number of sockets on the node 
        so that it matches the number_of_inputs property"""
    number_to_adjust_by = self.number_of_inputs - len(self.inputs)
    if number_to_adjust_by == 0:
        return
    elif number_to_adjust_by > 0:
        for _ in range(0, number_to_adjust_by):
            _ = self.inputs.new('SceneInputSocket', "Scene")
    else:
        # Clear the unlinked sockets first before the linked ones
        # just makes everything easier
        unlinked_list = [k for k in self.inputs if not k.is_linked]
        number_to_adjust_by = abs(number_to_adjust_by)
        for _ in range(0, number_to_adjust_by):
            if len(unlinked_list) <= 0:
                break
            number_to_adjust_by -= 1
            self.inputs.remove(unlinked_list.pop())
        linked_list = [k for k in self.inputs if k.is_linked]
        for _ in range(0, number_to_adjust_by):
            if len(self.inputs) <= 0:
                break
            self.inputs.remove(linked_list.pop())
