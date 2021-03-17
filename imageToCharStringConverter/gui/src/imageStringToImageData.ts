export const imageStringToImageData = async (imageString: string) => {
  const image = new Image();
  return new Promise<ImageData>((resolve, reject) => {
    image.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = image.width;
      canvas.height = image.height;
      const context = canvas.getContext("2d")!;
      context.drawImage(image, 0, 0);
      resolve(context.getImageData(0, 0, image.width, image.height));
    };
    image.onerror = (ev) => {
      reject(typeof ev == "string" ? ev : (ev as ErrorEvent).message);
    };
    image.src = imageString;
  });
};
