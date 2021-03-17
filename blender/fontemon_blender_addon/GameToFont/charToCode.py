# from ..CreateText.parse_text import parse_char
import bpy
import re
from .GameToFontError import GameToFontError
def to_char(text):
    # type: (str) -> str
    return text
_lowercase = re.compile("[a-z]")

def charToCode(i: str) -> str:
   # type: (str) -> bpy.ParsedResult
    # Generated by imageToCharStringConverter/cli/src/createFont.ts
    # do not modify by hand
    if i == "\\":
        return "backslash"
    if i == " ":
        return "space"
    if _lowercase.match(i) is not None:
        return to_char(i.upper())
    if i.isupper():
        return to_char("capital"+i)
    if i == "0":
        return to_char("zero")
    if i == "1":
        return to_char("one")
    if i == "2":
        return to_char("two")
    if i == "3":
        return to_char("three")
    if i == "4":
        return to_char("four")
    if i == "5":
        return to_char("five")
    if i == "6":
        return to_char("six")
    if i == "7":
        return to_char("seven")
    if i == "8":
        return to_char("eight")
    if i == "9":
        return to_char("nine")
    if i == "!":
        return to_char("exclam")
    if i == "\"":
        return to_char("quotedbl")
    if i == "#":
        return to_char("numbersign")
    if i == "$":
        return to_char("dollar")
    if i == "%":
        return to_char("percent")
    if i == "&":
        return to_char("ampersand")
    if i == "'":
        return to_char("quotesingle")
    if i == "(":
        return to_char("parenleft")
    if i == ")":
        return to_char("parenright")
    if i == "*":
        return to_char("asterisk")
    if i == "+":
        return to_char("plus")
    if i == ",":
        return to_char("comma")
    if i == "-":
        return to_char("hyphen")
    if i == ".":
        return to_char("period")
    if i == "/":
        return to_char("slash")
    if i == ":":
        return to_char("colon")
    if i == ";":
        return to_char("semicolon")
    if i == "<":
        return to_char("less")
    if i == "=":
        return to_char("equal")
    if i == ">":
        return to_char("greater")
    if i == "?":
        return to_char("question")
    if i == "@":
        return to_char("at")
    if i == "[":
        return to_char("bracketleft")
    if i == "]":
        return to_char("bracketright")
    if i == "^":
        return to_char("asciicircum")
    if i == "_":
        return to_char("underscore")
    if i == "`":
        return to_char("grave")
    if i == "{":
        return to_char("braceleft")
    if i == "|":
        return to_char("bar")
    if i == "}":
        return to_char("braceright")
    if i == "~":
        return to_char("asciitilde")
    if i == "©":
        return to_char("copyright")
    # end generated

    raise GameToFontError("Unrecognized character in text: " + i)
