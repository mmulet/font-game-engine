import express from "express";
import open from "open";
import { directories } from "project-directories";
const app = express();
const port = 80;

app.use(
  "/",
  express.static(directories.testFontInBrowser.assets),
  express.static(directories.gameToFont.output, {
    setHeaders: (response) => {
      response.setHeader("Cache-Control", "no-store");
    },
  })
);

app.listen(port, "0.0.0.0", () => {
  console.log(`Example app listening on port ${port}!`);
  open(`http://localhost:${port}`);
});
