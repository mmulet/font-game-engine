export interface LineStateLine {
  readonly line: string[];
  readonly drawCount: number;
}

export interface LineState {
  readonly top: LineStateLine;
  readonly bottom: LineStateLine;
}

export const lineStateEmpty: LineState = {
  top: {
    line: [],
    drawCount: 0,
  },
  bottom: {
    line: [],
    drawCount: 0,
  },
};
