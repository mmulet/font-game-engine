// import { SaveFileInput } from "api";
import { SaveFileInput } from "./SaveFileInput.js";
import { Request, Response } from "express";
import { writeFile } from "fs/promises";
import { join, basename } from "path";
import { directories } from "project-directories";
export const saveFile = async (request: Request, response: Response) => {
  const {
    pngURL,
    charStringInfo,
    name: nameOrPath,
  } = request.body as SaveFileInput;
  const comma = pngURL.indexOf(",");
  if (comma < 0) {
    throw new Error(`invalid data url`);
  }
  const name = basename(nameOrPath);
  const buf = Buffer.from(unescape(pngURL.substring(comma + 1)), "base64");
  await Promise.all([
    writeFile(join(directories.images.path, name + ".png"), buf),
    writeFile(
      join(directories.images.charStrings, name + ".charstring"),
      charStringInfo
    ),
  ]);
  response.sendStatus(200);
  return;
};
