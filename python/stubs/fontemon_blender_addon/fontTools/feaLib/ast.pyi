class Element:
    def asFea(self, indent: str = ...) -> str:
        ...


class Statement(Element):
    ...


class Block(Statement):
    statements: list[Statement]


class Expression(Element):
    ...


class FeatureFile(Block):
    statements: list[Element]


class GlyphName(Expression):
    def __init__(self, glyph: str) -> None:
        ...


class GlyphClass(Expression):
    def __init__(self, glyphs: list[GlyphName]) -> None:
        ...


class GlyphClassDefinition(Element):
    def __init__(self, name: str, glyphs: GlyphClass) -> None:
        ...


class GlyphClassName(Expression):
    def __init__(self, defintion: GlyphClassDefinition) -> None:
        ...


class FeatureBlock(Block):
    def __init__(self, name: str) -> None:
        ...


class LookupBlock(Block):
    def __init__(self, name: str) -> None:
        ...


GlyphContaningObject = GlyphName | GlyphClass | GlyphClassName


class LigatureSubstStatement(Statement):
    def __init__(self, prefix: list[GlyphContaningObject],
                 glyphs: list[GlyphContaningObject],
                 suffix: list[GlyphContaningObject],
                 replacement: GlyphContaningObject) -> None:
        ...


class SingleSubstStatement(Statement):
    def __init__(
        self,
        glyphs: list[GlyphContaningObject],
        replacement: GlyphContaningObject,
        prefix: list[GlyphContaningObject],
        suffix: list[GlyphContaningObject],
    ) -> None:
        ...