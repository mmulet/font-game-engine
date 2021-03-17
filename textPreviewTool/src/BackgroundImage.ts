const animation = [0, 1, 2, 3, 3, 2];

export class BackgroundImage {
  width: number;
  height: number;
  context: CanvasRenderingContext2D;

  fontemonLogo: HTMLImageElement;

  codeRelayLogo: HTMLImageElement[];

  x = 0;
  y = 0;
  scaleX = 2;
  scaleY = 2;

  lastTime = 0;
  animationTime = 0;
  frame = 0;
  mouse: MouseOrTouchInput | null = null;
  mouseK = -50;
  mouseI = -50;
  playAnimation = false;
  // specialFrames: SpecialFrames = new Map();

  constructor() {
    const ratio = window.devicePixelRatio || 1;
    this.width = window.innerWidth > 0 ? window.innerWidth : screen.width;
    this.height = window.innerHeight > 0 ? window.innerHeight : screen.height;
    const maybeContext = makeAnimationCanvas(this.width, this.height, ratio);
    if (!maybeContext) {
      throw new Error("Could not make Animation canvas");
    }
    this.context = maybeContext.context;
    this.context.scale(this.scaleX, this.scaleY);

    this.context.imageSmoothingEnabled = false;
    this.fontemonLogo = document.getElementById(
      "fontemon"
    )! as HTMLImageElement;
    this.codeRelayLogo = [...new Array(4).keys()].map(
      (i) =>
        document.getElementById(`code-relay-0${i + 1}`)! as HTMLImageElement
    );
    try {
      if (matchMedia("(prefers-reduced-motion)").matches) {
        this.playAnimation = false;
      } else {
        const shouldPlayAnimation = localStorage.getItem("play-animation");
        this.playAnimation =
          shouldPlayAnimation ? true : false;
      }
    } catch (err) {}
    this.setupMouseAndTouchListeners();
    requestAnimationFrame(this.updateStateAndDraw);
  }
  updateStateAndDraw = (totalTimeElapsed: number) => {
    const deltaTime = totalTimeElapsed - this.lastTime;
    this.lastTime = totalTimeElapsed;
    if (!this.playAnimation) {
      requestAnimationFrame(this.updateStateAndDraw);
      return;
    }
    this.updateState(deltaTime);
    this.draw();
    requestAnimationFrame(this.updateStateAndDraw);
  };
  updateState = (deltaTime: number) => {
    this.animationTime += deltaTime;
    if (this.animationTime >= 160) {
      this.animationTime = 0;
      this.frame++;
      if (this.frame >= animation.length) {
        this.frame = 0;
      }
    }
    const velocity = deltaTime * 0.04;
    this.x += velocity;
    if (this.x >= 256) {
      this.x -= 256;
    }

    this.y += velocity;
    if (this.y >= 128) {
      this.y -= 128;
    }

    if (!this.mouse) {
      return;
    }
    this.mouseK = Math.floor((this.mouse.clientY - this.y) / 64);
    this.mouseI = Math.floor((this.mouse.clientX - this.x) / 128);
  };

  draw = () => {
    this.context.clearRect(0, 0, this.width, this.height);
    const logoFrame = this.codeRelayLogo[animation[this.frame]];
    const alternateLogoFrame = this.codeRelayLogo[
      animation[(this.frame + 3) % animation.length]
    ];
    const numberOfColumns = this.width / this.scaleX / 128 + 1;
    for (let k = -2; k < this.height / this.scaleY / 64 + 1; k++) {
      const mouseRow = this.mouseK == k;
      for (let i = -2; i < numberOfColumns; i++) {
        const image =
          i % 2
            ? k % 2
              ? this.fontemonLogo
              : alternateLogoFrame
            : k % 2
            ? logoFrame
            : this.fontemonLogo;

        if (mouseRow && this.mouse && i == this.mouseI) {
          this.context.drawImage(
            image,
            this.x + i * 128 - 32,
            this.y + k * 64 - 16,
            192,
            96
          );
          continue;
        }
        this.context.drawImage(image, this.x + i * 128, this.y + k * 64);
      }
    }
    if (!this.mouse) {
      return;
    }
  };

  setupMouseAndTouchListeners = () => {
    window.addEventListener(
      "mousemove",
      ({ clientX, clientY }: MouseEvent) => {
        this.mouse = setupTouch({
          clientX: clientX / this.scaleX,
          clientY: clientY / this.scaleY,
          input: this.mouse ?? undefined,
        });
      },
      false
    );

    document
      .getElementById("toggle-animation")!
      .addEventListener("click", () => {
        this.playAnimation = !this.playAnimation;
        try {
          localStorage.setItem(
            "play-animation",
            this.playAnimation ? "true" : ""
          );
          if (!this.playAnimation) {
            this.context.clearRect(0, 0, this.width, this.height);
          }
        } catch (err) {}
        console.log(this.playAnimation);
      });
  };
}
const setupTouch = ({
  clientX,
  clientY,
  input: maybeInput,
}: {
  readonly clientX: number;
  readonly clientY: number;
  readonly input?: MouseOrTouchInput;
}) => {
  const touchWidth = 20;
  const input = maybeInput ?? {
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    clientX: 0,
    clientY: 0,
    difference: null,
    frameValid: false,
  };
  if (input) {
    input.difference = {
      x: clientX - input.clientX,
      y: clientY - input.clientY,
    };
  }
  input.clientX = clientX;
  input.clientY = clientY;
  input.left = clientX - touchWidth;
  input.right = clientX + touchWidth;
  input.top = clientY - touchWidth;
  input.bottom = clientY + touchWidth;
  return input;
};
interface MouseOrTouchInput {
  left: number;
  right: number;
  top: number;
  bottom: number;
  clientX: number;
  clientY: number;
  difference: {
    x: number;
    y: number;
  } | null;
}

const animationCanvasId = "animation-canvas";

export const makeAnimationCanvas = (
  width: number,
  height: number,
  ratio: number
) => {
  {
    const canvas = document.getElementById(
      animationCanvasId
    ) as HTMLCanvasElement;
    if (canvas) {
      const context = canvas.getContext("2d");
      if (!context) {
        return null;
      }
      return {
        canvas,
        context,
      };
    }
  }
  const canvas = makeAnimationCanvasElement(width, height, ratio);
  document.body.appendChild(canvas);

  const context = canvas.getContext("2d");
  if (!context) {
    return null;
  }
  context?.scale(ratio, ratio);
  return {
    canvas,
    context,
  };
};

export const makeAnimationCanvasElement = (
  width: number,
  height: number,
  ratio: number
) => {
  const canvas = document.createElement("canvas");
  canvas.id = animationCanvasId;
  canvas.width = width * ratio;
  canvas.height = height * ratio;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  canvas.style.top = "0";
  canvas.style.left = "0";
  canvas.style.position = "fixed";
  canvas.style.pointerEvents = "none";
  return canvas;
};
