import { outputColorList } from "./OutputColors.js";

export const drawOutputColors = (context: CanvasRenderingContext2D) => {
  context.fillStyle = "black";
  context.fillText("Output Colors:", 0, 0 + 15);

  for (const [
    name,
    {
      style,
      position: { x, y, width, height },
    },
  ] of outputColorList) {
    context.fillStyle = "black";
    context.fillText(name + ":", x, y - 5);
    context.fillStyle = style;
    context.fillRect(x, y, width, height);
  }
};
