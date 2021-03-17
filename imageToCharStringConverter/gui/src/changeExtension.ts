/**
 * 

 * @param extension Without the dot
 */
export const changeExtension = (filename: string, extension: string) =>
  filename.replace(/\.[^\.]+$/, `.${extension}`);
