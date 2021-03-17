import { changeExtension } from "./changeExtension.js";

export const extensionToCharString = (filename: string) =>
  changeExtension(filename, "charstring");
