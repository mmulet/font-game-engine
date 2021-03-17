import { BDFState, PARSEBITMAP } from "./BDFState.js";
import { Font } from "./Font.js";

export const parsePARSEBITMAP = (
  out_state: PARSEBITMAP,
  line: string,
  out_font: Font
): BDFState => {
  if (line == "ENDCHAR") {
    out_font[out_state.code] = out_state.out;
    return {
      type: "STARTCHAR",
    };
  }
  const bits = parseInt(line, 16);
  if (isNaN(bits)) {
    throw new Error(
      `expected a number in bdf but found ${line}. In char ${out_state.code}`
    );
  }
  /**
   * 4 bytes per pixel. 8 pixels per line
   */
  for (let i = 0, index = out_state.lineIndex * 4 * 8; i < 8; i++, index += 4) {
    if (!(bits & (1 << (7 - i)))) {
      continue;
    }
    /**
     * 4th pixel is the alpha channel
     */
    out_state.out.imageData.data[index + 3] = 255;
  }
  out_state.lineIndex++;
  return out_state;
};
