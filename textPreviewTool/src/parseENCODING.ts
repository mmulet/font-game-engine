import { BDFState, ENCODING } from "./BDFState.js";

export const parseENCODING = (state: ENCODING, line: string): BDFState => {
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
