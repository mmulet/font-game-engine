import { Parser } from "./parseText";

export const getMaxFrame = (parser: Parser | null) => {
  if (!parser) {
    return 0;
  }
  switch (parser.type) {
    case "WordParseState":
      return Math.max(
        0,
        /**
         * number of frames -1
         * because frames is zero based
         */
        parser.parsed_text.reduce((o, line) => o + line.length, 0) - 1
      );
    case "ParseState":
      return parser.parsed_text.reduce((o, line) => o + line.length, 0);
  }
};
