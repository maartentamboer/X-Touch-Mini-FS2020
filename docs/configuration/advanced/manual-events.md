# Manual events
Manual events give the option to attach a value when an event is called. 

| Element       | Mandatory                     | Description |
|---------------|:-----------------------------:|----------|
| `event`       | :white_check_mark:            | The event to call |
| `type`        | :white_check_mark:            | Always set to `manual` |
| `value`       | :white_check_mark:            | The value to send with the event |
| `description` | :negative_squared_cross_mark: | Description for your own reference |


## Example
For example to select the speed mode in the A320 `SPEED_SLOT_INDEX_SET` event can be set to 1 for selected mode and 2 for managed mode.
```json
"event_short_press": {
  "event": "SPEED_SLOT_INDEX_SET",
  "type": "manual",
  "value": 1,
  "description": "A32NX - set AP Speed Hold to selected mode"
},
"event_long_press": {
  "event": "SPEED_SLOT_INDEX_SET",
  "type": "manual",
  "value": 2,
  "description": "A32NX - set AP Speed Hold to managed mode"
}
```