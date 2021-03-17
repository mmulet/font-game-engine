import { replaceImageDataWithGuessedColors } from "./replaceImageDataWithGuessedColors.js";
import { colors } from "./OutputColors.js";

export const imageToDataURL = (image: ImageData) => {
  const canvas = document.createElement("canvas");
  canvas.width = image.width;
  canvas.height = image.height;

  const newData = new ImageData(image.width, image.height);
  newData.data.set(image.data);
  replaceImageDataWithGuessedColors(newData, colors);
  canvas.getContext("2d")!.putImageData(newData, 0, 0);
  return canvas.toDataURL();
};
