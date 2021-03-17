import express from "express";
import open from "open";
import { directories } from "project-directories";
import {join} from "path"
const app = express();
const { textPreviewTool } = directories;

app.use(
  express.static(textPreviewTool.assets, {
    extensions: ["js"],
  })
);
app.use(
  express.static(join(directories.blender.fontemon_blender_addon.path, "assets", "web"), {
    extensions: ["js"],
  })
);


app.use(
  "/js",
  express.static(textPreviewTool.js, {
    extensions: ["js"],
  })
);

// app.use(
//   "/parseBDF",
//   express.static(directories.lib.parseBdf.lib, {
//     extensions: ["js"],
//   })
// );

const port = 8734;
app.listen(port, () => {
  console.log("listening on ", port);
  open(`http://localhost:${port}`);
});
