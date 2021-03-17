"""DEPRECATED - This module is kept here only as a backward compatibility shim
for the old ufoLib.plistlib module, which was moved to fontemon_blender_addon.fontTools.misc.plistlib.
Please use the latter instead.
"""
from fontemon_blender_addon.fontTools.misc.plistlib import dump, dumps, load, loads, tobytes

# The following functions were part of the old py2-like ufoLib.plistlib API.
# They are kept only for backward compatiblity.
from fontemon_blender_addon.fontTools.ufoLib.utils import deprecated


@deprecated("Use 'fontemon_blender_addon.fontTools.misc.plistlib.load' instead")
def readPlist(path_or_file):
    did_open = False
    if isinstance(path_or_file, str):
        path_or_file = open(path_or_file, "rb")
        did_open = True
    try:
        return load(path_or_file, use_builtin_types=False)
    finally:
        if did_open:
            path_or_file.close()


@deprecated("Use 'fontemon_blender_addon.fontTools.misc.plistlib.dump' instead")
def writePlist(value, path_or_file):
    did_open = False
    if isinstance(path_or_file, str):
        path_or_file = open(path_or_file, "wb")
        did_open = True
    try:
        dump(value, path_or_file, use_builtin_types=False)
    finally:
        if did_open:
            path_or_file.close()


@deprecated("Use 'fontemon_blender_addon.fontTools.misc.plistlib.loads' instead")
def readPlistFromString(data):
    return loads(tobytes(data, encoding="utf-8"), use_builtin_types=False)


@deprecated("Use 'fontemon_blender_addon.fontTools.misc.plistlib.dumps' instead")
def writePlistToString(value):
    return dumps(value, use_builtin_types=False)
