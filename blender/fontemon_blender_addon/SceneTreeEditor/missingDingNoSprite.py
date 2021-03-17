from random import randint

# Special processing for the
# *glitch* fontemon

sprite_choices = [
    "dollar.png",
    "question.png",
    "ampersand.png",
    "asciicircum.png",
    "asciitilde.png",
    "asterisk.png",
    "braceleft.png",
    "braceright.png",
    "bracketright.png",
    "colon.png",
    "exclam.png",
    "grave.png",
    "percent.png",
    "plus.png",
    "question.png",
]

length = len(sprite_choices) - 1

def missingDingNoSprite():
    # type: () -> str
    return sprite_choices[randint(0,length)]