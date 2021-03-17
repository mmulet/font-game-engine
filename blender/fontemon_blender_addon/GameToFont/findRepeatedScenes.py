import bpy


def findRepeatedScenes(nodes):
    # type: (bpy.SceneNodeInfosType) -> set[str]
    foundSceneOnce = set()  # type: set[str]
    repeatedScene = set()  # type: set[str]
    for node in nodes.values():
        scene_name = node['scene_name']
        if scene_name in foundSceneOnce:
            repeatedScene.add(scene_name)
            continue
        foundSceneOnce.add(scene_name)
    return repeatedScene
