# Buttons
The `buttons` element consists of a list of buttons. Each `button` object can contain the following elements. 

| Element             | Mandatory          | Description |
|---------------------|:------------------:|----------|
| `index`             | :white_check_mark: | Index of the button. 1-16 for layer A, 17-32 for layer B  |
| `event_press`       | :negative_squared_cross_mark: | The event to execute when the button is pressed down |
| `event_short_press` | :negative_squared_cross_mark: | The event to execute when the button is pressed and released |
| `event_long_press`  | :negative_squared_cross_mark: | The event to execute when the button is pressed for 0.5 seconds and released |
| `simvar_led`        | :negative_squared_cross_mark: | The simvar to monitor for setting the button led |

## Event press
The `event_press`, `event_short_press` and `event_long_press` give the option to fire off an event when a button is pressed.
The following example toggles the flight director on the autopilot of the plane.
```json
{
  "index": 1,
  "event_press": "TOGGLE_FLIGHT_DIRECTOR",
},
```
These events also support manual events and conditional events, information about those can be found in the advanced section.

## Simvar led
The X-Touch has illuminated buttons so it is possible to view the status of simvars. This means that the LEDs are always syncronized with what's happening in the plane. You can enable something with this application and then use a mouse in the cockpit to disable it the LED always indicates the actual status. The previous example has now been expanded to make sure the LED indicates the status of the flight director.
```json
{
  "index": 1,
  "event_press": "TOGGLE_FLIGHT_DIRECTOR",
  "simvar_led": "AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE"
},
```