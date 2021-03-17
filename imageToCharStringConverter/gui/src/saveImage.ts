import { imageToDataURL } from "./imageToDataURL.js";
import { saveDataUrl } from "./saveDataUrl.js";

export const saveImage = (image: ImageData, fileName: string) => {
  saveDataUrl({ dataURL: imageToDataURL(image), fileName });
};
