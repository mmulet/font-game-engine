import { codeToCharacter } from "./codeToCharacter";
import { Font } from "./Font";
import { Parser } from "./parseText";

export const parserToString = (parser: Parser | null, font: Font) => {
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
        .map((line) =>
          line
            .map((word) =>
              word.map((code) => codeToCharacter(font, code, true)).join("")
            )
            .join(" ")
        )
        .join("\\n");
  }
};
