import { CharStringWithoutInitialPosition } from "./CharStringWithoutInitialPosition.js";
import { getDrawCommand } from "./getDrawCommand.js";
import { getMoveCommand } from "./getMoveCommand.js";
import { ImageDataToCharStringInput } from "./imageDataToCharString.js";
import { pixelWidth, pixelHeight } from "./ImageConvertConstants.js";
import { getImageDataInfo } from "./getImageDataInfo.js";
import { callSubroutineCommand } from "./callSubroutineCommand.js";

export const imageDataToCharStringWithoutInitialPosition = (
  input: ImageDataToCharStringInput
): CharStringWithoutInitialPosition => {
  const notBlankPixels = getImageDataInfo(input);

  const firstCommand = callSubroutineCommand(-103 + notBlankPixels[0]!.color);
  let allCommands = firstCommand + "\n";
  for (let i = 1; i < notBlankPixels.length; ) {
    const pixel = notBlankPixels[i]!;
    const lastPixel = notBlankPixels[i - 1]!;
    const moveCommand = getMoveCommand({
      pixelHeight,
      pixelWidth,
      lastPixel,
      pixel,
    });
    const { drawCommand, dataConsumed } = getDrawCommand({
      notBlankPixels,
      index: i,
      color: pixel.color,
    });
    i += dataConsumed;
    allCommands += moveCommand + drawCommand;
  }
  const endPixel = notBlankPixels[notBlankPixels.length - 1]!;
  return {
    commands: allCommands,
    initialPosition: {
      x: notBlankPixels[0]!.x,
      y: notBlankPixels[0]!.y,
    },
    endPosition: {
      x: endPixel.x,
      y: endPixel.y,
    },
  };
};
