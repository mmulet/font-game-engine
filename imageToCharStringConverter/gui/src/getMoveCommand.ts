import { horizontalMoveToCommand } from "./horizontalMoveToCommand.js";
import { relativeMoveToCommand } from "./relativeMoveToCommand.js";

export interface GetMoveCommandInput {
  readonly pixel: { x: number; y: number };
  readonly lastPixel: { x: number; y: number };
  readonly pixelWidth: number;
  readonly pixelHeight: number;
}
export const getMoveCommand = ({
  pixel: { x, y },
  lastPixel: { x: lastX, y: lastY },
  pixelHeight,
  pixelWidth,
}: GetMoveCommandInput) => {
  if (lastY === y) {
    if (x === lastX + 1) {
      return "";
    }
    /**
     * Draw should be like this
     * so you end up at the start
     * of the next available pixel
     *   |    |       |   /\
     *   |    |       |   |
     *   |    |       |   |
     *   \/   |_______|   |
     *           -->
     *
     * so calculate the x distance to the pixel
     * minus 1, if pixels are adjacent then
     * moveto should be 0. so that's where
     * the minus one comes from.
     */
    return horizontalMoveToCommand({
      dx: (x - lastX - 1) * pixelWidth,
    });
  }
  /**
   * CFF is is
   *           /\
   *            |
   *            |
   *            -------->
   * But our image data is in
   *
   * -------->
   * |
   * |
   * |
   * \/
   *
   * that's where the -1 comes from
   */
  return relativeMoveToCommand({
    dx: (x - lastX - 1) * pixelWidth,
    dy: (y - lastY) * pixelHeight * -1,
  });
};
