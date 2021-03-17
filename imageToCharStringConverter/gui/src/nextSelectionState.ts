import { MousePosition } from "./MousePosition.js";
import { mousePositionToPixelPosition } from "./mousePositionToPixelPosition.js";
import { Selection } from "./Selection.js";
import { selectMatchingColor } from "./selectMatchingColor.js";
import { UIColor } from "./UIColor.js";

export const nextSelectionState = (
  selection: Selection,
  imageData: ImageData | null,
  currentColors: UIColor[],
  control: "mouse" | "keyboard",
  mousePosition: MousePosition,
  keyboardPosition: MousePosition,
  leftBound: number,
  topBound: number
): Selection => {
  switch (selection.type) {
    case "selected":
      return selection;
  }
  if (!imageData) {
    return selection;
  }
  const { x, y } =
    control == "mouse"
      ? mousePositionToPixelPosition(mousePosition, leftBound, topBound)
      : keyboardPosition;
  if (x < 0 || y < 0 || x > imageData.width || y > imageData.height) {
    switch (selection.type) {
      case "highlighted":
      case "output_highlighted":
        return {
          type: "none",
        };
    }
    return selection;
  }
  const i = 4 * (x + y * imageData.width);
  const matchingState = selectMatchingColor(imageData.data, i, currentColors);
  if (matchingState == null) {
    return selection;
  }
  return matchingState;
};
