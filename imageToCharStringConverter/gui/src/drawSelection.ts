import { drawStrokeBox } from "./drawStrokeBox.js";
import { UIColor } from "./UIColor.js";
import { Selection } from "./Selection.js";
import { outputColors } from "./OutputColors.js";
import { drawColorDescription } from "./drawColorDescriptions.js";

export const drawSelection = (
  context: CanvasRenderingContext2D,
  selection: Selection,
  currentColors: UIColor[],
  colorDescriptionX: number,
  colorDescriptionY: number
) => {
  switch (selection.type) {
    case "none":
      return;
    case "highlighted": {
      const { position, color } = currentColors[selection.inputColorIndex];
      drawStrokeBox(context, position, "orange");
      drawColorDescription(
        context,
        color,
        colorDescriptionX,
        colorDescriptionY
      );
      return;
    }
    case "selected": {
      const { position, color } = currentColors[selection.inputColorIndex];
      drawStrokeBox(context, position, "red");
      drawColorDescription(
        context,
        color,
        colorDescriptionX,
        colorDescriptionY
      );
      return;
    }
    case "output_highlighted": {
      const { position, color } = outputColors[selection.outputColor];
      drawStrokeBox(context, position, "red");
      drawColorDescription(
        context,
        color,
        colorDescriptionX,
        colorDescriptionY
      );
      return;
    }
  }
};
