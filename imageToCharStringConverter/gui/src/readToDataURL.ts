
export const readToDataURL = (data: Blob) =>
  new Promise<string>((resolve) => {
    const reader = new FileReader();
    reader.addEventListener("loadend", () => {
      resolve(reader.result!.toString());
    });
    reader.readAsDataURL(data);
  });
