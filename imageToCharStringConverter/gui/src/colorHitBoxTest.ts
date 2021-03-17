import { MousePosition } from "./MousePosition.js";
import { outputColorList, OutputColors } from "./OutputColors.js";
import { UIColor } from "./UIColor.js";

export type HitBoxTestResult =
  | {
      inputColorIndex: number;
      type: "input";
    }
  | {
      name: keyof OutputColors;
      type: "output";
    }
  | {
      type: "none";
    };

export const colorHitBoxTest = (
  mousePosition: MousePosition,
  currentColors: UIColor[]
): HitBoxTestResult => {
  for (const [
    i,
    {
      position: { x, y, width, height },
    },
  ] of currentColors.entries()) {
    if (
      mousePosition.x >= x &&
      mousePosition.x <= x + width &&
      mousePosition.y >= y &&
      mousePosition.y <= y + height
    ) {
      return {
        inputColorIndex: i,
        type: "input",
      };
    }
  }

  for (const [
    outputType,
    {
      position: { x, y, width, height },
    },
  ] of outputColorList) {
    if (
      mousePosition.x >= x &&
      mousePosition.x <= x + width &&
      mousePosition.y >= y &&
      mousePosition.y <= y + height
    ) {
      return {
        name: outputType as any,
        type: "output",
      };
    }
  }
  return {
    type: "none",
  };
};
