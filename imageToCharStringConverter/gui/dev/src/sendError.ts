import { Request, Response } from "express";

export const sendError = (
  func: (request: Request, response: Response) => Promise<any>
) => (request: Request, response: Response) =>
  func(request, response).catch((e) =>
    response.status(418).send(`Error ${e?.message}`)
  );
