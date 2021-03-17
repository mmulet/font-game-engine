import { imageStringToImageData } from "./imageStringToImageData.js";
import { readToDataURL } from "./readToDataURL.js";

export const blobToImageData = async (blob: Blob) => {
  const dataURL = await readToDataURL(blob);
  return imageStringToImageData(dataURL);
};
