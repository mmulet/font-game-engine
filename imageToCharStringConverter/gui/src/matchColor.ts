import { Color } from "./Color.js";
import { colorEqual } from "./colorEqual.js";
import { Colors } from "./Colors.js";

export interface MatchColorInput {
  readonly colors: Colors;
  readonly color: Color;
}

export const transparent = Symbol("transparent");
export const noMatch = Symbol("noMatch");

export const matchColor = ({
  colors: { transparent: transparentColor, lightGray, darkGray, black },
  color,
}: MatchColorInput): typeof transparent | typeof noMatch | 0 | 1 | 2 => {
  const isEqualToColor = (c: Color) => colorEqual(c, color);
  if (transparentColor.some(isEqualToColor)) {
    return transparent;
  }
  if (black.some(isEqualToColor)) {
    return 0;
  }
  if (darkGray.some(isEqualToColor)) {
    return 1;
  }
  if (lightGray.some(isEqualToColor)) {
    return 2;
  }
  return noMatch;
};
