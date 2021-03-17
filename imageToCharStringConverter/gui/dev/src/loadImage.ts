import { Request, Response } from "express";
import { LoadImageInput } from "./LoadImageInput.js";

export const loadImage = async (request: Request, response: Response) => {
  const { filePath } = request.body as LoadImageInput;
  response.sendFile(filePath, (err) => {
    if (!err) {
      return;
    }
    response
      .status(418)
      .send(`Error\n Could not load ${filePath}\n ${err?.message}`);
  });
};
