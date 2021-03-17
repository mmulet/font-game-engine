print(__name__)

from fontemon_blender_addon.fontTools.misc.py23 import *
import logging
from fontemon_blender_addon.fontTools.misc.loggingTools import configLogger

log = logging.getLogger(__name__)

version = __version__ = "4.18.2"

__all__ = ["version", "log", "configLogger"]

print("in this module")
