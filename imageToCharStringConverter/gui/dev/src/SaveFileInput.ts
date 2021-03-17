export interface SaveFileInput {
  /**
   * should be a base64 dataURL
   */
  readonly pngURL: string;
  /**
   * JSON.stringify of a parse-bdf/CharStringWithoutInitialPosition
   */
  readonly charStringInfo: string;
  /**
   * name without extension
   */
  readonly name: string;
}
