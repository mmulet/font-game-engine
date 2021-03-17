import { Color } from "./Color.js";
import { outputColorList, OutputColors } from "./OutputColors.js";
import { UIColor } from "./UIColor.js";
import { yPositionCurrentColor } from "./yPositionCurrentColor.js";

export const getAllColorsFromAnImage = (
  { data, width, height }: ImageData,
  skipOutputVersion: boolean
): {
  inputColors: UIColor[];
  outputColors: Set<keyof OutputColors>;
} => {
  const currentColors: UIColor[] = [];
  const outputColors: Set<keyof OutputColors> = new Set();
  for (let i = 0; i < width * height * 4; i += 4) {
    let colorMatch = false;
    for (let k = 0; k < currentColors.length; k++) {
      const { color } = currentColors[k];
      for (let g = 0; g < 4; g++) {
        if (color[g] != data[i + g]) {
          colorMatch = false;
          break;
        }
        colorMatch = true;
      }
      if (colorMatch) {
        break;
      }
    }
    if (colorMatch) {
      continue;
    }
    if (!skipOutputVersion) {
      for (const [outputColorName, { color }] of outputColorList) {
        for (let g = 0; g < 4; g++) {
          if (color[g] != data[i + g]) {
            colorMatch = false;
            break;
          }
          colorMatch = true;
        }
        if (colorMatch) {
          outputColors.add(outputColorName);
          break;
        }
      }
      if (colorMatch) {
        continue;
      }
    }

    const color = [data[i], data[i + 1], data[i + 2], data[i + 3]] as Color;
    currentColors.push({
      style: `#${color.map((a) => a.toString(16).padStart(2, "0")).join("")}`,
      color,
      position: {
        x: 10,
        y: yPositionCurrentColor(currentColors.length),
        width: 20,
        height: 5,
      },
    });
    /**
     * This is only supposed to work with lo-res pixel art style things
     * Large number of colors not supported
     */
    if (currentColors.length > 200) {
      break;
    }
  }
  return {
    inputColors: currentColors,
    outputColors,
  };
};
