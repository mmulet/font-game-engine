import { CharStringWithoutInitialPosition } from "./CharStringWithoutInitialPosition.js";
import { endCharacterCommand } from "./endCharacterCommand.js";
import {
  pixelWidth,
  commandHeight,
  pixelHeight,
} from "./ImageConvertConstants.js";
import { relativeMoveToCommand } from "./relativeMoveToCommand.js";

export const addInitialDataToCharString = ({
  commands,
  initialPosition,
}: CharStringWithoutInitialPosition): string => {
  return (
    `0 ${relativeMoveToCommand({
      dx: initialPosition.x * pixelWidth,
      dy: commandHeight - initialPosition.y * pixelHeight,
    })} ` +
    commands +
    endCharacterCommand()
  );
};
