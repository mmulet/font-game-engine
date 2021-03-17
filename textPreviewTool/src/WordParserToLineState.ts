import { WordParseState } from "./parseText";

export class WordParserToLineState {
  lines: WordParseState["parsed_text"];
  current_frame: number;
  constructor(lines: WordParseState["parsed_text"], current_frame: number) {
    this.lines = lines;
    this.current_frame = current_frame;
  }

  toLine = (line: string[][]) =>
    line.flatMap((a, index) => (index == 0 ? [] : [" "]).concat(a));

  toCharacterCount = (line: string[][], kThWord: number) => {
    let length = 0;
    if (line.length <= 0) {
      return 0;
    }
    for (let i = 0; i < kThWord + 1; i++) {
      if (i != 0) {
        /**
         * The space
         */
        length++;
      }
      /**
       * number of characters in the word
       */
      length += line[i].length;
    }
    return length;
  };

  lengthOfCharacterInLine = (line: string[][]) =>
    line.reduce(
      (out, word, index) => (index == 0 ? 0 : 1) + out + word.length,
      0
    );
}
