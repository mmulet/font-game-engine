# Project Directories

This library includes the full path of the project directories.
Generate the directories via

```bash
node ./generate/index.js
```

or

```bash
npm run gen
```

This will generate the entire project structure as a typescript interface.
Each string item of ProjectDirectories is the full system path for the
directory so it can be used in writeFile,readFile etc

* Note: kebob case directories are replaced with camelCase 
Example:
project-directories -> projectDirectories
