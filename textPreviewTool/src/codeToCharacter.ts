import { Font } from "./Font";

export const codeToCharacter = (
  font: Font,
  code: string,
  escapeSpace: boolean
) => {
  switch (code) {
    case " ":
      return escapeSpace ? "\\ " : " ";
    case "backslash":
      return "\\\\";
    default:
      break;
  }
  const maybe = font[code];
  if (maybe == undefined) {
    return " ";
  }
  return maybe.char;
};
