import { UIColor } from "./UIColor.js";

export const drawStrokeBox = (
  context: CanvasRenderingContext2D,
  { x, y, width, height }: UIColor["position"],
  color: string
) => {
  context.strokeStyle = color;
  context.strokeRect(x - 2, y - 2, width + 4, height + 4);
};
