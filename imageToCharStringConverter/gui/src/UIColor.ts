import { Color } from "./Color.js";

export interface UIColor {
  color: Color;
  style: string;
  position: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}
