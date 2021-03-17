import { outputColorList } from "./OutputColors.js";
import { UIColor } from "./UIColor.js";
import { Selection } from "./Selection.js";

export const selectMatchingColor = (
  pixels: Uint8ClampedArray,
  i: number,
  currentColors: UIColor[]
): Selection | null => {
  for (let k = 0; k < currentColors.length; k++) {
    const { color } = currentColors[k];
    let colorMatch = false;
    for (let g = 0; g < 4; g++) {
      if (color[g] != pixels[i + g]) {
        colorMatch = false;
        break;
      }
      colorMatch = true;
    }
    if (colorMatch) {
      return {
        type: "highlighted",
        inputColorIndex: k,
      };
    }
  }
  for (const [name, { color }] of outputColorList) {
    let colorMatch = false;
    for (let g = 0; g < 4; g++) {
      if (color[g] != pixels[i + g]) {
        colorMatch = false;
        break;
      }
      colorMatch = true;
    }
    if (colorMatch) {
      return {
        type: "output_highlighted",
        outputColor: name as any,
      };
    }
  }
  return null;
};
