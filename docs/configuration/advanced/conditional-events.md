# Conditional events
Conditional events give the option to run a script whenever it's executed.
They can be used in `event_*` or in the triggers section.

| Element       | Mandatory                     | Description |
|---------------|:-----------------------------:|----------|
| `type`        | :white_check_mark:            | `condition` or `condition-file` |
| `event`       | :white_check_mark:            | When on `condition` an array of strings. When on `condition-file` the path to a jinja2 file |
| `description` | :negative_squared_cross_mark: | Description for your own reference |

## Condition
This is the older syntax where the script is directly defined in the json file.
It is not very readable so the `condition-file` is a better option, especially for larger scripts.
```json
{
  "trigger_type": "condition",
  "simvar": "AUTOPILOT_HEADING_LOCK_DIR",
  "condition": [ "{% set heading = (data.get_simvar_value('AUTOPILOT_HEADING_LOCK_DIR') / 27.0) | round %}",
                  "{{ data.set_encoder_led_value(2, heading) }}"]
}
```

## Condition file
`condition-file` enables the condition to be made in a seperate file. This enables syntax highlighting in Visual Studio Code and leaves the json file readable.
```json
"event_press": {
  "type": "condition-file",
  "event": "Functions/Generic/heading-bug-sync.jinja2",
  "description": "Set heading bug to current heading"
}
```
```jinja
{# Set the heading bug to the current flown heading #}
{# HEADING_INDICATOR returns in radians but HEADING_BUG_SET needs it in degrees  #}
{% set heading = (data.get_simvar_value('HEADING_INDICATOR') * 180 / 3.14) | round %}
{{ data.trigger_event('HEADING_BUG_SET', heading) }}
```

## Condition syntax
The condition uses [jinja2](https://jinja.palletsprojects.com/en/2.11.x/) to execute the script. To understand the full capabilities of this read the [Template Designer Documentation](https://jinja.palletsprojects.com/en/2.11.x/templates/).

### Available functions
In the jinja code there is a data object available which is an instance of the [conditionalrunner.py](https://github.com/maartentamboer/X-Touch-Mini-FS2020/blob/main/conditionalrunner.py). With this object functions can be called to execute specific actions.

| Function | Description |
|----------|-------------|
| `#!python data.get_simvar_value(name: str)` | Get the value of a simvar |
| `#!python data.set_simvar_value(name: str, value)` | Set the value of a simvar |
| `#!python data.trigger_event(name: str, value)` | Trigger an event |
| `#!python data.trigger_encoder_alternate(index: int, value: bool)` | Trigger the alternate mode of an encoder |
| `#!python data.set_global_variable(key: str, value)` | Set a variable in the application, this can be used in other conditions, |
| `#!python data.get_global_variable(key: str)` | Get a variable from the application |
| `#!python data.print(data)` | Print something in the console output of the application |
| `#!python data.set_button_led(index: int, on: bool, blink=False)` | Set the LED of a button |
| `#!python data.set_encoder_led(index: int, on: bool, blink=False)` | Set the entire LED ring of an encoder |
| `#!python data.set_encoder_led_value(index: int, value: int, blink=False)` | Set the LED ring to a specific value |

## Examples with explanation
This first example can be used to synchronize the heading bug to the current flown heading.
First the `HEADING_INDICATOR` simvar is read, this returns the current heading in radians. 
These radians are then converted to degrees, rounded to a whole number and stored in the script variable `heading`.
The script variable is then used as the parameter for the `trigger_event` function.
```jinja
{# Set the heading bug to the current flown heading #}
{# HEADING_INDICATOR returns in radians but HEADING_BUG_SET needs it in degrees  #}
{% set heading = (data.get_simvar_value('HEADING_INDICATOR') * 180 / 3.14) | round %}
{{ data.trigger_event('HEADING_BUG_SET', heading) }}
```

This example monitors the `AUTOPILOT_VERTICAL_HOLD` simvar and triggers the alternate mode for an encoder.
The LED of the encoder is also updated based on the status.
```jinja
{% if data.get_simvar_value('AUTOPILOT_VERTICAL_HOLD') == 1.0 %}
    {{ data.trigger_encoder_alternate(5, True) }}
    {{ data.set_encoder_led(5, True) }}
{% else %}
    {{ data.trigger_encoder_alternate(5, False) }}
    {{ data.set_encoder_led(5, False) }}
{% endif %}
```