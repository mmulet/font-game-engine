from typing import Type
from bpy import context_test

class Larry:
    pass


class Harry:
    larry: Type[context_test] 