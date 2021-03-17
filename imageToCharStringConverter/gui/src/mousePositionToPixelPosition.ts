import { MousePosition } from "./MousePosition.js";

export const mousePositionToPixelPosition = (
  mousePosition: MousePosition,
  leftBound: number,
  topBound: number
) => {
  const x = Math.floor(mousePosition.x - leftBound);
  const y = Math.floor(mousePosition.y - topBound);
  return {
    x,
    y,
  };
};
