import { Color } from "./Color.js";
import { defaultColors } from "./defaultColors.js";
import { UIColor } from "./UIColor.js";

export interface OutputColors {
  readonly black: Readonly<UIColor>;
  readonly transparent: Readonly<UIColor>;
  readonly lightGray: Readonly<UIColor>;
  readonly darkGray: Readonly<UIColor>;
}
export const colors: {
  [k in keyof OutputColors]: Color[];
} = defaultColors

export const outputColors: OutputColors = {
  black: {
    style: "#000000",
    color: colors.black[0],
    position: {
      x: 0,
      y: 45,
      width: 20,
      height: 5,
    },
  },
  transparent: {
    style: "#ffffff",
    color: colors.transparent[0],
    position: {
      x: 0,
      y: 65,
      width: 20,
      height: 5,
    },
  },
  lightGray: {
    style: "#a8a8a8ff",
    color: colors.lightGray[0],
    position: {
      x: 0,
      y: 85,
      width: 20,
      height: 5,
    },
  },
  darkGray: {
    style: "#606060ff",
    color: colors.darkGray[0],
    position: {
      x: 0,
      y: 105,
      width: 20,
      height: 5,
    },
  },
};

export const outputColorList: [
  keyof OutputColors,
  Readonly<UIColor>
][] = Object.entries(outputColors) as any;

