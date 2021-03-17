import { ImageDataToCharStringInput } from "./imageDataToCharString";
import { ImagePixel } from "./ImagePixel";
import { matchColor, noMatch, transparent } from "./matchColor.js";

export const getImageDataInfo = ({
  imageData: { width, height, data },
  colors,
}: ImageDataToCharStringInput) => {
  const bitWidth = 4;
  const stride = bitWidth * width;
  const notBlankPixels: ImagePixel[] = [];
  for (let k = 0; k < height; k += 1) {
    for (let i = k * stride; i < (k + 1) * stride; i += 4) {
      const r = data[i]!;
      const g = data[i + 1]!;
      const b = data[i + 2]!;
      const a = data[i + 3]!;
      const color = matchColor({
        colors,
        color: [r, g, b, a],
      });
      switch (color) {
        case transparent:
          continue;
        case noMatch:
          throw new Error(`Unrecognized color ${[r, g, b, a]}`);
        default:
          break;
      }
      notBlankPixels.push({
        x: (i % stride) / 4,
        y: k,
        color,
      });
    }
  }
  return notBlankPixels;
};
