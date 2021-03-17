import express from "express";
import open from "open";
import bodyParser from "body-parser";
const { json } = bodyParser;
// import { saveFilePath, loadImagePath, nextImagePath } from "api";
import { saveFilePath } from "./saveFilePath.js";
import { loadImagePath } from "./loadImagePath.js";
import { nextImagePath } from "./nextImagePath.js";
import { directories } from "project-directories";
import { saveFile } from "./saveFile.js";
import { nextImage } from "./nextImage.js";
import { loadImage } from "./loadImage.js";
import { sendError } from "./sendError.js";
import { join } from "path";
const app = express();

const { gui } = directories.imageToCharStringConverter;

app.use(
  express.static(gui.assets, {
    extensions: ["js"],
  })
);

app.use(
  express.static(
    join(directories.blender.fontemon_blender_addon.path, "assets", "web"),
    {
      extensions: ["js"],
    }
  )
);

app.use(
  "/js",
  express.static(gui.js, {
    extensions: ["js"],
  })
);

app.use(
  "/src",
  express.static(gui.src, {
    extensions: ["js"],
  })
);

// app.use(
//   "/to-char-string",
//   express.static(directories.lib.toCharString.lib, {
//     extensions: ["js"],
//   })
// );

// app.use(
//   "/api",
//   express.static(gui.api.lib, {
//     extensions: ["js"],
//   })
// );
const jsonParser = json({ type: () => true });

app.post(loadImagePath, jsonParser, sendError(loadImage));

app.post(nextImagePath, jsonParser, sendError(nextImage));

app.post(saveFilePath, jsonParser, sendError(saveFile));

const port = 4234;
app.listen(port, () => {
  console.log("listening on ", port);
  open(`http://localhost:${port}`);
});
