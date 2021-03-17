import { imageToDataURL } from "./imageToDataURL.js";
import { saveCompleteFile } from "./saveCompleteFile.js";
import { imageDataToCharStringWithoutInitialPosition } from "./imageDataToCharStringWithoutInitialPosition.js";
import { colors } from "./OutputColors.js";

export const saveBoth = async (image: ImageData, saveFileName: string) => {
  try {
    const pngURL = imageToDataURL(image);
    const charStringInfo = imageDataToCharStringWithoutInitialPosition({
      imageData: image,
      colors,
    });

    return await saveCompleteFile({
      charStringInfo,
      pngURL,
      name: saveFileName,
    });
  } catch (err) {
    return {
      type: "error" as const,
      text: err.message as string
    }
  }
};
