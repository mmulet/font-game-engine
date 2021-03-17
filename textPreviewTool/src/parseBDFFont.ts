import { BDFState } from "./BDFState.js";
import { Font, FontInfo } from "./Font.js";
import { MakeImageData } from "./MakeImageData.js";
import { parseBITMAP } from "./parseBITMAP.js";
import { parseENCODING } from "./parseENCODING.js";
import { parsePARSEBITMAP } from "./parsePARSEBITMAP.js";
import { parsePARSEBITMAPLater } from "./parsePARSEBITMAPLater.js";
import { parseSTARTCHAR } from "./parseSTARTCHAR.js";



/**
 *
 * a simple bdf parser. Not guaranteed to work with all bdfs
 * just the one I have included.
 */
export const parseBDFFont: {
  (bdf: string): FontInfo;
  (bdf: string, makeImageData: MakeImageData): Font;
} = (bdf: string, makeImageData: MakeImageData | undefined = undefined) => {
  const lines = bdf.split("\n");
  let bdfState: BDFState = {
    type: "STARTCHAR",
  };
  const fontInfo: FontInfo = {};
  const font: Font = {};
  for (const line of lines) {
    switch (bdfState.type) {
      case "STARTCHAR":
        bdfState = parseSTARTCHAR(
          bdfState,
          line,
          makeImageData == undefined ? fontInfo : font
        );
        continue;
      case "ENCODING":
        bdfState = parseENCODING(bdfState, line);
        continue;
      case "BITMAP":
        bdfState = parseBITMAP(bdfState, line, makeImageData);
        continue;
      case "PARSEBITMAPLater":
        bdfState = parsePARSEBITMAPLater(bdfState, line, fontInfo);
        continue;
      case "PARSEBITMAP":
        bdfState = parsePARSEBITMAP(bdfState, line, font);
        continue;
    }
  }
  return (makeImageData == undefined ? fontInfo : font) as any;
};
