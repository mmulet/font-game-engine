import { outputColors, OutputColors } from "./OutputColors.js";
import { UIColor } from "./UIColor.js";

export const replaceInputColorWithOutputColor = (
  outputColorKey: keyof OutputColors,
  imageData: ImageData,
  oldColor: UIColor
) => {
  const { data, width, height } = imageData;
  const outputColor = outputColors[outputColorKey];
  for (let i = 0; i < width * height * 4; i += 4) {
    let colorMatch = false;
    for (let g = 0; g < 4; g++) {
      if (oldColor.color[g] != data[i + g]) {
        colorMatch = false;
        break;
      }
      colorMatch = true;
    }
    if (!colorMatch) {
      continue;
    }
    for (let g = 0; g < 4; g++) {
      data[i + g] = outputColor.color[g];
    }
  }
 
};
