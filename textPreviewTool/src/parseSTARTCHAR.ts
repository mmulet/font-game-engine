import { BDFState, STARTCHAR } from "./BDFState.js";
import { Font, FontInfo } from "./Font.js";
import { getValidCode } from "./getValidCode.js";

export const parseSTARTCHAR = (
  state: STARTCHAR,
  line: string,
  font: FontInfo | Font
): BDFState => {
  if (!line.startsWith("STARTCHAR")) {
    return state;
  }
  const maybeCode = getValidCode(line.substring("STARTCHAR".length + 1));
  if (maybeCode == null) {
    return state;
  }
  /**
   * no duplicates
   */
  if (font[maybeCode] != undefined) {
    return state;
  }
  return {
    type: "ENCODING",
    code: maybeCode,
  };
};
