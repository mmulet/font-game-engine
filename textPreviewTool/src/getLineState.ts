import { LineState } from "./LineState";
import { ParseStateToLineState } from "./ParseStateToLineState";
import { Parser } from "./parseText";
import { WordParserToLineState } from "./WordParserToLineState";

export const getLineState = (
  parser: Parser | null,
  current_frame: number
): LineState => {
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
      return genericGetLineState(
        new ParseStateToLineState(parser.parsed_text, current_frame)
      );
    case "WordParseState":
      return genericGetLineState(
        new WordParserToLineState(parser.parsed_text, current_frame)
      );
  }
};

export interface Input<T> {
  lines: T[][];
  current_frame: number;
  toLine: (t: T[]) => string[];
  toCharacterCount: (t: T[], k: number) => number;
  lengthOfCharacterInLine: (t: T[]) => number;
}

export const genericGetLineState = <T>({
  lines,
  current_frame,
  toCharacterCount,
  toLine,
  lengthOfCharacterInLine,
}: Input<T>) => {
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
