import pkgutil
import sys
import fontemon_blender_addon.fontTools
import importlib
import os
from pathlib import Path


def main():
    """Show this help"""
    path = fontemon_blender_addon.fontTools.__path__
    descriptions = {}
    for pkg in sorted(
        mod.name
        for mod in pkgutil.walk_packages([fontemon_blender_addon.fontTools.__path__[0]], prefix="fontemon_blender_addon.fontTools.")
    ):
        try:
            imports = __import__(pkg, globals(), locals(), ["main"])
        except ImportError as e:
            continue
        try:
            description = imports.main.__doc__
            if description:
                pkg = pkg.replace("fontemon_blender_addon.fontTools.", "").replace(".__main__", "")
                descriptions[pkg] = description
        except AttributeError as e:
            pass
    for pkg, description in descriptions.items():
        print("fontemon_blender_addon.fontTools %-12s %s" % (pkg, description), file=sys.stderr)


if __name__ == "__main__":
    print("fontemon_blender_addon.fontTools v%s\n" % fontemon_blender_addon.fontTools.__version__, file=sys.stderr)
    main()
