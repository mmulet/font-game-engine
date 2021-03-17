import { BDFState, BITMAP } from "./BDFState.js";
import { MakeImageData } from "./MakeImageData.js";

export const parseBITMAP = (
  state: BITMAP,
  line: string,
  makeImageData: MakeImageData | undefined
): BDFState => {
  if (line != "BITMAP") {
    return state;
  }
  if (makeImageData == undefined) {
    return {
      type: "PARSEBITMAPLater",
      code: state.code,
      char: state.char,
      lines: [],
    };
  }
  return {
    type: "PARSEBITMAP",
    code: state.code,
    out: {
      imageData: makeImageData(8, 14),
      char: state.char,
    },
    lineIndex: 0,
  };
};
