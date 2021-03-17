import { BackgroundImage } from "./BackgroundImage.js";
import { colorHitBoxTest, HitBoxTestResult } from "./colorHitBoxTest.js";
import { convertAndSave } from "./convertAndSave.js";
import { drawCrossHairs } from "./drawCrossHairs.js";
import { drawCurrentColors } from "./drawCurrentColors.js";
import { drawOutputColors } from "./drawOutputColors.js";
import { drawSelection } from "./drawSelection.js";
import { getAllColorsFromAnImage } from "./getAllColorsFromAnImage.js";
import { ImageInfo } from "./ImageInfo.js";
import { listenForImageChanges } from "./listenForImageChanges.js";
import { loadImageByFilePath } from "./loadImageByFilePath.js";
import { loadNextImageByFilePath } from "./loadNextImageByFilePath.js";
import { MousePosition } from "./MousePosition.js";
import { mousePositionToPixelPosition } from "./mousePositionToPixelPosition.js";
import { nextSelectionState } from "./nextSelectionState.js";
import { OutputColors } from "./OutputColors.js";
import { removeQuotes } from "./removeQuotes.js";
import { replaceInputColorWithOutputColor } from "./replaceInputColorWithOutputColor.js";
import { saveBoth } from "./saveBoth.js";
import { saveImage } from "./saveImage.js";
import { Selection } from "./Selection.js";
import { UIColor } from "./UIColor.js";
import { yPositionCurrentColor } from "./yPositionCurrentColor.js";

class Converter {
  image: ImageInfo | null = null;
  context: CanvasRenderingContext2D;
  canvas: HTMLCanvasElement;
  imageCanvas: HTMLCanvasElement;
  width = 500;
  height = 500;

  scale = 1;

  imageStartX = 70;
  imageStartY = 70;

  undoStack: {
    image: ImageInfo;
    currentColors: UIColor[];
  }[] = [];

  mousePosition: MousePosition = { x: -Infinity, y: -Infinity };
  keyboardPosition: MousePosition = {
    x: 0,
    y: 0,
  };

  control: "mouse" | "keyboard" = "mouse";

  get controlPosition(): MousePosition {
    if (this.control == "mouse") {
      return mousePositionToPixelPosition(
        this.mousePosition,
        this.imageStartX,
        this.imageStartY
      );
    }
    return this.keyboardPosition;
  }

  selection: Selection = {
    type: "none",
  };

  currentColors: UIColor[] = [];

  saveFileNameInput: HTMLInputElement;
  imageFilePathInput: HTMLInputElement;

  constructor() {
    this.canvas = document.getElementById("canvas") as HTMLCanvasElement;
    this.imageCanvas = document.createElement("canvas");
    this.context = this.canvas!.getContext("2d")!;
    this.saveFileNameInput = document.getElementById(
      "file-name"
    ) as HTMLInputElement;
    this.imageFilePathInput = document.getElementById(
      "image-file-path"
    ) as HTMLInputElement;
    this.context.imageSmoothingEnabled = false;
    this.context.scale(this.scale, this.scale);
    this.setupMouseAndTouchListeners();
    requestAnimationFrame(this.updateStateAndDraw);
  }

  updateStateAndDraw = (_totalTimeElapsed: number) => {
    this.updateState();
    this.draw();
    requestAnimationFrame(this.updateStateAndDraw);
  };

  updateState = () => {
    this.updateCursor();
    this.updateSelectionState();
  };

  updateCursor = () => {
    const x = this.mousePosition.x - this.imageStartX;
    const y = this.mousePosition.y - this.imageStartY;
    if (x >= 0 && y >= 0) {
      if (this.control == "mouse") {
        this.canvas.style.cursor = "none";
        return;
      }
      this.canvas.style.cursor = "crosshair";
      return;
    }
    {
      const out = colorHitBoxTest(this.mousePosition, this.currentColors);
      if (out.type != "none") {
        this.canvas.style.cursor = "pointer";
        return;
      }
    }

    this.canvas.style.cursor = "default";
  };

  updateSelectionState = () => {
    this.selection = nextSelectionState(
      this.selection,
      this.image ? this.image.data : null,
      this.currentColors,
      this.control,
      this.mousePosition,
      this.keyboardPosition,
      this.imageStartX,
      this.imageStartY
    );
  };

  draw = () => {
    this.context.clearRect(0, 0, this.width, this.height);
    this.context.fillStyle = "gray";
    this.context.fillRect(this.imageStartX, this.imageStartY, 500, 500);
    if (this.image) {
      this.imageCanvas.getContext("2d")!.putImageData(this.image.data, 0, 0);
      this.context.drawImage(
        this.imageCanvas,
        this.imageStartX,
        this.imageStartY
      );
    }
    drawOutputColors(this.context);

    drawCurrentColors(this.context, this.currentColors);

    drawSelection(
      this.context,
      this.selection,
      this.currentColors,
      this.imageStartX,
      this.imageStartY - 20
    );

    drawCrossHairs(
      this.context,
      this.control,
      this.mousePosition,
      this.keyboardPosition,
      this.imageStartX,
      this.imageStartY
    );
  };

  mouseEventToMousePosition = ({
    offsetX,
    offsetY,
  }: MouseEvent): MousePosition => ({
    x: offsetX / this.scale,
    y: offsetY / this.scale,
  });

  setupMouseAndTouchListeners = () => {
    this.canvas.addEventListener(
      "mousemove",
      (event: MouseEvent) => {
        this.mousePosition = this.mouseEventToMousePosition(event);
      },
      false
    );

    window.addEventListener("click", this.handleCanvasClick);
    document
      .getElementById("save-charstring")!
      .addEventListener("click", () => {
        if (!this.image) {
          return;
        }
        convertAndSave(this.image.data, this.image.fileName);
      });

    document.getElementById("save-image")!.addEventListener("click", () => {
      if (!this.image) {
        return;
      }
      saveImage(this.image.data, this.image.fileName);
    });

    document.getElementById("undo-button")!.addEventListener("click", () => {
      if (!this.image || this.undoStack.length <= 0) {
        return;
      }
      const { image, currentColors } = this.undoStack.pop()!;
      this.image = image;
      this.setFileNameInput(image.fileName);
      this.currentColors = currentColors;
    });

    document.getElementById("scale")!.addEventListener("change", (e) => {
      this.context.resetTransform();
      this.scale = (e.target as any).value as number;
      this.context.scale(this.scale, this.scale);
    });

    document
      .getElementById("save-both")
      ?.addEventListener("click", async () => {
        if (!this.image) {
          return;
        }
        const fileName = this.saveFileNameInput.value;
        const status = await saveBoth(this.image.data, fileName);
        switch (status.type) {
          case "ok":
            this.setSaveStatus(`Saved ${fileName}`);
            return;
          case "error":
            this.setSaveStatus(`Error: ${status.text}`);
            return;
        }
      });

    document
      .getElementById("load-by-path")!
      .addEventListener("click", async () => {
        const filePath = this.imageFileInput;
        if (!filePath) {
          return;
        }
        try {
          this.clearLoadImageError();
          const data = await loadImageByFilePath(filePath);
          this.onNewImage(data, filePath);
        } catch (err) {
          this.setLoadImageError(err.message);
        }
      });
    document.getElementById("next")!.addEventListener("click", async () => {
      const filePath = this.imageFileInput;
      if (!filePath) {
        return;
      }
      try {
        this.clearLoadImageError();
        const { data, fileName } = await loadNextImageByFilePath(filePath);
        this.onNewImage(data, fileName);
        this.imageFilePathInput.value = fileName;
      } catch (err) {
        this.setLoadImageError(err.message);
      }
    });
    window.addEventListener("keydown", ({ key }) => {
      if (
        document.activeElement != null &&
        document.activeElement != document.body
      ) {
        return;
      }
      switch (key) {
        case "ArrowLeft":
        case "ArrowRight":
        case "ArrowUp":
        case "ArrowDown":
        case "Enter":
        case "Backspace":
          break;
        default:
          return;
      }
      if (this.control == "mouse") {
        this.control = "keyboard";
        const { x, y } = mousePositionToPixelPosition(
          this.mousePosition,
          this.imageStartX,
          this.imageStartY
        );
        this.keyboardPosition.x = Math.max(0, x);
        this.keyboardPosition.y = Math.max(0, y);
      }
      switch (key) {
        case "ArrowLeft":
          this.keyboardPosition.x = Math.max(0, this.keyboardPosition.x - 1);
          return;
        case "ArrowRight":
          this.keyboardPosition.x++;
          return;
        case "ArrowUp":
          this.keyboardPosition.y = Math.max(0, this.keyboardPosition.y - 1);
          return;
        case "ArrowDown":
          this.keyboardPosition.y++;
          return;
        case "Enter":
          this.selectOrClearSelection();
          return;
        case "Backspace":
          this.selection = {
            type: "none",
          };
          return;
        default:
          return;
      }
    });
    listenForImageChanges(this.onNewImage);
  };

  get imageFileInput(): string | null {
    const { value } = this.imageFilePathInput;
    if (!value) {
      return null;
    }
    return removeQuotes(value);
  }

  onNewImage = (imageData: ImageData, fileName: string) => {
    this.image = {
      data: imageData,
      fileName: fileName,
    };
    this.setFileNameInput(fileName);
    this.currentColors = getAllColorsFromAnImage(
      this.image.data,
      true
    ).inputColors;
    this.imageCanvas
      .getContext("2d")!
      .clearRect(0, 0, this.imageCanvas.width, this.imageCanvas.height);
    this.imageCanvas.width = this.image.data.width;
    this.imageCanvas.height = this.image.data.height;
  };

  setSaveStatus = (status: string) => {
    (document.getElementById(
      "save-status"
    )! as HTMLDivElement).innerText = status;
  };

  setLoadImageError = (error: string) => {
    (document.getElementById(
      "load-image-error"
    )! as HTMLDivElement).innerText = error;
  };
  clearLoadImageError = () => {
    (document.getElementById("load-image-error")! as HTMLDivElement).innerText =
      "";
  };

  setFileNameInput = (fileName: string) => {
    const parts = removeQuotes(fileName)
      .replace(/\.[^\.]+$/, "")
      .split(/[\\/]/);
    this.saveFileNameInput.value = parts[parts.length - 1];
  };

  onColorBoxClick = (hitBoxTest: HitBoxTestResult) => {
    switch (hitBoxTest.type) {
      case "none":
        return;
      case "input":
        this.selection = {
          inputColorIndex: hitBoxTest.inputColorIndex,
          type: "selected",
        };
        return;
      case "output":
        if (this.selection.type != "selected") {
          return;
        }
        this.moveColor(this.selection.inputColorIndex, hitBoxTest.name);
        this.selection = {
          type: "none",
        };
        return;
    }
  };

  moveColor = (inputColorIndex: number, outputColorKey: keyof OutputColors) => {
    if (!this.image) {
      return;
    }
    const newData = new ImageData(
      this.image.data.width,
      this.image.data.height
    );
    newData.data.set(this.image.data.data);
    this.undoStack.push({
      image: this.image,
      currentColors: JSON.parse(JSON.stringify(this.currentColors)),
    });
    this.image = {
      data: newData,
      fileName: this.image.fileName,
    };
    const [oldColor] = this.currentColors.splice(inputColorIndex, 1);
    if (this.undoStack.length >= 50) {
      this.undoStack.shift();
    }
    replaceInputColorWithOutputColor(outputColorKey, this.image.data, oldColor);
    for (const [i, color] of this.currentColors.entries()) {
      color.position.y = yPositionCurrentColor(i);
    }
  };

  handleCanvasClick = (event: MouseEvent) => {
    const hitBoxTest = colorHitBoxTest(
      this.mouseEventToMousePosition(event),
      this.currentColors
    );
    if (hitBoxTest.type != "none") {
      this.onColorBoxClick(hitBoxTest);
      return;
    }
    if (this.control == "keyboard") {
      this.control = "mouse";
      return;
    }
    this.selectOrClearSelection();
  };

  selectOrClearSelection = () => {
    switch (this.selection.type) {
      case "selected":
        this.selection = {
          type: "none",
        };
        return;
      case "highlighted":
        this.selection = {
          type: "selected",
          inputColorIndex: this.selection.inputColorIndex,
        };
    }
  };
}

///@ts-ignore
let animationState: Converter | null = null;
///@ts-ignore
let backgroundImage: BackgroundImage | null = null;

window.onload = () => {
  animationState = new Converter();
 
  backgroundImage = new BackgroundImage();
};
