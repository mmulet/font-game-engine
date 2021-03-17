import { readdirSync } from "fs";
import { dirname, join } from "path";
import { writeFileSync } from "fs";
const makeDirectory = (path, makeType = false) => {
  const entries = readdirSync(path, {
    withFileTypes: true,
  });
  const out = {};
  let empty = true;
  /**
   * kebobCase to camel case
   */
  for (const entry of entries) {
    if (!entry.isDirectory()) {
      continue;
    }
    const entryKey = entry.name.replace(/-(.)/g, (_match, letterAfterKebob) =>
      letterAfterKebob !== "-" ? letterAfterKebob.toUpperCase() : ""
    );
    switch (entry.name) {
      case "node_modules":
      case ".git":
      case ".vscode":
      case "__pycache__":
        continue;
      case "fontTools":
        out[entryKey] = makeType ? "string" : join(path, "fontTools");
        empty = false;
        continue;
      default:
        break;
    }
    out[entryKey] = makeDirectory(join(path, entry.name), makeType);
    empty = false;
  }
  if (empty) {
    return makeType ? "string" : path;
  }
  out["path"] = makeType ? "string" : path;
  return out;
};

const getProjectRootDirectory = () => {
  const projectDirectoriesSubFolder = dirname(
    new URL(import.meta.url).pathname.substring(1)
  );
  const projectDirectories = dirname(projectDirectoriesSubFolder);
  const projectDirectoriesSrc = join(projectDirectories, "src");
  const libDirectory = dirname(projectDirectories);
  const projectRootDirectory = dirname(libDirectory);
  return { projectRootDirectory, projectDirectoriesSrc };
};
const {
  projectRootDirectory,
  projectDirectoriesSrc,
} = getProjectRootDirectory();
writeFileSync(
  join(projectDirectoriesSrc, "index.ts"),
  `//@ts-nocheck
  /**
*   This is an auto generated file. Do not modify. Modify 
*   or run ./generate/index.j instead
*/
import { readdirSync } from "fs";
import { dirname, join } from "path";

export interface ProjectDirectories  ${JSON.stringify(
    makeDirectory(projectRootDirectory, true)
  ).replace(/"string"/g, "string")};
  
const makeDirectory = ${makeDirectory.toString()}

const getProjectRootDirectory = ${getProjectRootDirectory.toString()}

export const directories : ProjectDirectories = makeDirectory(getProjectRootDirectory().projectRootDirectory)
  `
);
