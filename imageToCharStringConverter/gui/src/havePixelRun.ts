import { ImagePixel } from "./ImagePixel.js";

export interface HavePixelRunInput {
  pixel: ImagePixel;
  nextPixel: ImagePixel | undefined;
}
export const havePixelRun = ({ pixel, nextPixel }: HavePixelRunInput) => {
  if (nextPixel === undefined) {
    return false;
  }
  if (nextPixel.y !== pixel.y) {
    return false;
  }
  if (nextPixel.x !== pixel.x + 1) {
    return false;
  }
  return true;
};
