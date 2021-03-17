import { Font, FontInfo } from "./Font";

/**
 *
 * An inverse of font, a map from characters to codes
 */
export const getCharToCode = (font: FontInfo | Font) => {
  const charToCode: CharToCode = {};
  for (const [code, { char }] of Object.entries(font)) {
    charToCode[char] = (charToCode[char] ?? []).concat([code]);
  }
  return charToCode;
};

export interface CharToCode {
  [char: string]: string[] | undefined;
}
