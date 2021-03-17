 # pyright: reportUnusedFunction=false

class PatternError(Exception):
    def __init__(self, i: int):
        self.i = i

def evaluate_pattern(i, pattern):
    # type: (int, str) -> str
    # helper functions to use in the pattern
    # TODO document these
    def z(a, z):
        # type: (int,int) -> str
        return str(a).zfill(z)
    def iz(z):
        # type: (int) -> str
        return str(i).zfill(z)
    def ipz(p, z):
        # type: (int,int) -> str
        return str(i + p).zfill(z)
    try:
        return eval(pattern)
    except:
        raise PatternError(i)
        
