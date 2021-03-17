// import { nextFilePathHeader, NextImageInput } from "api";
import { Request, Response } from "express";
import { join, extname, basename, dirname } from "path";
import { NextImageInput, nextFilePathHeader  } from "./nextImageInput.js";

export const nextImage = async (request: Request, response: Response) => {
  const { imageFilePath } = request.body as NextImageInput;
  const extension = extname(imageFilePath);
  const name = basename(imageFilePath, extension);
  const result = /\d+$/.exec(name);
  if (result == null) {
    response.sendStatus(404);
    return;
  }
  const [numberString] = result;
  const number = parseInt(numberString);
  const nextNumber = number + 1;
  const nextFilePath = join(
    dirname(imageFilePath),
    name.substring(0, name.length - numberString.length) +
      nextNumber.toString().padStart(numberString.length, "0") +
      extension
  );
  response.setHeader(nextFilePathHeader, nextFilePath);
  response.sendFile(nextFilePath, (err) => {
    if (!err) {
      return;
    }
    response
      .status(418)
      .send(
        `Error\n Could not load the next image for ${imageFilePath}:\n${err?.message}`
      );
  });
};
