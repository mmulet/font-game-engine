import { nextImagePath } from "./nextImagePath.js";
import { NextImageInput, nextFilePathHeader } from "./nextImageInput.js";
import { ImageInfo } from "./ImageInfo.js";
import { blobToImageData } from "./blobToImageData.js";

export const loadNextImageByFilePath = async (
  filePath: string
): Promise<ImageInfo> => {
  const input: NextImageInput = {
    imageFilePath: filePath,
  };

  const response = await fetch(
    new Request(nextImagePath, {
      method: "POST",
      body: JSON.stringify(input),
    })
  );
  const fileName = response.headers.get(nextFilePathHeader)!;
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return {
    data: await blobToImageData(await response.blob()),
    fileName,
  };
};
