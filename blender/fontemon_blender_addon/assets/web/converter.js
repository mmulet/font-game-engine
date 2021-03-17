const animation = [0, 1, 2, 3, 3, 2];
class BackgroundImage {
    constructor() {
        this.x = 0;
        this.y = 0;
        this.scaleX = 2;
        this.scaleY = 2;
        this.lastTime = 0;
        this.animationTime = 0;
        this.frame = 0;
        this.mouse = null;
        this.mouseK = -50;
        this.mouseI = -50;
        this.playAnimation = false;
        this.updateStateAndDraw = (totalTimeElapsed) => {
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
        this.updateState = (deltaTime) => {
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
        this.draw = () => {
            this.context.clearRect(0, 0, this.width, this.height);
            const logoFrame = this.codeRelayLogo[animation[this.frame]];
            const alternateLogoFrame = this.codeRelayLogo[animation[(this.frame + 3) % animation.length]];
            const numberOfColumns = this.width / this.scaleX / 128 + 1;
            for (let k = -2; k < this.height / this.scaleY / 64 + 1; k++) {
                const mouseRow = this.mouseK == k;
                for (let i = -2; i < numberOfColumns; i++) {
                    const image = i % 2
                        ? k % 2
                            ? this.fontemonLogo
                            : alternateLogoFrame
                        : k % 2
                            ? logoFrame
                            : this.fontemonLogo;
                    if (mouseRow && this.mouse && i == this.mouseI) {
                        this.context.drawImage(image, this.x + i * 128 - 32, this.y + k * 64 - 16, 192, 96);
                        continue;
                    }
                    this.context.drawImage(image, this.x + i * 128, this.y + k * 64);
                }
            }
            if (!this.mouse) {
                return;
            }
        };
        this.setupMouseAndTouchListeners = () => {
            window.addEventListener("mousemove", ({ clientX, clientY }) => {
                this.mouse = setupTouch({
                    clientX: clientX / this.scaleX,
                    clientY: clientY / this.scaleY,
                    input: this.mouse ?? undefined,
                });
            }, false);
            document
                .getElementById("toggle-animation")
                .addEventListener("click", () => {
                this.playAnimation = !this.playAnimation;
                try {
                    localStorage.setItem("play-animation", this.playAnimation ? "true" : "");
                    if (!this.playAnimation) {
                        this.context.clearRect(0, 0, this.width, this.height);
                    }
                }
                catch (err) { }
                console.log(this.playAnimation);
            });
        };
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
        this.fontemonLogo = document.getElementById("fontemon");
        this.codeRelayLogo = [...new Array(4).keys()].map((i) => document.getElementById(`code-relay-0${i + 1}`));
        try {
            if (matchMedia("(prefers-reduced-motion)").matches) {
                this.playAnimation = false;
            }
            else {
                const shouldPlayAnimation = localStorage.getItem("play-animation");
                this.playAnimation =
                    shouldPlayAnimation ? true : false;
            }
        }
        catch (err) { }
        this.setupMouseAndTouchListeners();
        requestAnimationFrame(this.updateStateAndDraw);
    }
}
const setupTouch = ({ clientX, clientY, input: maybeInput, }) => {
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
const animationCanvasId = "animation-canvas";
const makeAnimationCanvas = (width, height, ratio) => {
    {
        const canvas = document.getElementById(animationCanvasId);
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
const makeAnimationCanvasElement = (width, height, ratio) => {
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

const defaultColors = {
    black: [[0, 0, 0, 255]],
    transparent: [
        [255, 255, 255, 255],
        [0, 0, 0, 0],
    ],
    lightGray: [[168, 168, 168, 255]],
    darkGray: [[96, 96, 96, 255]],
};

const colors = defaultColors;
const outputColors = {
    black: {
        style: "#000000",
        color: colors.black[0],
        position: {
            x: 0,
            y: 45,
            width: 20,
            height: 5,
        },
    },
    transparent: {
        style: "#ffffff",
        color: colors.transparent[0],
        position: {
            x: 0,
            y: 65,
            width: 20,
            height: 5,
        },
    },
    lightGray: {
        style: "#a8a8a8ff",
        color: colors.lightGray[0],
        position: {
            x: 0,
            y: 85,
            width: 20,
            height: 5,
        },
    },
    darkGray: {
        style: "#606060ff",
        color: colors.darkGray[0],
        position: {
            x: 0,
            y: 105,
            width: 20,
            height: 5,
        },
    },
};
const outputColorList = Object.entries(outputColors);

const colorHitBoxTest = (mousePosition, currentColors) => {
    for (const [i, { position: { x, y, width, height }, },] of currentColors.entries()) {
        if (mousePosition.x >= x &&
            mousePosition.x <= x + width &&
            mousePosition.y >= y &&
            mousePosition.y <= y + height) {
            return {
                inputColorIndex: i,
                type: "input",
            };
        }
    }
    for (const [outputType, { position: { x, y, width, height }, },] of outputColorList) {
        if (mousePosition.x >= x &&
            mousePosition.x <= x + width &&
            mousePosition.y >= y &&
            mousePosition.y <= y + height) {
            return {
                name: outputType,
                type: "output",
            };
        }
    }
    return {
        type: "none",
    };
};

const changeExtension = (filename, extension) => filename.replace(/\.[^\.]+$/, `.${extension}`);

const extensionToCharString = (filename) => changeExtension(filename, "charstring");

const callSubroutineCommand = (subroutineNumber) => `${subroutineNumber} callsubr\n`;

const havePixelRun = ({ pixel, nextPixel }) => {
    if (nextPixel === undefined) {
        return false;
    }
    if (nextPixel.y !== pixel.y) {
        return false;
    }
    if (nextPixel.x !== pixel.x + 1) {
        return false;
    }
    return true;
};

const findRuns = ({ notBlankPixels, index }) => {
    const pixel = notBlankPixels[index];
    const nextPixel = notBlankPixels[index + 1];
    if (!havePixelRun({ pixel, nextPixel })) {
        return null;
    }
    const runNumber = _findRuns({
        notBlankPixels,
        nextColorShouldBe: pixel.color,
        currentRunNumber: 1,
        index: index + 1,
    });
    const runType = `${pixel.color}${nextPixel.color}`;
    return {
        runNumber,
        runType,
    };
};
const _findRuns = ({ notBlankPixels, index, currentRunNumber, nextColorShouldBe, }) => {
    if (currentRunNumber >= 23) {
        return currentRunNumber;
    }
    const pixel = notBlankPixels[index];
    const nextPixel = notBlankPixels[index + 1];
    if (!havePixelRun({ pixel, nextPixel }) ||
        nextPixel.color !== nextColorShouldBe) {
        return currentRunNumber;
    }
    return _findRuns({
        notBlankPixels,
        index: index + 1,
        currentRunNumber: currentRunNumber + 1,
        nextColorShouldBe: pixel.color,
    });
};

const getDrawCommand = (input) => {
    const runs = findRuns(input);
    if (!runs) {
        return {
            dataConsumed: 1,
            drawCommand: callSubroutineCommand(-103 + input.color),
        };
    }
    const { runNumber, runType } = runs;
    const num = (() => {
        switch (runType) {
            case "00":
                return -99;
            case "11":
                return -76;
            case "22":
                return -53;
            case "01":
                return -30;
            case "02":
                return -7;
            case "12":
                return 16;
            case "10":
                return 39;
            case "20":
                return 62;
            case "21":
                return 85;
            default:
                console.error(`unrecognized runtype ${runType}`);
                return -100;
        }
    })() +
        runNumber -
        1;
    return {
        dataConsumed: runNumber + 1,
        drawCommand: callSubroutineCommand(num),
    };
};

const horizontalMoveToCommand = ({ dx }) => `${dx} hmoveto\n`;

const relativeMoveToCommand = ({ dx, dy, }) => `${dx} ${dy} rmoveto\n`;

const getMoveCommand = ({ pixel: { x, y }, lastPixel: { x: lastX, y: lastY }, pixelHeight, pixelWidth, }) => {
    if (lastY === y) {
        if (x === lastX + 1) {
            return "";
        }
        return horizontalMoveToCommand({
            dx: (x - lastX - 1) * pixelWidth,
        });
    }
    return relativeMoveToCommand({
        dx: (x - lastX - 1) * pixelWidth,
        dy: (y - lastY) * pixelHeight * -1,
    });
};

const pixelWidth = 12;
const pixelHeight = 12;

const colorEqual = ([tr, tg, tb, ta], [r, g, b, a]) => tr === r && tg === g && tb === b && ta === a;

const transparent = Symbol("transparent");
const noMatch = Symbol("noMatch");
const matchColor = ({ colors: { transparent: transparentColor, lightGray, darkGray, black }, color, }) => {
    const isEqualToColor = (c) => colorEqual(c, color);
    if (transparentColor.some(isEqualToColor)) {
        return transparent;
    }
    if (black.some(isEqualToColor)) {
        return 0;
    }
    if (darkGray.some(isEqualToColor)) {
        return 1;
    }
    if (lightGray.some(isEqualToColor)) {
        return 2;
    }
    return noMatch;
};

const getImageDataInfo = ({ imageData: { width, height, data }, colors, }) => {
    const bitWidth = 4;
    const stride = bitWidth * width;
    const notBlankPixels = [];
    for (let k = 0; k < height; k += 1) {
        for (let i = k * stride; i < (k + 1) * stride; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            const a = data[i + 3];
            const color = matchColor({
                colors,
                color: [r, g, b, a],
            });
            switch (color) {
                case transparent:
                    continue;
                case noMatch:
                    throw new Error(`Unrecognized color ${[r, g, b, a]}`);
            }
            notBlankPixels.push({
                x: (i % stride) / 4,
                y: k,
                color,
            });
        }
    }
    return notBlankPixels;
};

const imageDataToCharStringWithoutInitialPosition = (input) => {
    const notBlankPixels = getImageDataInfo(input);
    const firstCommand = callSubroutineCommand(-103 + notBlankPixels[0].color);
    let allCommands = firstCommand + "\n";
    for (let i = 1; i < notBlankPixels.length;) {
        const pixel = notBlankPixels[i];
        const lastPixel = notBlankPixels[i - 1];
        const moveCommand = getMoveCommand({
            pixelHeight,
            pixelWidth,
            lastPixel,
            pixel,
        });
        const { drawCommand, dataConsumed } = getDrawCommand({
            notBlankPixels,
            index: i,
            color: pixel.color,
        });
        i += dataConsumed;
        allCommands += moveCommand + drawCommand;
    }
    const endPixel = notBlankPixels[notBlankPixels.length - 1];
    return {
        commands: allCommands,
        initialPosition: {
            x: notBlankPixels[0].x,
            y: notBlankPixels[0].y,
        },
        endPosition: {
            x: endPixel.x,
            y: endPixel.y,
        },
    };
};

const saveDataUrl = ({ dataURL, fileName }) => {
    const link = document.createElement("a");
    link.download = fileName;
    link.target = "_blank";
    link.href = dataURL;
    link.click();
};

const convertAndSave = (image, imageFileName) => {
    const charString = imageDataToCharStringWithoutInitialPosition({
        imageData: image,
        colors,
    });
    saveDataUrl({
        dataURL: `data:text/plain;base64,${btoa(JSON.stringify(charString))}`,
        fileName: extensionToCharString(imageFileName),
    });
};

const mousePositionToPixelPosition = (mousePosition, leftBound, topBound) => {
    const x = Math.floor(mousePosition.x - leftBound);
    const y = Math.floor(mousePosition.y - topBound);
    return {
        x,
        y,
    };
};

const drawCrossHairs = (context, control, mousePosition, keyboardPosition, leftBound, topBound) => {
    const { x, y } = control == "mouse"
        ? mousePositionToPixelPosition(mousePosition, leftBound, topBound)
        : keyboardPosition;
    if (x >= 0 && y >= 0) {
        context.fillStyle = "red";
        context.fillRect(leftBound, y + topBound, x, 2);
        context.fillRect(x + leftBound, topBound, 2, y);
    }
};

const drawCurrentColors = (context, currentColors) => {
    context.fillStyle = "black";
    context.fillText("Input Colors:", 0, 120);
    for (const [i, { style, position }] of currentColors.entries()) {
        context.fillStyle = "black";
        context.fillText(`${i}:`, position.x - 10, position.y + 5);
        context.fillStyle = style;
        context.fillRect(position.x, position.y, position.width, position.height);
    }
};

const drawOutputColors = (context) => {
    context.fillStyle = "black";
    context.fillText("Output Colors:", 0, 0 + 15);
    for (const [name, { style, position: { x, y, width, height }, },] of outputColorList) {
        context.fillStyle = "black";
        context.fillText(name + ":", x, y - 5);
        context.fillStyle = style;
        context.fillRect(x, y, width, height);
    }
};

const drawStrokeBox = (context, { x, y, width, height }, color) => {
    context.strokeStyle = color;
    context.strokeRect(x - 2, y - 2, width + 4, height + 4);
};

const drawColorDescription = (context, color, x, y) => {
    context.fillStyle = "black";
    context.fillText(`Color Value: ${JSON.stringify(color)}`, x, y);
};

const drawSelection = (context, selection, currentColors, colorDescriptionX, colorDescriptionY) => {
    switch (selection.type) {
        case "none":
            return;
        case "highlighted": {
            const { position, color } = currentColors[selection.inputColorIndex];
            drawStrokeBox(context, position, "orange");
            drawColorDescription(context, color, colorDescriptionX, colorDescriptionY);
            return;
        }
        case "selected": {
            const { position, color } = currentColors[selection.inputColorIndex];
            drawStrokeBox(context, position, "red");
            drawColorDescription(context, color, colorDescriptionX, colorDescriptionY);
            return;
        }
        case "output_highlighted": {
            const { position, color } = outputColors[selection.outputColor];
            drawStrokeBox(context, position, "red");
            drawColorDescription(context, color, colorDescriptionX, colorDescriptionY);
            return;
        }
    }
};

const yPositionCurrentColor = (i) => i * 10 + 130;

const getAllColorsFromAnImage = ({ data, width, height }, skipOutputVersion) => {
    const currentColors = [];
    const outputColors = new Set();
    for (let i = 0; i < width * height * 4; i += 4) {
        let colorMatch = false;
        for (let k = 0; k < currentColors.length; k++) {
            const { color } = currentColors[k];
            for (let g = 0; g < 4; g++) {
                if (color[g] != data[i + g]) {
                    colorMatch = false;
                    break;
                }
                colorMatch = true;
            }
            if (colorMatch) {
                break;
            }
        }
        if (colorMatch) {
            continue;
        }
        if (!skipOutputVersion) {
            for (const [outputColorName, { color }] of outputColorList) {
                for (let g = 0; g < 4; g++) {
                    if (color[g] != data[i + g]) {
                        colorMatch = false;
                        break;
                    }
                    colorMatch = true;
                }
                if (colorMatch) {
                    outputColors.add(outputColorName);
                    break;
                }
            }
            if (colorMatch) {
                continue;
            }
        }
        const color = [data[i], data[i + 1], data[i + 2], data[i + 3]];
        currentColors.push({
            style: `#${color.map((a) => a.toString(16).padStart(2, "0")).join("")}`,
            color,
            position: {
                x: 10,
                y: yPositionCurrentColor(currentColors.length),
                width: 20,
                height: 5,
            },
        });
        if (currentColors.length > 200) {
            break;
        }
    }
    return {
        inputColors: currentColors,
        outputColors,
    };
};

const imageStringToImageData = async (imageString) => {
    const image = new Image();
    return new Promise((resolve, reject) => {
        image.onload = () => {
            const canvas = document.createElement("canvas");
            canvas.width = image.width;
            canvas.height = image.height;
            const context = canvas.getContext("2d");
            context.drawImage(image, 0, 0);
            resolve(context.getImageData(0, 0, image.width, image.height));
        };
        image.onerror = (ev) => {
            reject(typeof ev == "string" ? ev : ev.message);
        };
        image.src = imageString;
    });
};

const readToDataURL = (data) => new Promise((resolve) => {
    const reader = new FileReader();
    reader.addEventListener("loadend", () => {
        resolve(reader.result.toString());
    });
    reader.readAsDataURL(data);
});

const blobToImageData = async (blob) => {
    const dataURL = await readToDataURL(blob);
    return imageStringToImageData(dataURL);
};

const listenForImageChanges = (onNewImageData) => {
    const imageFile = document.getElementById("image-file");
    imageFile.addEventListener("change", async () => {
        const imageData = await blobToImageData(imageFile.files[0]);
        const imageFileName = imageFile.files[0].name;
        onNewImageData(imageData, imageFileName);
    });
};

const loadImagePath = "/loadImage";

const loadImageByFilePath = async (filePath) => {
    const input = {
        filePath,
    };
    const response = await fetch(new Request(loadImagePath, {
        method: "POST",
        body: JSON.stringify(input),
    }));
    if (!response.ok) {
        throw new Error(await response.text());
    }
    return blobToImageData(await response.blob());
};

const nextImagePath = "/nextImage";

const nextFilePathHeader = "next-file-path";

const loadNextImageByFilePath = async (filePath) => {
    const input = {
        imageFilePath: filePath,
    };
    const response = await fetch(new Request(nextImagePath, {
        method: "POST",
        body: JSON.stringify(input),
    }));
    const fileName = response.headers.get(nextFilePathHeader);
    if (!response.ok) {
        throw new Error(await response.text());
    }
    return {
        data: await blobToImageData(await response.blob()),
        fileName,
    };
};

const selectMatchingColor = (pixels, i, currentColors) => {
    for (let k = 0; k < currentColors.length; k++) {
        const { color } = currentColors[k];
        let colorMatch = false;
        for (let g = 0; g < 4; g++) {
            if (color[g] != pixels[i + g]) {
                colorMatch = false;
                break;
            }
            colorMatch = true;
        }
        if (colorMatch) {
            return {
                type: "highlighted",
                inputColorIndex: k,
            };
        }
    }
    for (const [name, { color }] of outputColorList) {
        let colorMatch = false;
        for (let g = 0; g < 4; g++) {
            if (color[g] != pixels[i + g]) {
                colorMatch = false;
                break;
            }
            colorMatch = true;
        }
        if (colorMatch) {
            return {
                type: "output_highlighted",
                outputColor: name,
            };
        }
    }
    return null;
};

const nextSelectionState = (selection, imageData, currentColors, control, mousePosition, keyboardPosition, leftBound, topBound) => {
    switch (selection.type) {
        case "selected":
            return selection;
    }
    if (!imageData) {
        return selection;
    }
    const { x, y } = control == "mouse"
        ? mousePositionToPixelPosition(mousePosition, leftBound, topBound)
        : keyboardPosition;
    if (x < 0 || y < 0 || x > imageData.width || y > imageData.height) {
        switch (selection.type) {
            case "highlighted":
            case "output_highlighted":
                return {
                    type: "none",
                };
        }
        return selection;
    }
    const i = 4 * (x + y * imageData.width);
    const matchingState = selectMatchingColor(imageData.data, i, currentColors);
    if (matchingState == null) {
        return selection;
    }
    return matchingState;
};

const removeQuotes = (string) => {
    const hasQuotes = /^"([^"]+)"$/.exec(string);
    if (!hasQuotes) {
        return string;
    }
    const [, actualValue] = hasQuotes;
    return actualValue;
};

const replaceInputColorWithOutputColor = (outputColorKey, imageData, oldColor) => {
    const { data, width, height } = imageData;
    const outputColor = outputColors[outputColorKey];
    for (let i = 0; i < width * height * 4; i += 4) {
        let colorMatch = false;
        for (let g = 0; g < 4; g++) {
            if (oldColor.color[g] != data[i + g]) {
                colorMatch = false;
                break;
            }
            colorMatch = true;
        }
        if (!colorMatch) {
            continue;
        }
        for (let g = 0; g < 4; g++) {
            data[i + g] = outputColor.color[g];
        }
    }
};

const replaceImageDataWithGuessedColors = ({ width, height, data }, colors) => {
    const bitWidth = 4;
    const stride = bitWidth * width;
    for (let k = 0; k < height; k++) {
        for (let i = k * stride; i < (k + 1) * stride; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            const a = data[i + 3];
            switch (matchColor({
                colors,
                color: [r, g, b, a],
            })) {
                case transparent:
                    data[i] = 0;
                    data[i + 1] = 0;
                    data[i + 2] = 0;
                    data[i + 3] = 0;
                    continue;
                case noMatch:
                    break;
                default:
                    continue;
            }
            const color = 0;
            data[i] = color;
            data[i + 1] = color;
            data[i + 2] = color;
            data[i + 3] = 255;
        }
    }
};

const imageToDataURL = (image) => {
    const canvas = document.createElement("canvas");
    canvas.width = image.width;
    canvas.height = image.height;
    const newData = new ImageData(image.width, image.height);
    newData.data.set(image.data);
    replaceImageDataWithGuessedColors(newData, colors);
    canvas.getContext("2d").putImageData(newData, 0, 0);
    return canvas.toDataURL();
};

const saveFilePath = "/saveFile";

const saveCompleteFile = async ({ charStringInfo, pngURL, name, }) => {
    const saveFileInput = {
        charStringInfo: JSON.stringify(charStringInfo),
        pngURL,
        name,
    };
    try {
        const response = await fetch(new Request(saveFilePath, {
            method: "POST",
            body: JSON.stringify(saveFileInput),
        }));
        if (response.ok) {
            return {
                type: "ok",
            };
        }
        const text = await response.text();
        return {
            type: "error",
            text,
        };
    }
    catch (err) {
        return {
            type: "error",
            text: err.message,
        };
    }
};

const saveBoth = async (image, saveFileName) => {
    try {
        const pngURL = imageToDataURL(image);
        const charStringInfo = imageDataToCharStringWithoutInitialPosition({
            imageData: image,
            colors,
        });
        return await saveCompleteFile({
            charStringInfo,
            pngURL,
            name: saveFileName,
        });
    }
    catch (err) {
        return {
            type: "error",
            text: err.message
        };
    }
};

const saveImage = (image, fileName) => {
    saveDataUrl({ dataURL: imageToDataURL(image), fileName });
};

class Converter {
    constructor() {
        this.image = null;
        this.width = 500;
        this.height = 500;
        this.scale = 1;
        this.imageStartX = 70;
        this.imageStartY = 70;
        this.undoStack = [];
        this.mousePosition = { x: -Infinity, y: -Infinity };
        this.keyboardPosition = {
            x: 0,
            y: 0,
        };
        this.control = "mouse";
        this.selection = {
            type: "none",
        };
        this.currentColors = [];
        this.updateStateAndDraw = (_totalTimeElapsed) => {
            this.updateState();
            this.draw();
            requestAnimationFrame(this.updateStateAndDraw);
        };
        this.updateState = () => {
            this.updateCursor();
            this.updateSelectionState();
        };
        this.updateCursor = () => {
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
        this.updateSelectionState = () => {
            this.selection = nextSelectionState(this.selection, this.image ? this.image.data : null, this.currentColors, this.control, this.mousePosition, this.keyboardPosition, this.imageStartX, this.imageStartY);
        };
        this.draw = () => {
            this.context.clearRect(0, 0, this.width, this.height);
            this.context.fillStyle = "gray";
            this.context.fillRect(this.imageStartX, this.imageStartY, 500, 500);
            if (this.image) {
                this.imageCanvas.getContext("2d").putImageData(this.image.data, 0, 0);
                this.context.drawImage(this.imageCanvas, this.imageStartX, this.imageStartY);
            }
            drawOutputColors(this.context);
            drawCurrentColors(this.context, this.currentColors);
            drawSelection(this.context, this.selection, this.currentColors, this.imageStartX, this.imageStartY - 20);
            drawCrossHairs(this.context, this.control, this.mousePosition, this.keyboardPosition, this.imageStartX, this.imageStartY);
        };
        this.mouseEventToMousePosition = ({ offsetX, offsetY, }) => ({
            x: offsetX / this.scale,
            y: offsetY / this.scale,
        });
        this.setupMouseAndTouchListeners = () => {
            this.canvas.addEventListener("mousemove", (event) => {
                this.mousePosition = this.mouseEventToMousePosition(event);
            }, false);
            window.addEventListener("click", this.handleCanvasClick);
            document
                .getElementById("save-charstring")
                .addEventListener("click", () => {
                if (!this.image) {
                    return;
                }
                convertAndSave(this.image.data, this.image.fileName);
            });
            document.getElementById("save-image").addEventListener("click", () => {
                if (!this.image) {
                    return;
                }
                saveImage(this.image.data, this.image.fileName);
            });
            document.getElementById("undo-button").addEventListener("click", () => {
                if (!this.image || this.undoStack.length <= 0) {
                    return;
                }
                const { image, currentColors } = this.undoStack.pop();
                this.image = image;
                this.setFileNameInput(image.fileName);
                this.currentColors = currentColors;
            });
            document.getElementById("scale").addEventListener("change", (e) => {
                this.context.resetTransform();
                this.scale = e.target.value;
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
                .getElementById("load-by-path")
                .addEventListener("click", async () => {
                const filePath = this.imageFileInput;
                if (!filePath) {
                    return;
                }
                try {
                    this.clearLoadImageError();
                    const data = await loadImageByFilePath(filePath);
                    this.onNewImage(data, filePath);
                }
                catch (err) {
                    this.setLoadImageError(err.message);
                }
            });
            document.getElementById("next").addEventListener("click", async () => {
                const filePath = this.imageFileInput;
                if (!filePath) {
                    return;
                }
                try {
                    this.clearLoadImageError();
                    const { data, fileName } = await loadNextImageByFilePath(filePath);
                    this.onNewImage(data, fileName);
                    this.imageFilePathInput.value = fileName;
                }
                catch (err) {
                    this.setLoadImageError(err.message);
                }
            });
            window.addEventListener("keydown", ({ key }) => {
                if (document.activeElement != null &&
                    document.activeElement != document.body) {
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
                    const { x, y } = mousePositionToPixelPosition(this.mousePosition, this.imageStartX, this.imageStartY);
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
        this.onNewImage = (imageData, fileName) => {
            this.image = {
                data: imageData,
                fileName: fileName,
            };
            this.setFileNameInput(fileName);
            this.currentColors = getAllColorsFromAnImage(this.image.data, true).inputColors;
            this.imageCanvas
                .getContext("2d")
                .clearRect(0, 0, this.imageCanvas.width, this.imageCanvas.height);
            this.imageCanvas.width = this.image.data.width;
            this.imageCanvas.height = this.image.data.height;
        };
        this.setSaveStatus = (status) => {
            document.getElementById("save-status").innerText = status;
        };
        this.setLoadImageError = (error) => {
            document.getElementById("load-image-error").innerText = error;
        };
        this.clearLoadImageError = () => {
            document.getElementById("load-image-error").innerText =
                "";
        };
        this.setFileNameInput = (fileName) => {
            const parts = removeQuotes(fileName)
                .replace(/\.[^\.]+$/, "")
                .split(/[\\/]/);
            this.saveFileNameInput.value = parts[parts.length - 1];
        };
        this.onColorBoxClick = (hitBoxTest) => {
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
        this.moveColor = (inputColorIndex, outputColorKey) => {
            if (!this.image) {
                return;
            }
            const newData = new ImageData(this.image.data.width, this.image.data.height);
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
        this.handleCanvasClick = (event) => {
            const hitBoxTest = colorHitBoxTest(this.mouseEventToMousePosition(event), this.currentColors);
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
        this.selectOrClearSelection = () => {
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
        this.canvas = document.getElementById("canvas");
        this.imageCanvas = document.createElement("canvas");
        this.context = this.canvas.getContext("2d");
        this.saveFileNameInput = document.getElementById("file-name");
        this.imageFilePathInput = document.getElementById("image-file-path");
        this.context.imageSmoothingEnabled = false;
        this.context.scale(this.scale, this.scale);
        this.setupMouseAndTouchListeners();
        requestAnimationFrame(this.updateStateAndDraw);
    }
    get controlPosition() {
        if (this.control == "mouse") {
            return mousePositionToPixelPosition(this.mousePosition, this.imageStartX, this.imageStartY);
        }
        return this.keyboardPosition;
    }
    get imageFileInput() {
        const { value } = this.imageFilePathInput;
        if (!value) {
            return null;
        }
        return removeQuotes(value);
    }
}
window.onload = () => {
    new Converter();
    new BackgroundImage();
};
