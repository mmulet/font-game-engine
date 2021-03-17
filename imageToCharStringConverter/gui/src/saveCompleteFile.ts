import { CharStringWithoutInitialPosition } from "./CharStringWithoutInitialPosition.js";
import { SaveFileInput } from "./SaveFileInput";
import { saveFilePath } from "./saveFilePath";
export interface Input {
  readonly charStringInfo: CharStringWithoutInitialPosition;
  readonly pngURL: string;
  readonly name: string;
}

export const saveCompleteFile = async ({
  charStringInfo,
  pngURL,
  name,
}: Input) => {
  const saveFileInput: SaveFileInput = {
    charStringInfo: JSON.stringify(charStringInfo),
    pngURL,
    name,
  };
  try {
    const response = await fetch(
      new Request(saveFilePath, {
        method: "POST",
        // headers: {
        //   'Content-Type': 'application/json'
        // },
        body: JSON.stringify(saveFileInput),
      })
    );
    if (response.ok) {
      return {
        type: "ok",
      } as const;
    }
    const text = await response.text();

    return {
      type: "error",
      text,
    } as const;
  } catch (err) {
    return {
      type: "error" as const,
      text: err.message as string,
    } as const;
  }
};
