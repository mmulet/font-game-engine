//@ts-nocheck
  /**
*   This is an auto generated file. Do not modify. Modify 
*   or run ./generate/index.j instead
*/
import { readdirSync } from "fs";
import { dirname, join } from "path";

export interface ProjectDirectories  {"blender":{"blenderFiles":{"assets":{"fonts":{"Alfa_Slab_One":string,"Amatic_SC":string,"Anton":string,"Caveat":{"static":string,"path":string},"Cinzel":{"static":string,"path":string},"Indie_Flower":string,"Merriweather":string,"Mulish":{"static":string,"path":string},"Orbitron":{"static":string,"path":string},"Press_Start_2P":string,"path":string},"path":string},"output":{"hpBar":string,"mainCharacterWalk":string,"path":string},"path":string},"fontemon_blender_addon":{"Common":string,"CreateText":string,"SceneTreeEditor":string,"SizeImage":string,"path":string},"saveFiles":string,"path":string},"gameToFont":{"assets":string,"intermediate":string,"js":string,"output":string,"src":string,"path":string},"images":{"charStrings":string,"path":string},"imageToCharStringConverter":{"cli":{"js":string,"src":string,"path":string},"gui":{"api":{"lib":string,"src":string,"path":string},"assets":string,"dev":{"js":string,"src":string,"path":string},"js":string,"src":string,"path":string},"path":string},"lib":{"parseBdf":{"lib":string,"src":string,"path":string},"projectDirectories":{"generate":string,"lib":string,"src":string,"path":string},"toCharString":{"lib":string,"src":string,"path":string},"path":string},"python":{"compileFont":{"fontTools":string,"lap":string,"path":string},"stubs":{"bpy":{"app":string,"context_test":string,"data":string,"ops":string,"props":string,"types":string,"utils":string,"path":string},"bpy_extras":{"io_utils":string,"path":string},"fontTools":string,"lap":string,"nodeitems_utils":string,"path":string},"path":string},"testFontInBrowser":{"assets":string,"dev":string,"path":string},"textPreviewTool":{"assets":string,"dev":string,"js":string,"src":string,"path":string},"util":{"blackjack":{"goodGames":string,"js":string,"out":string,"src":string,"path":string},"inspectFont":string,"path":string},"path":string};
  
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
}

const getProjectRootDirectory = () => {
  const projectDirectoriesSubFolder = dirname(
    new URL(import.meta.url).pathname.substring(1)
  );
  const projectDirectories = dirname(projectDirectoriesSubFolder);
  const projectDirectoriesSrc = join(projectDirectories, "src");
  const libDirectory = dirname(projectDirectories);
  const projectRootDirectory = dirname(libDirectory);
  return { projectRootDirectory, projectDirectoriesSrc };
}

export const directories : ProjectDirectories = makeDirectory(getProjectRootDirectory().projectRootDirectory)
  