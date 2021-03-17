# When there are less than 1240 subroutines, the subroutines are biased
# by -107. When there are more, We need to adjust the subroutines.
# First add 107 to get rid of the old bias, then minus the new bias
from re import compile

find_subroutines = compile(r"(-?\d+)\s+callsubr")


def adjustSubroutineBias(string: str, subroutineCount: int) -> str:
    if subroutineCount < 1240:
        return string
    biasAdjustment = 107 + (-1131 if subroutineCount < 33900 else -32768)

    return find_subroutines.sub(
        lambda match: f"{int(match[1]) + biasAdjustment} callsubr", string)
