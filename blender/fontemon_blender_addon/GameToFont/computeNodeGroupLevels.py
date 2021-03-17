import bpy
from .constants import firstNodeId
from collections import OrderedDict

class NodeGroup:
    def __init__(self, nodeIds: "list[str]", level: int) -> None:
        self.nodeIds = nodeIds
        self.level = level





def _biDirectionalSceneGraph(nodes, nodeId, out_inputs, visitedNodes):
    # type: (bpy.SceneNodeInfosType, bpy.NodeId, bpy.NodeGroupInputs, set[bpy.NodeId]) -> None
    if nodeId in visitedNodes:
        return
    node = nodes[nodeId]
    visitedNodes.add(nodeId)

    for condition in node['conditions']:
        inputs = out_inputs.setdefault(condition[
            'node_id'], set())
        inputs.add(nodeId)
    for condition in node['conditions']:
        _biDirectionalSceneGraph(nodes=nodes,
                                 nodeId=condition['node_id'],
                                 out_inputs=out_inputs,
                                 visitedNodes=visitedNodes)
    return


def biDirectionalSceneGraph(nodes):
    # type: (bpy.SceneNodeInfosType) -> bpy.NodeGroupInputs
    graph = {}  # type: bpy.NodeGroupInputs
    _biDirectionalSceneGraph(nodes, firstNodeId, graph, set())
    graph[firstNodeId] = set()
    return graph


def _buildNodeGroup(nodes, inputs, nodeId, firstNode, out_nodeGroupNodes):
    # type: (bpy.SceneNodeInfosType, bpy.NodeGroupInputs, bpy.NodeId, bool, list[bpy.NodeId]) -> list[bpy.NodeId]
    if not firstNode and len(inputs[nodeId]) > 1:
        return out_nodeGroupNodes
    out_nodeGroupNodes.append(nodeId)
    node = nodes[nodeId]
    if len(node['conditions']) != 1:
        return out_nodeGroupNodes
    return _buildNodeGroup(nodes=nodes,
                           inputs=inputs,
                           nodeId=node['conditions'][0]['node_id'],
                           firstNode=False,
                           out_nodeGroupNodes=out_nodeGroupNodes)


def buildNodeGroup(nodes, inputs, nodeId):
    # type: (bpy.SceneNodeInfosType, bpy.NodeGroupInputs, bpy.NodeId) -> list[bpy.NodeId]
    return _buildNodeGroup(nodes, inputs, nodeId, True, [])


def _computeNodeGroupLevels(nodes, inputs, out_nodeIdToNodeGroup, nodeId,
                            level):
    # type: (bpy.SceneNodeInfosType, bpy.NodeGroupInputs, dict[bpy.NodeId, NodeGroup], bpy.NodeId, int) -> None
    if nodeId not in out_nodeIdToNodeGroup:
        nodeGroupNodes = buildNodeGroup(nodes, inputs, nodeId)
        out_nodeIdToNodeGroup[nodeId] = NodeGroup(nodeGroupNodes, level)
        lastNode = nodes[nodeGroupNodes[-1]]
        for condition in lastNode['conditions']:
            _computeNodeGroupLevels(
                nodes=nodes,
                inputs=inputs,
                out_nodeIdToNodeGroup=out_nodeIdToNodeGroup,
                nodeId=condition['node_id'],
                level=level + 1)
        return
    alreadyComputedNodeGroup = out_nodeIdToNodeGroup[nodeId]
    if level <= alreadyComputedNodeGroup.level:
        return
    alreadyComputedNodeGroup.level = level
    lastNode = nodes[alreadyComputedNodeGroup.nodeIds[-1]]
    for condition in lastNode['conditions']:
        _computeNodeGroupLevels(nodes=nodes,
                                inputs=inputs,
                                out_nodeIdToNodeGroup=out_nodeIdToNodeGroup,
                                nodeId=condition['node_id'],
                                level=level + 1)
    return


def computeNodeGroupLevels(nodes):
    # type: (bpy.SceneNodeInfosType) -> OrderedDict[int, list[list[bpy.NodeId]]]
    nodeIdToNodeGroup = {}  # type: dict[bpy.NodeId, NodeGroup]
    inputs = biDirectionalSceneGraph(nodes)
    _computeNodeGroupLevels(nodes, inputs, nodeIdToNodeGroup, firstNodeId, 0)
    levelToNodeGroupNodes = {} # type: dict[int, list[list[bpy.NodeId]]]
    for nodeGroup in nodeIdToNodeGroup.values():
      currentLevelNodeGroups = levelToNodeGroupNodes.setdefault(nodeGroup.level, [])
      currentLevelNodeGroups.append(nodeGroup.nodeIds)
    return OrderedDict(sorted(levelToNodeGroupNodes.items()))
