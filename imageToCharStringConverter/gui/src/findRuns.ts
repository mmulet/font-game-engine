import { ImagePixel } from "./ImagePixel.js";
import { havePixelRun } from "./havePixelRun.js";

export interface FindRunsInput {
  readonly notBlankPixels: ImagePixel[];
  readonly index: number;
}
export const findRuns = ({ notBlankPixels, index }: FindRunsInput) => {
  const pixel = notBlankPixels[index]!;
  const nextPixel = notBlankPixels[index + 1]!;
  if (!havePixelRun({ pixel, nextPixel })) {
    return null;
  }
  const runNumber = _findRuns({
    notBlankPixels,
    nextColorShouldBe: pixel.color,
    currentRunNumber: 1,
    index: index + 1,
  });
  const runType = `${pixel.color}${nextPixel.color}`;
  return {
    runNumber,
    runType,
  };
};

export interface InnerInput extends FindRunsInput {
  readonly currentRunNumber: number;
  readonly nextColorShouldBe: number;
}
export const _findRuns = ({
  notBlankPixels,
  index,
  currentRunNumber,
  nextColorShouldBe,
}: InnerInput): number => {
  if (currentRunNumber >= 23) {
    return currentRunNumber;
  }
  const pixel = notBlankPixels[index]!;
  const nextPixel = notBlankPixels[index + 1]!;
  if (
    !havePixelRun({ pixel, nextPixel }) ||
    nextPixel.color !== nextColorShouldBe
  ) {
    return currentRunNumber;
  }

  //have a run, continue it
  return _findRuns({
    notBlankPixels,
    index: index + 1,
    currentRunNumber: currentRunNumber + 1,
    /**
     * runs are either an alternate pattern
     * color a, b, next is a
     * or a same pattern
     * color a a. next is a
     * In either case the next color should
     * be the color of the current pixel
     */
    nextColorShouldBe: pixel.color,
  });
};
