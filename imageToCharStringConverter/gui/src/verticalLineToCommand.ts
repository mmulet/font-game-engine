/**
 * Note: There are two forms to this command,
 * this uses the odd numbered form.
 * @odd numbered form
 */
export const verticalLineToCommand = ({
  pairs,
  lastDy,
}: {
  pairs: VerticalLineToPair[];
  lastDy: number;
}) =>
  `${pairs
    .map(({ dy, thenDx }) => `${dy} ${thenDx}`)
    .join(" ")} ${lastDy} vlineto\n`;

/**
 * Input pair to the vertical Line To Command.
 * The dy is applied before the dx,
 * that is why it is called dy and thenDx
 */
export interface VerticalLineToPair {
  readonly dy: number;
  readonly thenDx: number;
}
