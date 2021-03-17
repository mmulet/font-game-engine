import { extensionToCharString } from "./extensionToCharString.js";
import { imageDataToCharStringWithoutInitialPosition } from "./imageDataToCharStringWithoutInitialPosition.js";
import { colors } from "./OutputColors.js";
import { saveDataUrl } from "./saveDataUrl.js";

export const convertAndSave = (image: ImageData, imageFileName: string) => {
  const charString = imageDataToCharStringWithoutInitialPosition({
    imageData: image,
    colors,
  });

  saveDataUrl({
    dataURL: `data:text/plain;base64,${btoa(JSON.stringify(charString))}`,
    fileName: extensionToCharString(imageFileName),
  });
};
