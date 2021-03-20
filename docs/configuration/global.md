# Global configuration file
The global configuration file consists of multiple parts.

| Element              | Description |
|----------------------|-------------|
| `default`            | The default configuration to be loaded |
| `aircraft`           | Aircraft specific configurations |
| `midi_input_device`  | The name of the midi input |
| `midi_output_device` | The name of the midi output |
| `additional_simvars` | Extra simvars that are not available in python-simconnect |

## Default
Which json file to load when there is no match from the `aircraft_contains` elements of the `aircraft` element.
```json
"default": "config_default.json",
```

## Aircraft
!!! warning inline end
    Please note that the name of the aircraft can be different when selecting another livery, so select an identifier that is always there.
Load a specific config file when the name of the aircraft contains a specific string. To find out the name of your aircraft look at the output of the application when you switch aircraft.
```json
"aircraft": [
  {
    "aircraft_contains": "A320",
    "file": "config_a320.json"
  }
],
```

## Midi input & output device
Generally this is always `X-TOUCH MINI 0` for the input and `X-TOUCH MINI 1` for the output. But if you have more midi devices connected to your PC it might be different. To find out which device you need to select, launch the application and it will print out the found input and output devices.
```json
"midi_input_device": "X-TOUCH MINI 0",
"midi_output_device": "X-TOUCH MINI 1",
```

## Additional simvars
This is an advanced use case. This application uses the Python-SimConnect library to communicate with the Flight Simulator, but the library does not have all the simvars built in. To find out which simvars are built in look in the [RequestList.py](https://github.com/odwdinc/Python-SimConnect/blob/master/SimConnect/RequestList.py). Any additional simvars can be defined in this element.
```json
"additional_simvars": [
  {
    "name": "APU_SWITCH",
    "description": "When the APU is available",
    "simvar": "APU SWITCH",
    "type": "Bool",
    "writable": false
  }
]
```

| Element              | Description |
|----------------------|-------------|
| `name`            | The name that you reference in the config files |
| `description`           | Description |
| `simvar`  | Name of the actual simvar in MSFS |
| `type` | The type of the simvar, view Requestlist.py for possibilities |
| `writable` | `true` when you can write to the simvar |