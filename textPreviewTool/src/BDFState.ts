export type BDFState =
  | STARTCHAR
  | ENCODING
  | BITMAP
  | PARSEBITMAP
  | PARSEBITMAPLater;

export interface STARTCHAR {
  readonly type: "STARTCHAR";
}

export interface ENCODING {
  type: "ENCODING";
  code: string;
}

export interface BITMAP {
  type: "BITMAP";
  code: string;
  char: string;
}

export interface PARSEBITMAP {
  type: "PARSEBITMAP";
  code: string;
  out: {
    imageData: ImageData;
    char: string;
  };
  lineIndex: number;
}

export interface PARSEBITMAPLater {
  type: "PARSEBITMAPLater";
  code: string;
  char: string;
  lines: string[];
}
