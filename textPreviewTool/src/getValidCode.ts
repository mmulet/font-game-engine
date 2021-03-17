export const getValidCode = (code: string) => {
  if (alpha.test(code)) {
    return code.toUpperCase();
  }
  if (upperAlpha.test(code)) {
    return `capital${code}`;
  }

  switch (code) {
    case "at":
    case "greater":
    case "equal":
    case "less":
    case "percent":
    case "hyphen":
    case "plus":
    case "ampersand":
    case "numbersign":
    case "quotedbl":
    case "asterisk":
    case "asciicircum":
    case "copyright":
    case "grave":
    case "braceleft":
    case "backslash":
    case "slash":
    case "bar":
    case "braceright":
    case "asciitilde":
    case "underscore":
    case "dollar":
    case "quotesingle":
    case "parenright":
    case "parenleft":
    case "exclam":
    case "bracketleft":
    case "bracketright":
    case "question":
    case "zero":
    case "one":
    case "two":
    case "three":
    case "four":
    case "five":
    case "six":
    case "seven":
    case "eight":
    case "nine":
    case "period":
    case "colon":
    case "semicolon":
    case "comma":
      return code;
    default:
      return null;
  }
};
const alpha = /^[a-z]$/;
const upperAlpha = /^[A-Z]$/;
