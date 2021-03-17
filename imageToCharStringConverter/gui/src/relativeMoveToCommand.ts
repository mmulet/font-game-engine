export const relativeMoveToCommand = ({
  dx,
  dy,
}: {
  readonly dx: number;
  readonly dy: number;
}) => `${dx} ${dy} rmoveto\n`;
