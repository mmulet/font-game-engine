export type Output = {
  readonly error: string;
  readonly type: "error";
} | null;

const parse_char = (
  i: string,
  charToCode: { [string: string]: string[] | undefined }
) => {
  switch (i) {
    case "\n":
      return "newline";
    case "\\":
      return "newlineMaybe";
    case " ":
      return " ";
    default:
      break;
  }
  const maybe = charToCode[i];
  return maybe ? maybe[0] : null;
};

export interface LineParser {
  get_mightBeNewLine: () => boolean;
  set_mightBeNewLine: (m: boolean) => any;

  addLine: () => any;
  addChar: (char: string, width: number, skipSpace: boolean) => any;
  shouldSkipDoubleNewline: (width: number) => any;
  currentLineIsEmpty: () => boolean;
}

export type Parser = ParseState | WordParseState;

export class ParseState implements LineParser {
  type: "ParseState" = "ParseState";
  parsed_text: string[][] = [];
  current_line: string[] = [];
  mightBeNewLine = false;

  get_mightBeNewLine = () => this.mightBeNewLine;
  set_mightBeNewLine = (m: boolean) => {
    this.mightBeNewLine = m;
  };

  addLine = () => {
    this.parsed_text.push(this.current_line);
    this.current_line = [];
  };

  addChar = (char: string, width: number, _skipSpace = false) => {
    this.current_line.push(char);
    if (this.current_line.length < width) {
      return;
    }
    this.addLine();
  };

  /**
 * If there is a newline character directly following
 * a newline due to max width, ignore the second newline
 * @return true on removal
 * @example
 * width = 5
 * I enter
 * ```
 * tacos
 * bread
 * ```
 * Technically there are two new lines
 * 1. Caused by tacos being 5 letters
 * 2. Caused by the newline between tacos and bread
 * On the screen you would see this:
 * ```
 *
 * bread
 * ```
 * But I would expect the input to match the output.
 * I would want to see:
 * ```
 * tacos
 * bread
 * ```
 * So, we ignore the second newLine.
 *

 */
  shouldSkipDoubleNewline = (width: number) => {
    /**
     * Is not a blank line.
     */
    if (this.current_line.length > 0) {
      return false;
    }
    /**
     * No line above
     */
    if (this.parsed_text.length < 1) {
      return false;
    }
    const lineAbove = this.parsed_text[this.parsed_text.length - 1];
    /**
     * The line above was caused by a maxWidth, not a newline character
     */
    return lineAbove.length == width;
  };
  currentLineIsEmpty = () => this.current_line.length <= 0;
}

export class WordParseState implements LineParser {
  type: "WordParseState" = "WordParseState";

  parsed_text: string[][][] = [];
  current_line: string[][] = [];
  current_word: string[] = [];
  mightBeNewLine = false;

  get_mightBeNewLine = () => this.mightBeNewLine;
  set_mightBeNewLine = (m: boolean) => {
    this.mightBeNewLine = m;
  };

  addLine = () => {
    if (this.current_word.length > 0) {
      this.current_line.push(this.current_word);
      this.current_word = [];
    }
    this.parsed_text.push(this.current_line);
    this.current_line = [];
  };

  get lineWidth() {
    let length = this.lineLength(this.current_line);
    /**
     * space before current word
     */
    length +=
      this.current_line.length > 0 && this.current_word.length > 0 ? 1 : 0;
    length += this.current_word.length;
    return length;
  }

  lineLength = (line: string[][]) => {
    let length = 0;
    for (const word of line) {
      length += word.length;
    }
    /**
     * spaces between words
     */
    length += line.length - 1;
    return length;
  };

  addChar = (char: string, width: number, skipSpace = true) => {
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

  shouldSkipDoubleNewline = (width: number) => {
    /**
     * Is not a blank line.
     */
    if (this.current_line.length > 0 || this.current_word.length > 0) {
      return false;
    }
    /**
     * No line above
     */
    if (this.parsed_text.length < 1) {
      return false;
    }
    const lineAbove = this.parsed_text[this.parsed_text.length - 1];
    /**
     * The line above was caused by a maxWidth, not a newline character
     */

    return this.lineLength(lineAbove) == width;
  };
  currentLineIsEmpty = () => {
    return this.current_word.length <= 0 && this.current_line.length <= 0;
  };
}

/**
 * Parse text to text lines.
 * @sync with ./blender/fontemon_blender_addon/CreateText/parse_text.py
 */
export const parseText = (
  text: string,
  width: number,
  charToCode: { [string: string]: string[] | undefined },
  mutableState: LineParser
): Output => {
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
