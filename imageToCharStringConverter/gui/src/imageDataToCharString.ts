import { addInitialDataToCharString } from "./addInitialDataToCharString.js";
import { Colors } from "./Colors.js";
import { imageDataToCharStringWithoutInitialPosition } from "./imageDataToCharStringWithoutInitialPosition.js";

export interface ImageDataToCharStringInput {
  readonly imageData: ImageData;
  readonly colors: Colors;
}

export const imageDataToCharString = (input: ImageDataToCharStringInput) => {
  return addInitialDataToCharString(
    imageDataToCharStringWithoutInitialPosition(input)
  );
};
