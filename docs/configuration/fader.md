# Fader
The `faders` element consists of a list of buttons. Each `fader` object can contain the following elements. 

| Element        | Mandatory          | Description |
|----------------|:------------------:|----------|
| `index`        | :white_check_mark: | Index of the fader. 1 for layer A, 2 for layer B  |
| `event_change` | :white_check_mark: | The event to execute when the fader is moved |
| `min_value`    | :white_check_mark: | The value to send when the fader is at the bottom |
| `max_value`    | :white_check_mark: | The value to send when the fader is at the top |