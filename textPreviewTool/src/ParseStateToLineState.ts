import { ParseState } from "./parseText";

export class ParseStateToLineState {
  lines: ParseState["parsed_text"];
  current_frame: number;
  constructor(lines: ParseState["parsed_text"], current_frame: number) {
    this.lines = lines;
    this.current_frame = current_frame;
  }

  static toLine = (line: string[]) => line;

  toLine = ParseStateToLineState.toLine;

  static toCharacterCount = (_line: string[], kThWord: number) => kThWord + 1;
  toCharacterCount = ParseStateToLineState.toCharacterCount;
  static lengthOfCharacterInLine = (line: string[]) => line.length;
  lengthOfCharacterInLine = ParseStateToLineState.lengthOfCharacterInLine;
}
