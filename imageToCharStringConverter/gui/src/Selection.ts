import { OutputColors } from "./OutputColors.js";

export type Selection =
  | { type: "none" }
  | {
      inputColorIndex: number;
      type: "highlighted";
    }
  | {
      inputColorIndex: number;
      type: "selected";
    }
  | {
      outputColor: keyof OutputColors;
      type: "output_highlighted";
    };
