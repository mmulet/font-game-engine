export interface Font {
  [code: string]: { imageData: ImageData; char: string };
}

export interface FontInfo {
  [code: string]: { char: string; bitmapBDFLines: string[] };
}
