# Aircraft specific
The aircraft specific configuration file consists of multiple parts.

| Element              | Description |
|------------|-------------|
| `$schema`  | Indicate to the text editor which schema to use |
| `version`  | Version of the json format, currently use 1.0.0 |
| `encoders` | A list of the encoders |
| `buttons`  | A list of the buttons |
| `triggers` | A list of triggers |

## Schema
[JSON Schema](https://json-schema.org/) enables validation and autocompletion of json files.
```json
"$schema": "./config.schema.json",
```

## Version
The version element is here for the future in case a breaking change is introduced.
```json
"version": {
  "major": 1,
  "minor": 0,
  "patch": 0
},
```

## Others
All the other elements are explained in seperate pages.

