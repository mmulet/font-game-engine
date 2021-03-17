import { Box } from "./Box";
import { MousePosition } from "./MousePosition";

export const isInBox = (
  { x, y }: MousePosition,
  { x: left, y: top, width, height }: Box
) => x >= left && x <= left + width && y >= top && y <= top + height;
