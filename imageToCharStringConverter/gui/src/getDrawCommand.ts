import { callSubroutineCommand } from "./callSubroutineCommand.js";
import { findRuns, FindRunsInput as FindRunsInput } from "./findRuns.js";

export interface GetDrawCommandInput extends FindRunsInput {
  readonly color: 0 | 1 | 2;
}
export const getDrawCommand = (input: GetDrawCommandInput) => {
  const runs = findRuns(input);

  if (!runs) {
    return {
      dataConsumed: 1,
      drawCommand: callSubroutineCommand(-103 + input.color),
    };
  }
  const { runNumber, runType } = runs;

  const num =
    (() => {
      switch (runType) {
        case "00":
          return -99;
        case "11":
          return -76;
        case "22":
          return -53;
        case "01":
          return -30;
        case "02":
          return -7;
        case "12":
          return 16;
        case "10":
          return 39;
        case "20":
          return 62;
        case "21":
          return 85;
        default:
          console.error(`unrecognized runtype ${runType}`);
          return -100;
      }
    })() +
    runNumber -
    1;
  return {
    dataConsumed: runNumber + 1,
    drawCommand: callSubroutineCommand(num),
  };
};
