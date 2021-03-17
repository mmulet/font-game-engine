import { Color } from "./Color.js";

export const drawColorDescription = (
  context: CanvasRenderingContext2D,
  color: Color,
  x: number,
  y: number
) => {
  context.fillStyle = "black";
  context.fillText(`Color Value: ${JSON.stringify(color)}`, x, y);
};
