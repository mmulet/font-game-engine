import { Color } from "./Color.js";

export const colorEqual = ([tr, tg, tb, ta]: Color, [r, g, b, a]: Color) =>
  tr === r && tg === g && tb === b && ta === a;
