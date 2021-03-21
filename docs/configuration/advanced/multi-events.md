# Multiple events
It is possible to sent multiple events by defining an array for any of the events.
This example of a button toggles the flight director and AP master at the same time.
```json
{
  "index": 1,
  "event_press": [ "TOGGLE_FLIGHT_DIRECTOR", "AP_MASTER" ],
  "simvar_led": "AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE"
}
```