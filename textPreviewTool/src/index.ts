import { colors } from "./colors";
import { Font } from "./Font";
import { getLineState } from "./getLineState";
import { getMaxFrame } from "./getMaxFrame";
import { isInBox } from "./isInBox";
import { LineState, lineStateEmpty } from "./LineState";
import { MousePosition } from "./MousePosition";
import { parserToString } from "./parserToString";
import { Parser, ParseState, parseText, WordParseState } from "./parseText";
import { StoredProperties } from "./StoredProperties";
import { gohuFont } from "./gohuFont";
import { parseBDF } from "./parseBDF";
import { BackgroundImage } from "./BackgroundImage";

class PreviewTool {
  context: CanvasRenderingContext2D;
  canvas: HTMLCanvasElement;
  textArea: HTMLTextAreaElement;
  parser: Parser | null = null;

  reticleBox = {
    x: -1,
    y: -1,
    width: -1,
    height: -1,
  };

  frameLeftBox = {
    x: 250,
    y: 100,
    width: 10,
    height: 10,
  };
  frameRightBox = {
    x: 270,
    y: 100,
    width: 10,
    height: 10,
  };

  error: string | null = null;
  frame: number = 0;

  max_frame: number = 0;

  lineState: LineState = lineStateEmpty;

  brokenLines: number[] = [];

  dragFrameState: "dragging" | "notDragging" = "notDragging";

  mousePosition: MousePosition = {
    x: -1,
    y: -1,
  };
  font: Font;
  charToCode: { [char: string]: string[] | undefined };
  _text: string = "";

  get text() {
    return this._text;
  }

  set text(newValue) {
    this._text = newValue;
    this.saveSettings();
  }

  _spacing_x: number = 8;
  get spacing_x() {
    return this._spacing_x;
  }
  set spacing_x(newValue) {
    this._spacing_x = newValue;
    this.saveSettings();
  }

  _line_width: number = 17;
  get line_width() {
    return this._line_width;
  }

  set line_width(newValue) {
    this._line_width = newValue;
    this.saveSettings();
  }

  _bottom_line_distance = -10;
  get bottom_line_distance() {
    return this._bottom_line_distance;
  }

  set bottom_line_distance(newValue: number) {
    this._bottom_line_distance = newValue;
    this.saveSettings();
  }

  _textType: "character" | "word" = "word";
  get textType() {
    return this._textType;
  }
  set textType(newValue) {
    this._textType = newValue;
    this.saveSettings();
  }

  get frameScale(): number {
    if (this.max_frame < 79) {
      return 5;
    }
    return 395 / this.max_frame;
  }

  get trackFrame(): boolean {
    return this.frame == this.max_frame;
  }

  localStorage: Storage | null;

  constructor() {
    this.canvas = document.getElementById("canvas") as HTMLCanvasElement;
    this.context = this.canvas.getContext("2d")!;
    this.textArea = document.getElementById("area")! as HTMLTextAreaElement;

    this.setupMouseAndTouchListeners();
    const font = parseBDF({
      bdf: gohuFont,
      makeImageData: (w, h) => new ImageData(w, h),
    });
    this.font = font;
    this.charToCode = {};
    for (const [code, { char }] of Object.entries(font)) {
      this.charToCode[char] = (this.charToCode[char] ?? []).concat([code]);
    }

    this.context.font = "18px pressStart";
    try {
      this.localStorage = localStorage;
      this.setupStateFromStoredProperties();
    } catch (err) {
      this.localStorage = null;
    }

    requestAnimationFrame(this.updateStateAndDraw);
  }

  saveSettings = () => {
    if (!this.localStorage) {
      return;
    }
    const storedProps: StoredProperties = {
      bottom_line_distance: this.bottom_line_distance,
      line_width: this.line_width,
      spacing_x: this.spacing_x,
      text: this.text,
      textAreaHeight: this.textArea.style.height ?? `36px`,
      textAreaWidth: this.textArea.style.width ?? `163px`,
      textType: this.textType,
    };
    this.localStorage.setItem("storage", JSON.stringify(storedProps));
  };

  setupStateFromStoredProperties = () => {
    if (!this.localStorage) {
      return;
    }
    const storedPropertiesString = this.localStorage.getItem("storage");
    if (!storedPropertiesString) {
      return;
    }
    const storedProperties: StoredProperties = JSON.parse(
      storedPropertiesString
    );
    this._text = storedProperties.text;
    this._spacing_x = storedProperties.spacing_x;
    this._line_width = storedProperties.line_width;
    this._bottom_line_distance = storedProperties.bottom_line_distance;
    this.textArea.value = this.text;
    this.textArea.style.height = storedProperties.textAreaHeight;
    this.textArea.style.width = storedProperties.textAreaWidth;
    this.textType = storedProperties.textType ?? "word";

    (document.getElementById("spacing-x")! as HTMLInputElement).value = this
      ._spacing_x as any;
    (document.getElementById("line-width")! as HTMLInputElement).value = this
      ._line_width as any;
    (document.getElementById(
      "bottom-line-height"
    )! as HTMLInputElement).value = this._bottom_line_distance as any;
    (document.getElementById("word-based")! as HTMLInputElement).checked =
      this.textType == "word";

    this.reParseLineState(true);
  };

  updateStateAndDraw = () => {
    this.updateState();
    this.draw();
    requestAnimationFrame(this.updateStateAndDraw);
  };

  updateState = () => {
    this.updateReticleBoxState();
    this.updateCursorState();

    if (this.dragFrameState != "dragging") {
      return;
    }
    this.setCurrentFrameToMouseXPosition();
  };

  updateCursorState = () => {
    if (this.dragFrameState == "dragging") {
      this.canvas.style.cursor = "grabbing";
      return;
    }
    if (isInBox(this.mousePosition, this.reticleBox)) {
      this.canvas.style.cursor = "grab";
      return;
    }
    if (
      this.mouseIsOverFrame(this.mousePosition) ||
      [this.frameLeftBox, this.frameRightBox].some((box) =>
        isInBox(this.mousePosition, box)
      )
    ) {
      this.canvas.style.cursor = "pointer";
      return;
    }
    this.canvas.style.cursor = "default";
    return;
  };

  updateReticleBoxState = () => {
    const left = this.frame * this.frameScale - 5;
    this.reticleBox.x = left;
    this.reticleBox.y = 120;
    this.reticleBox.width = 10;
    this.reticleBox.height = 10;
  };

  setCurrentFrameToMouseXPosition = () => {
    const oldFrame = this.frame;
    const draggedFrame = Math.min(
      Math.round((this.mousePosition.x + 5) / this.frameScale),
      this.max_frame
    );
    this.frame = draggedFrame;
    if (oldFrame == this.frame) {
      return;
    }
    this.lineState = getLineState(this.parser, this.frame);
  };

  draw = () => {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.context.fillStyle = "black";
    if (this.error) {
      this.context.fillText(this.error, 0, 25);
    } else {
      this.drawLineOfText(
        this.lineState.top.line,
        this.lineState.top.drawCount,
        25
      );
      this.drawLineOfText(
        this.lineState.bottom.line,
        this.lineState.bottom.drawCount,
        25 + -1 * this.bottom_line_distance + 3
      );
    }
    const lineWidthPosition = this.line_width * this.spacing_x;
    this.context.fillRect(lineWidthPosition, 0, 2, 50);
    this.context.fillText(`Frame: ${this.frame}/${this.max_frame}`, 0, 115);
    this.context.fillText("←", this.frameLeftBox.x, this.frameLeftBox.y + 15);
    this.context.fillText("→", this.frameRightBox.x, this.frameRightBox.y + 15);

    for (let i = 0; i < this.max_frame; i++) {
      this.context.fillStyle = colors[i % colors.length];
      this.context.fillRect(this.frameScale * i, 130, this.frameScale, 10);
    }
    this.context.fillStyle = "#ff3b30";
    this.context.fillRect(
      this.reticleBox.x,
      this.reticleBox.y,
      this.reticleBox.width,
      this.reticleBox.height
    );
    this.drawLineBreaks(lineWidthPosition);
  };

  drawLineBreaks = (lineWidthPosition: number) => {
    if (this.brokenLines.length <= 0) {
      return;
    }
    this.context.fillStyle = "black";
    const plural = this.brokenLines.length > 1 ? "s" : "";
    this.context.fillText(
      `${this.brokenLines.length} line break${plural}`,
      lineWidthPosition + 15,
      15
    );
    this.context.fillText(
      `Line${plural}: ` + this.brokenLines.join(" "),
      lineWidthPosition + 15,
      35
    );
  };

  drawLineOfText = (line: string[], drawCount: number, y: number) => {
    for (let i = 0; i < drawCount; i++) {
      const character = line[i];
      if (character == " ") {
        continue;
      }
      const glyphInfo = this.font[character];
      if (!glyphInfo) {
        this.error = `Unrecognized character ${character}`;
        continue;
      }
      this.context.putImageData(glyphInfo.imageData, i * this.spacing_x, y);
    }
  };

  parseNewLines = (text: string) => {
    if (!text) {
      this.lineState = lineStateEmpty;
      return;
    }
    const parser =
      this.textType == "word" ? new WordParseState() : new ParseState();
    const output = parseText(text, this.line_width, this.charToCode, parser);
    if (!output) {
      this.parser = parser;
      this.error = null;
      return;
    }
    this.parser = null;
    this.error = output.error;
  };

  reParseLineState = (trackFrame: boolean) => {
    if (!this.text) {
      this.lineState = lineStateEmpty;
      return;
    }
    this.brokenLines = this.text
      .replace(/\\./g, " ")
      .split("\n")
      .reduce((o, line, index) => {
        if (line.length <= this.line_width) {
          return o;
        }
        o.push(index + 1);
        return o;
      }, [] as number[]);
    this.parseNewLines(this.text);
    this.max_frame = getMaxFrame(this.parser);
    if (trackFrame) {
      this.frame = this.max_frame;
    } else if (this.frame >= this.max_frame) {
      this.frame = this.max_frame;
    }
    this.lineState = getLineState(this.parser, this.frame);
  };

  mouseIsOverFrame = ({ y }: MousePosition) => {
    return y >= 130 && y < 130 + 10;
  };

  previousFrame = () => {
    this.frame = Math.max(this.frame - 1, 0);
    this.lineState = getLineState(this.parser, this.frame);
  };
  nextFrame = () => {
    this.frame = Math.min(this.frame + 1, this.max_frame);
    this.lineState = getLineState(this.parser, this.frame);
  };

  setupMouseAndTouchListeners = () => {
    this.textArea.addEventListener("input", () => {
      const text = this.textArea.value;
      const newText = text.replaceAll(/\\n/g, "\n");
      this.textArea.value = newText;
      this.text = newText;
      this.reParseLineState(this.trackFrame);
    });
    document
      .getElementById("transform-button")!
      .addEventListener("click", () => {
        const outputText = parserToString(this.parser, this.font);
        navigator.clipboard.writeText(outputText).then(() => {
          document.getElementById("copied")!.innerText = "Copied";
        });
      });
    {
      const spacingInput = document.getElementById(
        "spacing-x"
      )! as HTMLInputElement;
      spacingInput.addEventListener("input", () => {
        this.spacing_x = (spacingInput.value as unknown) as number;
      });
    }
    {
      const lineWidthInput = document.getElementById(
        "line-width"
      )! as HTMLInputElement;
      lineWidthInput.addEventListener("input", () => {
        this.line_width = Math.floor(
          (lineWidthInput.value as unknown) as number
        );
        this.reParseLineState(this.trackFrame);
      });
    }
    {
      const bottomLinInput = document.getElementById(
        "bottom-line-height"
      )! as HTMLInputElement;
      bottomLinInput.addEventListener("input", () => {
        this.bottom_line_distance = (bottomLinInput.value as unknown) as number;
      });
    }
    this.canvas.addEventListener("mousemove", ({ offsetX, offsetY }) => {
      this.mousePosition = {
        x: offsetX,
        y: offsetY,
      };
    });
    {
      const wordBasedCheckbox = document.getElementById(
        "word-based"
      )! as HTMLInputElement;

      wordBasedCheckbox.addEventListener("input", () => {
        console.log("tacos");
        this.textType = wordBasedCheckbox.checked ? "word" : "character";
        this.reParseLineState(this.trackFrame);
      });
    }

    this.canvas.addEventListener("mousedown", ({ offsetX, offsetY }) => {
      const position = {
        x: offsetX,
        y: offsetY,
      };
      if (isInBox(position, this.reticleBox)) {
        this.dragFrameState = "dragging";
        return;
      }
      if (isInBox(position, this.frameLeftBox)) {
        this.previousFrame();
        return;
      }
      if (isInBox(position, this.frameRightBox)) {
        this.nextFrame();
        return;
      }

      if (this.mouseIsOverFrame(position)) {
        this.setCurrentFrameToMouseXPosition();
        return;
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
          this.previousFrame();
          return;
        case "ArrowRight":
          this.nextFrame();
          return;
        default:
          return;
      }
    });
    window.addEventListener("mouseup", () => {
      this.dragFrameState = "notDragging";
    });
    try {
      //@ts-ignore
      const observer = new ResizeObserver(() => {
        this.saveSettings();
      });
      observer.observe(this.textArea);
    } catch (err) {}
  };
}

///@ts-ignore
let animationState: PreviewTool | null = null;
///@ts-ignore
let backgroundImage: BackgroundImage | null = null
window.onload = () => {
  animationState = new PreviewTool();
  backgroundImage = new BackgroundImage()
};
