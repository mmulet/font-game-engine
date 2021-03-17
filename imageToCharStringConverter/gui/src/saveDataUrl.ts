export interface Input {
  readonly dataURL: string;
  readonly fileName: string;
}

export const saveDataUrl = ({ dataURL, fileName }: Input) => {
  const link = document.createElement("a");
  link.download = fileName;
  link.target = "_blank";
  link.href = dataURL;
  link.click();
};
