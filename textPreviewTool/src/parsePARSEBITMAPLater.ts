import { BDFState, PARSEBITMAPLater } from "./BDFState.js";
import { FontInfo } from "./Font.js";
/**
 *
 *   Parse the BITMAP later, save the lines for now
 */
export const parsePARSEBITMAPLater = (
  out_state: PARSEBITMAPLater,
  line: string,
  out_font: FontInfo
): BDFState => {
  if (line == "ENDCHAR") {
    out_state.lines.push(line);
    out_font[out_state.code] = {
      char: out_state.char,
      bitmapBDFLines: out_state.lines,
    };
    return {
      type: "STARTCHAR",
    };
  }
  out_state.lines.push(line);
  return out_state;
};
