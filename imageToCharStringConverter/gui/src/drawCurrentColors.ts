import { UIColor } from "./UIColor.js";

export const drawCurrentColors = (
  context: CanvasRenderingContext2D,
  currentColors: UIColor[]
) => {
  context.fillStyle = "black";
  context.fillText("Input Colors:", 0, 120);

  for (const [i, { style, position }] of currentColors.entries()) {
    context.fillStyle = "black";
    context.fillText(`${i}:`, position.x - 10, position.y + 5);

    context.fillStyle = style;
    context.fillRect(position.x, position.y, position.width, position.height);
  }
};
