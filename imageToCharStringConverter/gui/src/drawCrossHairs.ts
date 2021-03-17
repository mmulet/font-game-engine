import { MousePosition } from "./MousePosition.js";
import { mousePositionToPixelPosition } from "./mousePositionToPixelPosition.js";

export const drawCrossHairs = (
  context: CanvasRenderingContext2D,
  control: "mouse" | "keyboard",
  mousePosition: MousePosition,
  keyboardPosition: MousePosition,
  leftBound: number,
  topBound: number
) => {
  const { x, y } =
    control == "mouse"
      ? mousePositionToPixelPosition(mousePosition, leftBound, topBound)
      : keyboardPosition;
  if (x >= 0 && y >= 0) {
    context.fillStyle = "red";
    context.fillRect(leftBound, y + topBound, x, 2);
    context.fillRect(x + leftBound, topBound, 2, y);
  }
};
