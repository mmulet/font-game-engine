import { BDFState } from "./BDFState.js";
import { Font } from "./Font.js";
import { MakeImageData } from "./MakeImageData.js";
import { parseBITMAP } from "./parseBITMAP.js";
import { parseENCODING } from "./parseENCODING.js";
import { parsePARSEBITMAP } from "./parsePARSEBITMAP.js";
import { parseSTARTCHAR } from "./parseSTARTCHAR.js";

export interface Input {
  readonly bdf: string;
  readonly makeImageData: MakeImageData;
}

/**
 *
 * a simple bdf parser. Not guaranteed to work with all bdfs
 * just the one I have included.
 */
export const parseBDF = ({ bdf, makeImageData }: Input) => {
  const lines = bdf.split("\n");
  let bdfState: BDFState = {
    type: "STARTCHAR",
  };
  const font: Font = {};
  for (const line of lines) {
    switch (bdfState.type) {
      case "STARTCHAR":
        bdfState = parseSTARTCHAR(bdfState, line, font);
        continue;
      case "ENCODING":
        bdfState = parseENCODING(bdfState, line);
        continue;

      case "BITMAP":
        bdfState = parseBITMAP(bdfState, line, makeImageData);
        continue;
      case "PARSEBITMAP":
        bdfState = parsePARSEBITMAP(bdfState, line, font);
        continue;
    }
  }
  return font;
};
