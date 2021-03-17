import { blobToImageData } from "./blobToImageData.js";

export const listenForImageChanges = (
  onNewImageData: (imageData: ImageData, imageFileName: string) => void
) => {
  const imageFile = document.getElementById("image-file") as HTMLInputElement;
  imageFile.addEventListener("change", async () => {
    const imageData = await blobToImageData(imageFile!.files![0]);
    const imageFileName = imageFile!.files![0].name;
    onNewImageData(imageData, imageFileName);
  });
};
