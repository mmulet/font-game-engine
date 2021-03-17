from ..ttLib import TTFont
from .ast import FeatureFile


def addOpenTypeFeatures(tt: TTFont, path: str | FeatureFile) -> None:
    ...


def addOpenTypeFeaturesFromString(tt: TTFont, features: str) -> None:
    ...
