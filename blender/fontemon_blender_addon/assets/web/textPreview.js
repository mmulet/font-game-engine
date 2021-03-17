const allColors = [
    "#007aff",
    "#34c759",
    "#33c6a2",
    "#007bff",
    "#5856d6",
    "#9855d6",
    "#00faff",
    "#5593d6",
    "#5ac8fa",
];
const colors = [...new Array(2000).keys()].map(() => allColors[Math.floor(Math.random() * allColors.length)]);

class ParseStateToLineState {
    constructor(lines, current_frame) {
        this.toLine = ParseStateToLineState.toLine;
        this.toCharacterCount = ParseStateToLineState.toCharacterCount;
        this.lengthOfCharacterInLine = ParseStateToLineState.lengthOfCharacterInLine;
        this.lines = lines;
        this.current_frame = current_frame;
    }
}
ParseStateToLineState.toLine = (line) => line;
ParseStateToLineState.toCharacterCount = (_line, kThWord) => kThWord + 1;
ParseStateToLineState.lengthOfCharacterInLine = (line) => line.length;

class WordParserToLineState {
    constructor(lines, current_frame) {
        this.toLine = (line) => line.flatMap((a, index) => (index == 0 ? [] : [" "]).concat(a));
        this.toCharacterCount = (line, kThWord) => {
            let length = 0;
            if (line.length <= 0) {
                return 0;
            }
            for (let i = 0; i < kThWord + 1; i++) {
                if (i != 0) {
                    length++;
                }
                length += line[i].length;
            }
            return length;
        };
        this.lengthOfCharacterInLine = (line) => line.reduce((out, word, index) => (index == 0 ? 0 : 1) + out + word.length, 0);
        this.lines = lines;
        this.current_frame = current_frame;
    }
}

const getLineState = (parser, current_frame) => {
    if (parser == null || parser.parsed_text.length <= 0) {
        return {
            top: {
                line: [],
                drawCount: 0,
            },
            bottom: {
                line: [],
                drawCount: 0,
            },
        };
    }
    switch (parser.type) {
        case "ParseState":
            return genericGetLineState(new ParseStateToLineState(parser.parsed_text, current_frame));
        case "WordParseState":
            return genericGetLineState(new WordParserToLineState(parser.parsed_text, current_frame));
    }
};
const genericGetLineState = ({ lines, current_frame, toCharacterCount, toLine, lengthOfCharacterInLine, }) => {
    let frame = 0;
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        for (let k = 0; k < line.length; k++, frame++) {
            if (frame != current_frame) {
                continue;
            }
            if (i == 0) {
                return {
                    top: {
                        line: toLine(line),
                        drawCount: toCharacterCount(line, k),
                    },
                    bottom: {
                        line: [],
                        drawCount: 0,
                    },
                };
            }
            const lineAbove = lines[i - 1];
            return {
                top: {
                    line: toLine(lineAbove),
                    drawCount: lengthOfCharacterInLine(lineAbove),
                },
                bottom: {
                    line: toLine(line),
                    drawCount: toCharacterCount(line, k),
                },
            };
        }
    }
    if (lines.length == 1) {
        return {
            top: {
                line: toLine(lines[0]),
                drawCount: lengthOfCharacterInLine(lines[0]),
            },
            bottom: {
                line: [],
                drawCount: 0,
            },
        };
    }
    const topLine = lines[lines.length - 2];
    const bottomLine = lines[lines.length - 1];
    return {
        top: {
            line: toLine(topLine),
            drawCount: lengthOfCharacterInLine(topLine),
        },
        bottom: {
            line: toLine(bottomLine),
            drawCount: lengthOfCharacterInLine(bottomLine),
        },
    };
};

const getMaxFrame = (parser) => {
    if (!parser) {
        return 0;
    }
    switch (parser.type) {
        case "WordParseState":
            return Math.max(0, parser.parsed_text.reduce((o, line) => o + line.length, 0) - 1);
        case "ParseState":
            return parser.parsed_text.reduce((o, line) => o + line.length, 0);
    }
};

const isInBox = ({ x, y }, { x: left, y: top, width, height }) => x >= left && x <= left + width && y >= top && y <= top + height;

const lineStateEmpty = {
    top: {
        line: [],
        drawCount: 0,
    },
    bottom: {
        line: [],
        drawCount: 0,
    },
};

const codeToCharacter = (font, code, escapeSpace) => {
    switch (code) {
        case " ":
            return escapeSpace ? "\\ " : " ";
        case "backslash":
            return "\\\\";
    }
    const maybe = font[code];
    if (maybe == undefined) {
        return " ";
    }
    return maybe.char;
};

const parserToString = (parser, font) => {
    if (!parser) {
        return "";
    }
    switch (parser.type) {
        case "ParseState":
            return parser.parsed_text
                .map((line) => line.map((code) => codeToCharacter(font, code, false)).join(""))
                .join("\\n");
        case "WordParseState":
            return parser.parsed_text
                .map((line) => line
                .map((word) => word.map((code) => codeToCharacter(font, code, true)).join(""))
                .join(" "))
                .join("\\n");
    }
};

const parse_char = (i, charToCode) => {
    switch (i) {
        case "\n":
            return "newline";
        case "\\":
            return "newlineMaybe";
        case " ":
            return " ";
    }
    const maybe = charToCode[i];
    return maybe ? maybe[0] : null;
};
class ParseState {
    constructor() {
        this.type = "ParseState";
        this.parsed_text = [];
        this.current_line = [];
        this.mightBeNewLine = false;
        this.get_mightBeNewLine = () => this.mightBeNewLine;
        this.set_mightBeNewLine = (m) => {
            this.mightBeNewLine = m;
        };
        this.addLine = () => {
            this.parsed_text.push(this.current_line);
            this.current_line = [];
        };
        this.addChar = (char, width, _skipSpace = false) => {
            this.current_line.push(char);
            if (this.current_line.length < width) {
                return;
            }
            this.addLine();
        };
        this.shouldSkipDoubleNewline = (width) => {
            if (this.current_line.length > 0) {
                return false;
            }
            if (this.parsed_text.length < 1) {
                return false;
            }
            const lineAbove = this.parsed_text[this.parsed_text.length - 1];
            return lineAbove.length == width;
        };
        this.currentLineIsEmpty = () => this.current_line.length <= 0;
    }
}
class WordParseState {
    constructor() {
        this.type = "WordParseState";
        this.parsed_text = [];
        this.current_line = [];
        this.current_word = [];
        this.mightBeNewLine = false;
        this.get_mightBeNewLine = () => this.mightBeNewLine;
        this.set_mightBeNewLine = (m) => {
            this.mightBeNewLine = m;
        };
        this.addLine = () => {
            if (this.current_word.length > 0) {
                this.current_line.push(this.current_word);
                this.current_word = [];
            }
            this.parsed_text.push(this.current_line);
            this.current_line = [];
        };
        this.lineLength = (line) => {
            let length = 0;
            for (const word of line) {
                length += word.length;
            }
            length += line.length - 1;
            return length;
        };
        this.addChar = (char, width, skipSpace = true) => {
            if (skipSpace && (char == " " || char == "space")) {
                this.current_line.push(this.current_word);
                this.current_word = [];
                return;
            }
            this.current_word.push(char);
            if (this.lineWidth < width) {
                return;
            }
            this.addLine();
        };
        this.shouldSkipDoubleNewline = (width) => {
            if (this.current_line.length > 0 || this.current_word.length > 0) {
                return false;
            }
            if (this.parsed_text.length < 1) {
                return false;
            }
            const lineAbove = this.parsed_text[this.parsed_text.length - 1];
            return this.lineLength(lineAbove) == width;
        };
        this.currentLineIsEmpty = () => {
            return this.current_word.length <= 0 && this.current_line.length <= 0;
        };
    }
    get lineWidth() {
        let length = this.lineLength(this.current_line);
        length +=
            this.current_line.length > 0 && this.current_word.length > 0 ? 1 : 0;
        length += this.current_word.length;
        return length;
    }
}
const parseText = (text, width, charToCode, mutableState) => {
    for (const i of text) {
        if (mutableState.get_mightBeNewLine()) {
            mutableState.set_mightBeNewLine(false);
            switch (i) {
                case "n":
                    if (mutableState.shouldSkipDoubleNewline(width)) {
                        continue;
                    }
                    mutableState.addLine();
                    continue;
                case "\\":
                    mutableState.addChar("backslash", width, true);
                    continue;
                case " ":
                    mutableState.addChar(" ", width, false);
                    continue;
                default:
                    return {
                        error: `Expected a n for a newline character but found: ${i}`,
                        type: "error",
                    };
            }
        }
        const value = parse_char(i, charToCode);
        if (value == null) {
            return {
                error: "Unrecognized character in text: " + i,
                type: "error",
            };
        }
        if (value == "newline") {
            if (mutableState.shouldSkipDoubleNewline(width)) {
                continue;
            }
            mutableState.addLine();
            continue;
        }
        if (value == "newlineMaybe") {
            mutableState.set_mightBeNewLine(true);
            continue;
        }
        mutableState.addChar(value, width, true);
    }
    if (!mutableState.currentLineIsEmpty()) {
        mutableState.addLine();
    }
    return null;
};

const gohuFont = `
STARTFONT 2.1
COMMENT "Copyright by Hugo Chargois"
COMMENT "Licensed under the WTFPL"
FONT -Gohu-Gohufont-Medium-R-Normal--14-100-100-100-C-80-ISO8859-1
SIZE 14 100 100
FONTBOUNDINGBOX 8 14 0 -3
STARTPROPERTIES 31
FOUNDRY "Gohu"
FAMILY_NAME "GohuFont"
WEIGHT_NAME "Medium"
SLANT "R"
SETWIDTH_NAME "Normal"
ADD_STYLE_NAME ""
PIXEL_SIZE 14
POINT_SIZE 100
RESOLUTION_X 100
RESOLUTION_Y 100
SPACING "C"
AVERAGE_WIDTH 80
CHARSET_REGISTRY "ISO8859"
CHARSET_ENCODING "1"
FONTNAME_REGISTRY ""
FONT_NAME "GohuFont"
FACE_NAME "GohuFont"
FONT_VERSION "001.000"
FONT_ASCENT 11
FONT_DESCENT 3
UNDERLINE_POSITION -1
UNDERLINE_THICKNESS 1
X_HEIGHT 7
CAP_HEIGHT 9
RAW_ASCENT 785
RAW_DESCENT 215
NORM_SPACE 8
FIGURE_WIDTH 8
AVG_LOWERCASE_WIDTH 80
AVG_UPPERCASE_WIDTH "80"
_GBDFED_INFO "Edited with gbdfed 1.6."
ENDPROPERTIES
CHARS 191
STARTCHAR space
ENCODING 32
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR exclam
ENCODING 33
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
10
10
10
10
10
10
00
10
10
00
00
00
ENDCHAR
STARTCHAR quotedbl
ENCODING 34
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
24
24
24
00
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR numbersign
ENCODING 35
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
28
28
28
FE
28
28
FE
28
28
28
00
00
00
ENDCHAR
STARTCHAR dollar
ENCODING 36
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
10
10
7C
92
90
90
7C
12
12
92
7C
10
10
00
ENDCHAR
STARTCHAR percent
ENCODING 37
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
64
94
68
08
10
10
20
2C
52
4C
00
00
ENDCHAR
STARTCHAR ampersand
ENCODING 38
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
18
24
24
18
30
4A
44
44
44
3A
00
00
00
ENDCHAR
STARTCHAR quotesingle
ENCODING 39
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
10
10
10
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR parenleft
ENCODING 40
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
08
10
20
20
40
40
40
40
20
20
10
08
00
ENDCHAR
STARTCHAR parenright
ENCODING 41
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
20
10
08
08
04
04
04
04
08
08
10
20
00
ENDCHAR
STARTCHAR asterisk
ENCODING 42
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
10
92
54
38
54
92
10
00
00
00
00
ENDCHAR
STARTCHAR plus
ENCODING 43
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
10
10
10
FE
10
10
10
00
00
00
00
ENDCHAR
STARTCHAR comma
ENCODING 44
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
00
00
00
00
30
30
10
20
00
ENDCHAR
STARTCHAR hyphen
ENCODING 45
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
00
7E
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR period
ENCODING 46
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
00
00
00
00
30
30
00
00
00
ENDCHAR
STARTCHAR slash
ENCODING 47
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
02
02
04
04
08
08
10
10
20
20
40
40
00
00
ENDCHAR
STARTCHAR zero
ENCODING 48
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
46
4A
52
62
42
42
3C
00
00
00
ENDCHAR
STARTCHAR one
ENCODING 49
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
08
18
28
48
08
08
08
08
08
00
00
00
ENDCHAR
STARTCHAR two
ENCODING 50
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
42
04
08
10
20
40
7E
00
00
00
ENDCHAR
STARTCHAR three
ENCODING 51
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
02
02
1C
02
02
42
3C
00
00
00
ENDCHAR
STARTCHAR four
ENCODING 52
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
04
0C
14
24
44
7E
04
04
04
00
00
00
ENDCHAR
STARTCHAR five
ENCODING 53
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
7E
40
40
7C
02
02
02
42
3C
00
00
00
ENDCHAR
STARTCHAR six
ENCODING 54
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
40
40
7C
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR seven
ENCODING 55
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
7E
02
04
04
08
08
10
10
10
00
00
00
ENDCHAR
STARTCHAR eight
ENCODING 56
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
42
42
3C
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR nine
ENCODING 57
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
42
42
3E
02
02
04
38
00
00
00
ENDCHAR
STARTCHAR colon
ENCODING 58
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
18
18
00
00
00
18
18
00
00
00
ENDCHAR
STARTCHAR semicolon
ENCODING 59
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
30
30
00
00
00
30
30
10
20
00
ENDCHAR
STARTCHAR less
ENCODING 60
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
04
08
10
20
40
20
10
08
04
00
00
00
ENDCHAR
STARTCHAR equal
ENCODING 61
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
7E
00
00
00
7E
00
00
00
00
00
ENDCHAR
STARTCHAR greater
ENCODING 62
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
40
20
10
08
04
08
10
20
40
00
00
00
ENDCHAR
STARTCHAR question
ENCODING 63
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
3C
42
02
02
04
08
10
00
10
10
00
00
00
ENDCHAR
STARTCHAR at
ENCODING 64
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
7C
82
9E
A2
A2
A2
A6
9A
80
7E
00
00
00
ENDCHAR
STARTCHAR A
ENCODING 65
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
42
42
7E
42
42
42
42
00
00
00
ENDCHAR
STARTCHAR B
ENCODING 66
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
7C
42
42
42
7C
42
42
42
7C
00
00
00
ENDCHAR
STARTCHAR C
ENCODING 67
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
40
40
40
40
40
42
3C
00
00
00
ENDCHAR
STARTCHAR D
ENCODING 68
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
78
44
42
42
42
42
42
44
78
00
00
00
ENDCHAR
STARTCHAR E
ENCODING 69
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
7E
40
40
40
78
40
40
40
7E
00
00
00
ENDCHAR
STARTCHAR F
ENCODING 70
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
7E
40
40
40
78
40
40
40
40
00
00
00
ENDCHAR
STARTCHAR G
ENCODING 71
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
40
40
4E
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR H
ENCODING 72
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
42
42
42
42
7E
42
42
42
42
00
00
00
ENDCHAR
STARTCHAR I
ENCODING 73
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
38
10
10
10
10
10
10
10
38
00
00
00
ENDCHAR
STARTCHAR J
ENCODING 74
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
02
02
02
02
02
02
42
42
3C
00
00
00
ENDCHAR
STARTCHAR K
ENCODING 75
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
42
44
48
50
60
50
48
44
42
00
00
00
ENDCHAR
STARTCHAR L
ENCODING 76
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
40
40
40
40
40
40
40
40
7E
00
00
00
ENDCHAR
STARTCHAR M
ENCODING 77
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
82
C6
AA
92
92
82
82
82
82
00
00
00
ENDCHAR
STARTCHAR N
ENCODING 78
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
42
62
62
52
52
4A
4A
46
46
00
00
00
ENDCHAR
STARTCHAR O
ENCODING 79
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR P
ENCODING 80
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
7C
42
42
42
7C
40
40
40
40
00
00
00
ENDCHAR
STARTCHAR Q
ENCODING 81
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
42
42
42
4A
4A
44
3A
02
00
00
ENDCHAR
STARTCHAR R
ENCODING 82
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
7C
42
42
42
7C
48
44
42
42
00
00
00
ENDCHAR
STARTCHAR S
ENCODING 83
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
40
40
3C
02
02
42
3C
00
00
00
ENDCHAR
STARTCHAR T
ENCODING 84
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
FE
10
10
10
10
10
10
10
10
00
00
00
ENDCHAR
STARTCHAR U
ENCODING 85
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
42
42
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR V
ENCODING 86
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
42
42
42
42
24
24
24
18
18
00
00
00
ENDCHAR
STARTCHAR W
ENCODING 87
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
82
82
92
92
92
AA
44
44
44
00
00
00
ENDCHAR
STARTCHAR X
ENCODING 88
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
42
42
24
24
18
24
24
42
42
00
00
00
ENDCHAR
STARTCHAR Y
ENCODING 89
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
82
82
44
44
28
10
10
10
10
00
00
00
ENDCHAR
STARTCHAR Z
ENCODING 90
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
7E
02
04
08
10
20
40
40
7E
00
00
00
ENDCHAR
STARTCHAR bracketleft
ENCODING 91
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
1C
10
10
10
10
10
10
10
10
10
1C
00
00
ENDCHAR
STARTCHAR backslash
ENCODING 92
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
40
40
20
20
10
10
08
08
04
04
02
02
00
00
ENDCHAR
STARTCHAR bracketright
ENCODING 93
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
38
08
08
08
08
08
08
08
08
08
38
00
00
ENDCHAR
STARTCHAR asciicircum
ENCODING 94
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
28
44
00
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR underscore
ENCODING 95
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
00
00
00
00
00
00
FF
00
00
ENDCHAR
STARTCHAR grave
ENCODING 96
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
40
20
10
00
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR a
ENCODING 97
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
3C
02
3E
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR b
ENCODING 98
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
40
40
40
5C
62
42
42
42
42
7C
00
00
00
ENDCHAR
STARTCHAR c
ENCODING 99
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
3C
42
40
40
40
42
3C
00
00
00
ENDCHAR
STARTCHAR d
ENCODING 100
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
02
02
02
3E
42
42
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR e
ENCODING 101
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
3C
42
42
7E
40
40
3E
00
00
00
ENDCHAR
STARTCHAR f
ENCODING 102
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
1C
20
20
20
3C
20
20
20
20
20
00
00
00
ENDCHAR
STARTCHAR g
ENCODING 103
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
3E
42
42
42
42
46
3A
02
02
3C
ENDCHAR
STARTCHAR h
ENCODING 104
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
40
40
40
5C
62
42
42
42
42
42
00
00
00
ENDCHAR
STARTCHAR i
ENCODING 105
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
10
00
70
10
10
10
10
10
1C
00
00
00
ENDCHAR
STARTCHAR j
ENCODING 106
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
08
08
00
18
08
08
08
08
08
08
08
08
70
ENDCHAR
STARTCHAR k
ENCODING 107
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
40
40
40
40
44
48
70
48
44
42
00
00
00
ENDCHAR
STARTCHAR l
ENCODING 108
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
30
10
10
10
10
10
10
10
10
0E
00
00
00
ENDCHAR
STARTCHAR m
ENCODING 109
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
FC
92
92
92
92
92
92
00
00
00
ENDCHAR
STARTCHAR n
ENCODING 110
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
7C
42
42
42
42
42
42
00
00
00
ENDCHAR
STARTCHAR o
ENCODING 111
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
3C
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR p
ENCODING 112
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
5C
62
42
42
42
42
7C
40
40
40
ENDCHAR
STARTCHAR q
ENCODING 113
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
3E
42
42
42
42
46
3A
02
02
02
ENDCHAR
STARTCHAR r
ENCODING 114
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
5C
62
40
40
40
40
40
00
00
00
ENDCHAR
STARTCHAR s
ENCODING 115
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
3C
40
40
3C
02
02
7C
00
00
00
ENDCHAR
STARTCHAR t
ENCODING 116
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
10
10
3C
10
10
10
10
10
0C
00
00
00
ENDCHAR
STARTCHAR u
ENCODING 117
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
42
42
42
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR v
ENCODING 118
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
42
42
42
24
24
18
18
00
00
00
ENDCHAR
STARTCHAR w
ENCODING 119
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
82
82
92
92
AA
44
44
00
00
00
ENDCHAR
STARTCHAR x
ENCODING 120
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
42
42
24
18
24
42
42
00
00
00
ENDCHAR
STARTCHAR y
ENCODING 121
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
42
42
42
42
42
46
3A
02
02
3C
ENDCHAR
STARTCHAR z
ENCODING 122
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
7E
04
08
10
20
40
7E
00
00
00
ENDCHAR
STARTCHAR braceleft
ENCODING 123
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
0E
10
10
10
10
10
E0
10
10
10
10
0E
00
ENDCHAR
STARTCHAR bar
ENCODING 124
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
10
10
10
10
10
10
10
10
10
10
10
00
ENDCHAR
STARTCHAR braceright
ENCODING 125
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
70
08
08
08
08
08
07
08
08
08
08
70
00
ENDCHAR
STARTCHAR asciitilde
ENCODING 126
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
62
92
8C
00
00
00
00
00
00
ENDCHAR
STARTCHAR nbspace
ENCODING 160
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR exclamdown
ENCODING 161
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
10
00
10
10
10
10
10
10
10
00
00
00
ENDCHAR
STARTCHAR cent
ENCODING 162
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
10
10
7C
92
90
90
90
92
7C
10
10
00
ENDCHAR
STARTCHAR sterling
ENCODING 163
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
18
24
20
20
78
20
20
20
22
5C
00
00
00
ENDCHAR
STARTCHAR currency
ENCODING 164
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
82
7C
44
44
44
7C
82
00
00
00
ENDCHAR
STARTCHAR yen
ENCODING 165
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
82
82
44
28
10
7C
10
7C
10
10
00
00
00
ENDCHAR
STARTCHAR brokenbar
ENCODING 166
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
10
10
10
10
00
00
10
10
10
10
10
00
ENDCHAR
STARTCHAR section
ENCODING 167
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
38
44
40
30
48
44
44
24
18
04
44
38
00
ENDCHAR
STARTCHAR dieresis
ENCODING 168
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
24
24
00
00
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR copyright
ENCODING 169
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
99
A5
A1
A5
99
42
3C
00
00
00
ENDCHAR
STARTCHAR ordfeminine
ENCODING 170
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
38
04
3C
44
3C
00
7C
00
00
00
00
00
00
ENDCHAR
STARTCHAR guillemotleft
ENCODING 171
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
12
24
48
90
48
24
12
00
00
00
ENDCHAR
STARTCHAR logicalnot
ENCODING 172
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
7E
02
02
02
00
00
00
00
00
ENDCHAR
STARTCHAR softhyphen
ENCODING 173
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
00
00
3C
00
00
00
00
00
00
ENDCHAR
STARTCHAR registered
ENCODING 174
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
B9
A5
B9
A9
A5
42
3C
00
00
00
ENDCHAR
STARTCHAR macron
ENCODING 175
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
7E
00
00
00
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR degree
ENCODING 176
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
18
24
24
18
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR plusminus
ENCODING 177
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
10
10
7C
10
10
00
7C
00
00
00
ENDCHAR
STARTCHAR twosuperior
ENCODING 178
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
18
24
08
10
3C
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR threesuperior
ENCODING 179
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
38
04
18
04
38
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR acute
ENCODING 180
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
08
10
00
00
00
00
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR mu
ENCODING 181
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
42
42
42
42
42
46
7A
40
40
40
ENDCHAR
STARTCHAR paragraph
ENCODING 182
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
7E
F2
F2
F2
F2
72
12
12
12
12
00
00
00
ENDCHAR
STARTCHAR periodcentered
ENCODING 183
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
00
30
30
00
00
00
00
00
00
ENDCHAR
STARTCHAR cedilla
ENCODING 184
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
00
00
00
00
00
00
10
10
20
ENDCHAR
STARTCHAR onesuperior
ENCODING 185
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
30
10
10
38
00
00
00
00
00
00
00
00
ENDCHAR
STARTCHAR ordmasculine
ENCODING 186
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
38
44
44
44
38
00
7C
00
00
00
00
00
00
ENDCHAR
STARTCHAR guillemotright
ENCODING 187
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
90
48
24
12
24
48
90
00
00
00
ENDCHAR
STARTCHAR onequarter
ENCODING 188
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
20
60
20
22
24
08
10
22
46
8A
1E
02
02
00
ENDCHAR
STARTCHAR onehalf
ENCODING 189
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
20
60
20
22
24
08
10
20
4C
92
04
08
1E
00
ENDCHAR
STARTCHAR threequarters
ENCODING 190
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
E0
10
60
12
E4
08
10
22
46
8A
1E
02
02
00
ENDCHAR
STARTCHAR question
ENCODING 191
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
08
08
00
08
10
20
40
40
42
3C
00
00
00
ENDCHAR
STARTCHAR Agrave
ENCODING 192
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
10
08
3C
42
42
42
7E
42
42
42
42
00
00
00
ENDCHAR
STARTCHAR Aacute
ENCODING 193
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
08
10
3C
42
42
42
7E
42
42
42
42
00
00
00
ENDCHAR
STARTCHAR Acircumflex
ENCODING 194
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
18
24
00
3C
42
42
42
7E
42
42
42
00
00
00
ENDCHAR
STARTCHAR Atilde
ENCODING 195
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
32
4C
00
3C
42
42
42
7E
42
42
42
00
00
00
ENDCHAR
STARTCHAR Adieresis
ENCODING 196
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
24
24
00
3C
42
42
42
7E
42
42
42
00
00
00
ENDCHAR
STARTCHAR Aring
ENCODING 197
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
18
24
18
3C
42
42
42
7E
42
42
42
00
00
00
ENDCHAR
STARTCHAR AE
ENCODING 198
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
7E
90
90
90
FC
90
90
90
9E
00
00
00
ENDCHAR
STARTCHAR Ccedilla
ENCODING 199
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
3C
42
40
40
40
40
40
42
3C
10
20
00
ENDCHAR
STARTCHAR Egrave
ENCODING 200
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
10
08
7E
40
40
40
78
40
40
40
7E
00
00
00
ENDCHAR
STARTCHAR Eacute
ENCODING 201
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
08
10
7E
40
40
40
78
40
40
40
7E
00
00
00
ENDCHAR
STARTCHAR Ecircumflex
ENCODING 202
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
18
24
00
7E
40
40
78
40
40
40
7E
00
00
00
ENDCHAR
STARTCHAR Edieresis
ENCODING 203
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
24
24
00
7E
40
40
78
40
40
40
7E
00
00
00
ENDCHAR
STARTCHAR Igrave
ENCODING 204
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
20
10
00
38
10
10
10
10
10
10
38
00
00
00
ENDCHAR
STARTCHAR Iacute
ENCODING 205
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
08
10
00
38
10
10
10
10
10
10
38
00
00
00
ENDCHAR
STARTCHAR Icircumflex
ENCODING 206
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
18
24
00
38
10
10
10
10
10
10
38
00
00
00
ENDCHAR
STARTCHAR Idieresis
ENCODING 207
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
44
44
00
38
10
10
10
10
10
10
38
00
00
00
ENDCHAR
STARTCHAR Eth
ENCODING 208
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
78
44
42
42
F2
42
42
44
78
00
00
00
ENDCHAR
STARTCHAR Ntilde
ENCODING 209
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
32
4C
00
62
62
52
52
4A
4A
46
46
00
00
00
ENDCHAR
STARTCHAR Ograve
ENCODING 210
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
10
08
3C
42
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR Oacute
ENCODING 211
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
08
10
3C
42
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR Ocircumflex
ENCODING 212
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
18
24
00
3C
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR Otilde
ENCODING 213
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
32
4C
00
3C
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR Odieresis
ENCODING 214
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
24
24
00
3C
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR multiply
ENCODING 215
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
00
42
24
18
24
42
00
00
00
00
ENDCHAR
STARTCHAR Oslash
ENCODING 216
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
02
3A
44
46
4A
4A
52
52
62
22
5C
40
00
00
ENDCHAR
STARTCHAR Ugrave
ENCODING 217
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
10
08
42
42
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR Uacute
ENCODING 218
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
08
10
42
42
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR Ucircumflex
ENCODING 219
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
18
24
00
42
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR Udieresis
ENCODING 220
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
24
24
00
42
42
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR Yacute
ENCODING 221
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
08
10
82
82
44
44
28
10
10
10
10
00
00
00
ENDCHAR
STARTCHAR Thorn
ENCODING 222
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
40
40
7C
42
42
42
42
7C
40
40
00
00
00
ENDCHAR
STARTCHAR germandbls
ENCODING 223
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
38
44
44
48
7C
42
42
42
62
5C
00
00
00
ENDCHAR
STARTCHAR agrave
ENCODING 224
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
08
00
3C
02
3E
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR aacute
ENCODING 225
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
08
10
00
3C
02
3E
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR acircumflex
ENCODING 226
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
18
24
00
3C
02
3E
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR atilde
ENCODING 227
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
32
4C
00
3C
02
3E
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR adieresis
ENCODING 228
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
24
24
00
3C
02
3E
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR aring
ENCODING 229
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
18
24
18
3C
02
3E
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR ae
ENCODING 230
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
6C
12
72
9E
90
90
6C
00
00
00
ENDCHAR
STARTCHAR ccedilla
ENCODING 231
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
3C
42
40
40
40
42
3C
10
20
00
ENDCHAR
STARTCHAR egrave
ENCODING 232
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
08
00
3C
42
42
7E
40
40
3E
00
00
00
ENDCHAR
STARTCHAR eacute
ENCODING 233
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
08
10
00
3C
42
42
7E
40
40
3E
00
00
00
ENDCHAR
STARTCHAR ecircumflex
ENCODING 234
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
18
24
00
3C
42
42
7E
40
40
3E
00
00
00
ENDCHAR
STARTCHAR edieresis
ENCODING 235
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
24
24
00
3C
42
42
7E
40
40
3E
00
00
00
ENDCHAR
STARTCHAR igrave
ENCODING 236
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
20
10
00
70
10
10
10
10
10
1C
00
00
00
ENDCHAR
STARTCHAR iacute
ENCODING 237
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
08
10
00
70
10
10
10
10
10
1C
00
00
00
ENDCHAR
STARTCHAR icircumflex
ENCODING 238
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
30
48
00
70
10
10
10
10
10
1C
00
00
00
ENDCHAR
STARTCHAR idieresis
ENCODING 239
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
48
48
00
70
10
10
10
10
10
1C
00
00
00
ENDCHAR
STARTCHAR eth
ENCODING 240
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
28
10
28
3C
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR ntilde
ENCODING 241
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
32
4C
00
7C
42
42
42
42
42
42
00
00
00
ENDCHAR
STARTCHAR ograve
ENCODING 242
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
08
00
3C
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR oacute
ENCODING 243
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
08
10
00
3C
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR ocircumflex
ENCODING 244
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
18
24
00
3C
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR otilde
ENCODING 245
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
32
4C
00
3C
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR odieresis
ENCODING 246
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
24
24
00
3C
42
42
42
42
42
3C
00
00
00
ENDCHAR
STARTCHAR divide
ENCODING 247
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
00
10
10
00
7C
00
10
10
00
00
00
ENDCHAR
STARTCHAR oslash
ENCODING 248
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
00
00
02
3C
46
4A
52
62
42
BC
00
00
00
ENDCHAR
STARTCHAR ugrave
ENCODING 249
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
10
08
00
42
42
42
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR uacute
ENCODING 250
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
08
10
00
42
42
42
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR ucircumflex
ENCODING 251
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
18
24
00
42
42
42
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR udieresis
ENCODING 252
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
24
24
00
42
42
42
42
42
46
3A
00
00
00
ENDCHAR
STARTCHAR yacute
ENCODING 253
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
08
10
00
42
42
42
42
42
46
3A
02
02
3C
ENDCHAR
STARTCHAR thorn
ENCODING 254
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
40
40
40
7C
42
42
42
42
42
7C
40
40
00
ENDCHAR
STARTCHAR ydieresis
ENCODING 255
SWIDTH 411 0
DWIDTH 8 0
BBX 8 14 0 -3
BITMAP
00
24
24
00
42
42
42
42
42
46
3A
02
02
3C
ENDCHAR
ENDFONT`;

const parseBITMAP = (state, line, makeImageData) => {
    if (line != "BITMAP") {
        return state;
    }
    if (makeImageData == undefined) {
        return {
            type: "PARSEBITMAPLater",
            code: state.code,
            char: state.char,
            lines: [],
        };
    }
    return {
        type: "PARSEBITMAP",
        code: state.code,
        out: {
            imageData: makeImageData(8, 14),
            char: state.char,
        },
        lineIndex: 0,
    };
};

const parseENCODING = (state, line) => {
    if (!line.startsWith("ENCODING")) {
        throw new Error(`Expected Encoding! for char ${state.code}`);
    }
    const charCode = line.substring("ENCODING".length + 1);
    const maybeInt = parseInt(charCode);
    if (isNaN(maybeInt)) {
        throw new Error(`Expected encoding got ${charCode}. In Char ${state.code}`);
    }
    return {
        type: "BITMAP",
        char: String.fromCharCode(maybeInt),
        code: state.code,
    };
};

const parsePARSEBITMAP = (out_state, line, out_font) => {
    if (line == "ENDCHAR") {
        out_font[out_state.code] = out_state.out;
        return {
            type: "STARTCHAR",
        };
    }
    const bits = parseInt(line, 16);
    if (isNaN(bits)) {
        throw new Error(`expected a number in bdf but found ${line}. In char ${out_state.code}`);
    }
    for (let i = 0, index = out_state.lineIndex * 4 * 8; i < 8; i++, index += 4) {
        if (!(bits & (1 << (7 - i)))) {
            continue;
        }
        out_state.out.imageData.data[index + 3] = 255;
    }
    out_state.lineIndex++;
    return out_state;
};

const getValidCode = (code) => {
    if (alpha.test(code)) {
        return code.toUpperCase();
    }
    if (upperAlpha.test(code)) {
        return `capital${code}`;
    }
    switch (code) {
        case "at":
        case "greater":
        case "equal":
        case "less":
        case "percent":
        case "hyphen":
        case "plus":
        case "ampersand":
        case "numbersign":
        case "quotedbl":
        case "asterisk":
        case "asciicircum":
        case "copyright":
        case "grave":
        case "braceleft":
        case "backslash":
        case "slash":
        case "bar":
        case "braceright":
        case "asciitilde":
        case "underscore":
        case "dollar":
        case "quotesingle":
        case "parenright":
        case "parenleft":
        case "exclam":
        case "bracketleft":
        case "bracketright":
        case "question":
        case "zero":
        case "one":
        case "two":
        case "three":
        case "four":
        case "five":
        case "six":
        case "seven":
        case "eight":
        case "nine":
        case "period":
        case "colon":
        case "semicolon":
        case "comma":
            return code;
        default:
            return null;
    }
};
const alpha = /^[a-z]$/;
const upperAlpha = /^[A-Z]$/;

const parseSTARTCHAR = (state, line, font) => {
    if (!line.startsWith("STARTCHAR")) {
        return state;
    }
    const maybeCode = getValidCode(line.substring("STARTCHAR".length + 1));
    if (maybeCode == null) {
        return state;
    }
    if (font[maybeCode] != undefined) {
        return state;
    }
    return {
        type: "ENCODING",
        code: maybeCode,
    };
};

const parseBDF = ({ bdf, makeImageData }) => {
    const lines = bdf.split("\n");
    let bdfState = {
        type: "STARTCHAR",
    };
    const font = {};
    for (const line of lines) {
        switch (bdfState.type) {
            case "STARTCHAR":
                bdfState = parseSTARTCHAR(bdfState, line, font);
                continue;
            case "ENCODING":
                bdfState = parseENCODING(bdfState, line);
                continue;
            case "BITMAP":
                bdfState = parseBITMAP(bdfState, line, makeImageData);
                continue;
            case "PARSEBITMAP":
                bdfState = parsePARSEBITMAP(bdfState, line, font);
                continue;
        }
    }
    return font;
};

const animation = [0, 1, 2, 3, 3, 2];
class BackgroundImage {
    constructor() {
        this.x = 0;
        this.y = 0;
        this.scaleX = 2;
        this.scaleY = 2;
        this.lastTime = 0;
        this.animationTime = 0;
        this.frame = 0;
        this.mouse = null;
        this.mouseK = -50;
        this.mouseI = -50;
        this.playAnimation = false;
        this.updateStateAndDraw = (totalTimeElapsed) => {
            const deltaTime = totalTimeElapsed - this.lastTime;
            this.lastTime = totalTimeElapsed;
            if (!this.playAnimation) {
                requestAnimationFrame(this.updateStateAndDraw);
                return;
            }
            this.updateState(deltaTime);
            this.draw();
            requestAnimationFrame(this.updateStateAndDraw);
        };
        this.updateState = (deltaTime) => {
            this.animationTime += deltaTime;
            if (this.animationTime >= 160) {
                this.animationTime = 0;
                this.frame++;
                if (this.frame >= animation.length) {
                    this.frame = 0;
                }
            }
            const velocity = deltaTime * 0.04;
            this.x += velocity;
            if (this.x >= 256) {
                this.x -= 256;
            }
            this.y += velocity;
            if (this.y >= 128) {
                this.y -= 128;
            }
            if (!this.mouse) {
                return;
            }
            this.mouseK = Math.floor((this.mouse.clientY - this.y) / 64);
            this.mouseI = Math.floor((this.mouse.clientX - this.x) / 128);
        };
        this.draw = () => {
            this.context.clearRect(0, 0, this.width, this.height);
            const logoFrame = this.codeRelayLogo[animation[this.frame]];
            const alternateLogoFrame = this.codeRelayLogo[animation[(this.frame + 3) % animation.length]];
            const numberOfColumns = this.width / this.scaleX / 128 + 1;
            for (let k = -2; k < this.height / this.scaleY / 64 + 1; k++) {
                const mouseRow = this.mouseK == k;
                for (let i = -2; i < numberOfColumns; i++) {
                    const image = i % 2
                        ? k % 2
                            ? this.fontemonLogo
                            : alternateLogoFrame
                        : k % 2
                            ? logoFrame
                            : this.fontemonLogo;
                    if (mouseRow && this.mouse && i == this.mouseI) {
                        this.context.drawImage(image, this.x + i * 128 - 32, this.y + k * 64 - 16, 192, 96);
                        continue;
                    }
                    this.context.drawImage(image, this.x + i * 128, this.y + k * 64);
                }
            }
            if (!this.mouse) {
                return;
            }
        };
        this.setupMouseAndTouchListeners = () => {
            window.addEventListener("mousemove", ({ clientX, clientY }) => {
                this.mouse = setupTouch({
                    clientX: clientX / this.scaleX,
                    clientY: clientY / this.scaleY,
                    input: this.mouse ?? undefined,
                });
            }, false);
            document
                .getElementById("toggle-animation")
                .addEventListener("click", () => {
                this.playAnimation = !this.playAnimation;
                try {
                    localStorage.setItem("play-animation", this.playAnimation ? "true" : "");
                    if (!this.playAnimation) {
                        this.context.clearRect(0, 0, this.width, this.height);
                    }
                }
                catch (err) { }
                console.log(this.playAnimation);
            });
        };
        const ratio = window.devicePixelRatio || 1;
        this.width = window.innerWidth > 0 ? window.innerWidth : screen.width;
        this.height = window.innerHeight > 0 ? window.innerHeight : screen.height;
        const maybeContext = makeAnimationCanvas(this.width, this.height, ratio);
        if (!maybeContext) {
            throw new Error("Could not make Animation canvas");
        }
        this.context = maybeContext.context;
        this.context.scale(this.scaleX, this.scaleY);
        this.context.imageSmoothingEnabled = false;
        this.fontemonLogo = document.getElementById("fontemon");
        this.codeRelayLogo = [...new Array(4).keys()].map((i) => document.getElementById(`code-relay-0${i + 1}`));
        try {
            if (matchMedia("(prefers-reduced-motion)").matches) {
                this.playAnimation = false;
            }
            else {
                const shouldPlayAnimation = localStorage.getItem("play-animation");
                this.playAnimation =
                    shouldPlayAnimation ? true : false;
            }
        }
        catch (err) { }
        this.setupMouseAndTouchListeners();
        requestAnimationFrame(this.updateStateAndDraw);
    }
}
const setupTouch = ({ clientX, clientY, input: maybeInput, }) => {
    const touchWidth = 20;
    const input = maybeInput ?? {
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
        clientX: 0,
        clientY: 0,
        difference: null,
        frameValid: false,
    };
    if (input) {
        input.difference = {
            x: clientX - input.clientX,
            y: clientY - input.clientY,
        };
    }
    input.clientX = clientX;
    input.clientY = clientY;
    input.left = clientX - touchWidth;
    input.right = clientX + touchWidth;
    input.top = clientY - touchWidth;
    input.bottom = clientY + touchWidth;
    return input;
};
const animationCanvasId = "animation-canvas";
const makeAnimationCanvas = (width, height, ratio) => {
    {
        const canvas = document.getElementById(animationCanvasId);
        if (canvas) {
            const context = canvas.getContext("2d");
            if (!context) {
                return null;
            }
            return {
                canvas,
                context,
            };
        }
    }
    const canvas = makeAnimationCanvasElement(width, height, ratio);
    document.body.appendChild(canvas);
    const context = canvas.getContext("2d");
    if (!context) {
        return null;
    }
    context?.scale(ratio, ratio);
    return {
        canvas,
        context,
    };
};
const makeAnimationCanvasElement = (width, height, ratio) => {
    const canvas = document.createElement("canvas");
    canvas.id = animationCanvasId;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    canvas.style.top = "0";
    canvas.style.left = "0";
    canvas.style.position = "fixed";
    canvas.style.pointerEvents = "none";
    return canvas;
};

class PreviewTool {
    constructor() {
        this.parser = null;
        this.reticleBox = {
            x: -1,
            y: -1,
            width: -1,
            height: -1,
        };
        this.frameLeftBox = {
            x: 250,
            y: 100,
            width: 10,
            height: 10,
        };
        this.frameRightBox = {
            x: 270,
            y: 100,
            width: 10,
            height: 10,
        };
        this.error = null;
        this.frame = 0;
        this.max_frame = 0;
        this.lineState = lineStateEmpty;
        this.brokenLines = [];
        this.dragFrameState = "notDragging";
        this.mousePosition = {
            x: -1,
            y: -1,
        };
        this._text = "";
        this._spacing_x = 8;
        this._line_width = 17;
        this._bottom_line_distance = -10;
        this._textType = "word";
        this.saveSettings = () => {
            if (!this.localStorage) {
                return;
            }
            const storedProps = {
                bottom_line_distance: this.bottom_line_distance,
                line_width: this.line_width,
                spacing_x: this.spacing_x,
                text: this.text,
                textAreaHeight: this.textArea.style.height ?? `36px`,
                textAreaWidth: this.textArea.style.width ?? `163px`,
                textType: this.textType,
            };
            this.localStorage.setItem("storage", JSON.stringify(storedProps));
        };
        this.setupStateFromStoredProperties = () => {
            if (!this.localStorage) {
                return;
            }
            const storedPropertiesString = this.localStorage.getItem("storage");
            if (!storedPropertiesString) {
                return;
            }
            const storedProperties = JSON.parse(storedPropertiesString);
            this._text = storedProperties.text;
            this._spacing_x = storedProperties.spacing_x;
            this._line_width = storedProperties.line_width;
            this._bottom_line_distance = storedProperties.bottom_line_distance;
            this.textArea.value = this.text;
            this.textArea.style.height = storedProperties.textAreaHeight;
            this.textArea.style.width = storedProperties.textAreaWidth;
            this.textType = storedProperties.textType ?? "word";
            document.getElementById("spacing-x").value = this
                ._spacing_x;
            document.getElementById("line-width").value = this
                ._line_width;
            document.getElementById("bottom-line-height").value = this._bottom_line_distance;
            document.getElementById("word-based").checked =
                this.textType == "word";
            this.reParseLineState(true);
        };
        this.updateStateAndDraw = () => {
            this.updateState();
            this.draw();
            requestAnimationFrame(this.updateStateAndDraw);
        };
        this.updateState = () => {
            this.updateReticleBoxState();
            this.updateCursorState();
            if (this.dragFrameState != "dragging") {
                return;
            }
            this.setCurrentFrameToMouseXPosition();
        };
        this.updateCursorState = () => {
            if (this.dragFrameState == "dragging") {
                this.canvas.style.cursor = "grabbing";
                return;
            }
            if (isInBox(this.mousePosition, this.reticleBox)) {
                this.canvas.style.cursor = "grab";
                return;
            }
            if (this.mouseIsOverFrame(this.mousePosition) ||
                [this.frameLeftBox, this.frameRightBox].some((box) => isInBox(this.mousePosition, box))) {
                this.canvas.style.cursor = "pointer";
                return;
            }
            this.canvas.style.cursor = "default";
            return;
        };
        this.updateReticleBoxState = () => {
            const left = this.frame * this.frameScale - 5;
            this.reticleBox.x = left;
            this.reticleBox.y = 120;
            this.reticleBox.width = 10;
            this.reticleBox.height = 10;
        };
        this.setCurrentFrameToMouseXPosition = () => {
            const oldFrame = this.frame;
            const draggedFrame = Math.min(Math.round((this.mousePosition.x + 5) / this.frameScale), this.max_frame);
            this.frame = draggedFrame;
            if (oldFrame == this.frame) {
                return;
            }
            this.lineState = getLineState(this.parser, this.frame);
        };
        this.draw = () => {
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.context.fillStyle = "black";
            if (this.error) {
                this.context.fillText(this.error, 0, 25);
            }
            else {
                this.drawLineOfText(this.lineState.top.line, this.lineState.top.drawCount, 25);
                this.drawLineOfText(this.lineState.bottom.line, this.lineState.bottom.drawCount, 25 + -1 * this.bottom_line_distance + 3);
            }
            const lineWidthPosition = this.line_width * this.spacing_x;
            this.context.fillRect(lineWidthPosition, 0, 2, 50);
            this.context.fillText(`Frame: ${this.frame}/${this.max_frame}`, 0, 115);
            this.context.fillText("←", this.frameLeftBox.x, this.frameLeftBox.y + 15);
            this.context.fillText("→", this.frameRightBox.x, this.frameRightBox.y + 15);
            for (let i = 0; i < this.max_frame; i++) {
                this.context.fillStyle = colors[i % colors.length];
                this.context.fillRect(this.frameScale * i, 130, this.frameScale, 10);
            }
            this.context.fillStyle = "#ff3b30";
            this.context.fillRect(this.reticleBox.x, this.reticleBox.y, this.reticleBox.width, this.reticleBox.height);
            this.drawLineBreaks(lineWidthPosition);
        };
        this.drawLineBreaks = (lineWidthPosition) => {
            if (this.brokenLines.length <= 0) {
                return;
            }
            this.context.fillStyle = "black";
            const plural = this.brokenLines.length > 1 ? "s" : "";
            this.context.fillText(`${this.brokenLines.length} line break${plural}`, lineWidthPosition + 15, 15);
            this.context.fillText(`Line${plural}: ` + this.brokenLines.join(" "), lineWidthPosition + 15, 35);
        };
        this.drawLineOfText = (line, drawCount, y) => {
            for (let i = 0; i < drawCount; i++) {
                const character = line[i];
                if (character == " ") {
                    continue;
                }
                const glyphInfo = this.font[character];
                if (!glyphInfo) {
                    this.error = `Unrecognized character ${character}`;
                    continue;
                }
                this.context.putImageData(glyphInfo.imageData, i * this.spacing_x, y);
            }
        };
        this.parseNewLines = (text) => {
            if (!text) {
                this.lineState = lineStateEmpty;
                return;
            }
            const parser = this.textType == "word" ? new WordParseState() : new ParseState();
            const output = parseText(text, this.line_width, this.charToCode, parser);
            if (!output) {
                this.parser = parser;
                this.error = null;
                return;
            }
            this.parser = null;
            this.error = output.error;
        };
        this.reParseLineState = (trackFrame) => {
            if (!this.text) {
                this.lineState = lineStateEmpty;
                return;
            }
            this.brokenLines = this.text
                .replace(/\\./g, " ")
                .split("\n")
                .reduce((o, line, index) => {
                if (line.length <= this.line_width) {
                    return o;
                }
                o.push(index + 1);
                return o;
            }, []);
            this.parseNewLines(this.text);
            this.max_frame = getMaxFrame(this.parser);
            if (trackFrame) {
                this.frame = this.max_frame;
            }
            else if (this.frame >= this.max_frame) {
                this.frame = this.max_frame;
            }
            this.lineState = getLineState(this.parser, this.frame);
        };
        this.mouseIsOverFrame = ({ y }) => {
            return y >= 130 && y < 130 + 10;
        };
        this.previousFrame = () => {
            this.frame = Math.max(this.frame - 1, 0);
            this.lineState = getLineState(this.parser, this.frame);
        };
        this.nextFrame = () => {
            this.frame = Math.min(this.frame + 1, this.max_frame);
            this.lineState = getLineState(this.parser, this.frame);
        };
        this.setupMouseAndTouchListeners = () => {
            this.textArea.addEventListener("input", () => {
                const text = this.textArea.value;
                const newText = text.replaceAll(/\\n/g, "\n");
                this.textArea.value = newText;
                this.text = newText;
                this.reParseLineState(this.trackFrame);
            });
            document
                .getElementById("transform-button")
                .addEventListener("click", () => {
                const outputText = parserToString(this.parser, this.font);
                navigator.clipboard.writeText(outputText).then(() => {
                    document.getElementById("copied").innerText = "Copied";
                });
            });
            {
                const spacingInput = document.getElementById("spacing-x");
                spacingInput.addEventListener("input", () => {
                    this.spacing_x = spacingInput.value;
                });
            }
            {
                const lineWidthInput = document.getElementById("line-width");
                lineWidthInput.addEventListener("input", () => {
                    this.line_width = Math.floor(lineWidthInput.value);
                    this.reParseLineState(this.trackFrame);
                });
            }
            {
                const bottomLinInput = document.getElementById("bottom-line-height");
                bottomLinInput.addEventListener("input", () => {
                    this.bottom_line_distance = bottomLinInput.value;
                });
            }
            this.canvas.addEventListener("mousemove", ({ offsetX, offsetY }) => {
                this.mousePosition = {
                    x: offsetX,
                    y: offsetY,
                };
            });
            {
                const wordBasedCheckbox = document.getElementById("word-based");
                wordBasedCheckbox.addEventListener("input", () => {
                    console.log("tacos");
                    this.textType = wordBasedCheckbox.checked ? "word" : "character";
                    this.reParseLineState(this.trackFrame);
                });
            }
            this.canvas.addEventListener("mousedown", ({ offsetX, offsetY }) => {
                const position = {
                    x: offsetX,
                    y: offsetY,
                };
                if (isInBox(position, this.reticleBox)) {
                    this.dragFrameState = "dragging";
                    return;
                }
                if (isInBox(position, this.frameLeftBox)) {
                    this.previousFrame();
                    return;
                }
                if (isInBox(position, this.frameRightBox)) {
                    this.nextFrame();
                    return;
                }
                if (this.mouseIsOverFrame(position)) {
                    this.setCurrentFrameToMouseXPosition();
                    return;
                }
            });
            window.addEventListener("keydown", ({ key }) => {
                if (document.activeElement != null &&
                    document.activeElement != document.body) {
                    return;
                }
                switch (key) {
                    case "ArrowLeft":
                        this.previousFrame();
                        return;
                    case "ArrowRight":
                        this.nextFrame();
                        return;
                    default:
                        return;
                }
            });
            window.addEventListener("mouseup", () => {
                this.dragFrameState = "notDragging";
            });
            try {
                const observer = new ResizeObserver(() => {
                    this.saveSettings();
                });
                observer.observe(this.textArea);
            }
            catch (err) { }
        };
        this.canvas = document.getElementById("canvas");
        this.context = this.canvas.getContext("2d");
        this.textArea = document.getElementById("area");
        this.setupMouseAndTouchListeners();
        const font = parseBDF({
            bdf: gohuFont,
            makeImageData: (w, h) => new ImageData(w, h),
        });
        this.font = font;
        this.charToCode = {};
        for (const [code, { char }] of Object.entries(font)) {
            this.charToCode[char] = (this.charToCode[char] ?? []).concat([code]);
        }
        this.context.font = "18px pressStart";
        try {
            this.localStorage = localStorage;
            this.setupStateFromStoredProperties();
        }
        catch (err) {
            this.localStorage = null;
        }
        requestAnimationFrame(this.updateStateAndDraw);
    }
    get text() {
        return this._text;
    }
    set text(newValue) {
        this._text = newValue;
        this.saveSettings();
    }
    get spacing_x() {
        return this._spacing_x;
    }
    set spacing_x(newValue) {
        this._spacing_x = newValue;
        this.saveSettings();
    }
    get line_width() {
        return this._line_width;
    }
    set line_width(newValue) {
        this._line_width = newValue;
        this.saveSettings();
    }
    get bottom_line_distance() {
        return this._bottom_line_distance;
    }
    set bottom_line_distance(newValue) {
        this._bottom_line_distance = newValue;
        this.saveSettings();
    }
    get textType() {
        return this._textType;
    }
    set textType(newValue) {
        this._textType = newValue;
        this.saveSettings();
    }
    get frameScale() {
        if (this.max_frame < 79) {
            return 5;
        }
        return 395 / this.max_frame;
    }
    get trackFrame() {
        return this.frame == this.max_frame;
    }
}
window.onload = () => {
    new PreviewTool();
    new BackgroundImage();
};
