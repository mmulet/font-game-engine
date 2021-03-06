# Copyright (c) 2009 Type Supply LLC
# Author: Tal Leming

from fontemon_blender_addon.fontTools.misc.py23 import *
from fontemon_blender_addon.fontTools.misc.fixedTools import otRound
from fontemon_blender_addon.fontTools.misc.psCharStrings import T2CharString
from fontemon_blender_addon.fontTools.pens.basePen import BasePen
from fontemon_blender_addon.fontTools.cffLib.specializer import specializeCommands, commandsToProgram


def t2c_round(number, tolerance=0.5):
    if tolerance == 0:
        return number  # no-op
    rounded = otRound(number)
    # return rounded integer if the tolerance >= 0.5, or if the absolute
    # difference between the original float and the rounded integer is
    # within the tolerance
    if tolerance >= .5 or abs(rounded - number) <= tolerance:
        return rounded
    else:
        # else return the value un-rounded
        return number

def makeRoundFunc(tolerance):
    if tolerance < 0:
        raise ValueError("Rounding tolerance must be positive")

    def roundPoint(point):
        x, y = point
        return t2c_round(x, tolerance), t2c_round(y, tolerance)

    return roundPoint


class T2CharStringPen(BasePen):
    """Pen to draw Type 2 CharStrings.

    The 'roundTolerance' argument controls the rounding of point coordinates.
    It is defined as the maximum absolute difference between the original
    float and the rounded integer value.
    The default tolerance of 0.5 means that all floats are rounded to integer;
    a value of 0 disables rounding; values in between will only round floats
    which are close to their integral part within the tolerated range.
    """

    def __init__(self, width, glyphSet, roundTolerance=0.5, CFF2=False):
        super(T2CharStringPen, self).__init__(glyphSet)
        self.roundPoint = makeRoundFunc(roundTolerance)
        self._CFF2 = CFF2
        self._width = width
        self._commands = []
        self._p0 = (0,0)

    def _p(self, pt):
        p0 = self._p0
        pt = self._p0 = self.roundPoint(pt)
        return [pt[0]-p0[0], pt[1]-p0[1]]

    def _moveTo(self, pt):
        self._commands.append(('rmoveto', self._p(pt)))

    def _lineTo(self, pt):
        self._commands.append(('rlineto', self._p(pt)))

    def _curveToOne(self, pt1, pt2, pt3):
        _p = self._p
        self._commands.append(('rrcurveto', _p(pt1)+_p(pt2)+_p(pt3)))

    def _closePath(self):
        pass

    def _endPath(self):
        pass

    def getCharString(self, private=None, globalSubrs=None, optimize=True):
        commands = self._commands
        if optimize:
            maxstack = 48 if not self._CFF2 else 513
            commands = specializeCommands(commands,
                                          generalizeFirst=False,
                                          maxstack=maxstack)
        program = commandsToProgram(commands)
        if self._width is not None:
            assert not self._CFF2, "CFF2 does not allow encoding glyph width in CharString."
            program.insert(0, otRound(self._width))
        if not self._CFF2:
            program.append('endchar')
        charString = T2CharString(
            program=program, private=private, globalSubrs=globalSubrs)
        return charString
