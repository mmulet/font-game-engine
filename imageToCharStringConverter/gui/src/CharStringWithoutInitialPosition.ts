export interface CharStringWithoutInitialPosition {
  commands: string;
  initialPosition: { x: number; y: number };
  endPosition: { x: number; y: number };
}
