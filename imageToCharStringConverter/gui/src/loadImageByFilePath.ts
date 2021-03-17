import { blobToImageData } from "./blobToImageData.js";
import { LoadImageInput } from "./LoadImageInput.js";
import { loadImagePath } from "./loadImagePath.js";

export const loadImageByFilePath = async (filePath: string) => {
  const input: LoadImageInput = {
    filePath,
  };
  const response = await fetch(
    new Request(loadImagePath, {
      method: "POST",
      body: JSON.stringify(input),
    })
  );
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return blobToImageData(await response.blob());
};
