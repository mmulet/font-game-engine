import bpy


def view_nodes(all_nodes, selected_nodes):
    # type: (bpy.Sequence[bpy.types.Node],bpy.Sequence[bpy.types.Node]) -> None
    for n in all_nodes:
        n.select = False
    for n in selected_nodes:
        n.select = True
    bpy.ops.node.view_selected()
