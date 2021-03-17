from typing import Callable
from .CharStringInfo import CharStringInfo
from .AddSubroutineState import AddSubroutineState
from functools import reduce
import bpy
from xml.etree.ElementTree import Element
from .PixelPosition import PixelPosition
from .verticalLineToCommand import verticalLineToCommand, VerticalLineToPair
from .constants import pixelWidth
from .AddSubroutineState import AddSubroutineState
from .addCharStringToSubroutineTable import addCharStringToSubroutineTable


def addRepeatedPixelSubroutines(
    out_subroutineTable,
    startSubroutineIndex,
    startSubroutineNumber,
    smaller,
):
    # type: (Element, int, int, bool) -> AddSubroutineState[int]
    fakePosition = PixelPosition(0, 0)

    def repeat(y):
        # type: (int) -> bpy.Callable[[int], str]
        return lambda numberOfPixels: verticalLineToCommand(pairs=[
            VerticalLineToPair(dy=-y, thenDx=numberOfPixels * pixelWidth)
        ],
                                                            lastDy=y)

    # Draw in an alternating pattern like this
    # |                   |                                 |                  |
    # |                   |           ___________           |    second ______ |                ____________
    # |______  first      |__________|           |__________|                       difference |
    #                       pixelWidth pixelWidth  pixelWidth
    # First draw, the initial line down of length first, then ( go right pixelWidth)
    # Then draw up or down (alternating, so use  k % 2 to check index is even or odd)
    # Then draw the last line upwards at the end (if numberOf pixels is even, it will
    # be the length of the first, otherwise second)
    def alternate(first, second):
        # type: (float, float) -> bpy.Callable[[int], str]
        distance = first - second
        return lambda numberOfPixels: verticalLineToCommand(
            pairs=[VerticalLineToPair(dy=-first, thenDx=pixelWidth)] + [
                VerticalLineToPair(dy=-distance if k % 2 else distance,
                                   thenDx=pixelWidth)
                for k in range(numberOfPixels - 1)
            ],
            lastDy=first if numberOfPixels % 2 else second)

    blackSize = 12
    darkGraySize = 2 if smaller else 6
    lightGraySize = 1 if smaller else 2

    def reducer(state: AddSubroutineState[int],
                toCommands: Callable[[int], str]) -> AddSubroutineState[int]:
        def reducer_2(i: int) -> CharStringInfo:
            return CharStringInfo(toCommands(i), fakePosition, fakePosition)
        # 23 because 24*2 is 48, and the argument stack
        # limit is 48 for Type2 CharString
        return reduce(
            addCharStringToSubroutineTable(reducer_2, out_subroutineTable),
            [i + 2 for i in range(23)], state)

    return reduce(
        reducer, [
            repeat(blackSize),
            repeat(darkGraySize),
            repeat(lightGraySize),
            alternate(blackSize, darkGraySize),
            alternate(blackSize, lightGraySize),
            alternate(darkGraySize, lightGraySize),
            alternate(darkGraySize, blackSize),
            alternate(lightGraySize, blackSize),
            alternate(lightGraySize, darkGraySize),
        ], AddSubroutineState[int]({}, startSubroutineIndex,
                                   startSubroutineNumber))
