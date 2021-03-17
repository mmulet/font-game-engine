import { Colors } from "./Colors.js";
import { matchColor, noMatch, transparent } from "./matchColor.js";

export const replaceImageDataWithGuessedColors = (
  { width, height, data }: ImageData,
  colors: Colors
) => {
  const bitWidth = 4;
  const stride = bitWidth * width;
  for (let k = 0; k < height; k++) {
    for (let i = k * stride; i < (k + 1) * stride; i += 4) {
      const r = data[i]!;
      const g = data[i + 1]!;
      const b = data[i + 2]!;
      const a = data[i + 3]!;
      switch (
        matchColor({
          colors,
          color: [r, g, b, a],
        })
      ) {
        case transparent:
          data[i] = 0;
          data[i + 1] = 0;
          data[i + 2] = 0;
          data[i + 3] = 0;
          continue;
        case noMatch:
          break;
        default:
          continue;
      }

      const color = 0;
      data[i] = color;
      data[i + 1] = color;
      data[i + 2] = color;
      data[i + 3] = 255;
    }
  }
};
