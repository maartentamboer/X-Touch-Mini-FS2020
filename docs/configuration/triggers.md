# Triggers
The `triggers` element consists of a list of trigger. Each `trigger` object can contain the following elements.
Triggers enable the application to act on a change of a simvar. For example to trigger an alternate of an encoder.

| Element         | Mandatory                     | Description |
|-----------------|:-----------------------------:|----------|
| `simvar`        | :white_check_mark:            | The simvar to monitor |
| `trigger_type`  | :white_check_mark:            | The type of the trigger |
| `trigger_index` | :negative_squared_cross_mark: | The index of the element to trigger |
| `condition`     | :negative_squared_cross_mark: | The condition when the `trigger_type` is set to condition |

## Type
Th `trigger_type` can be set to `encoder`, `condition` or `condition-file`. The 2 condition types are explained in the advanced section. The encoder type can be used to trigger the alternate mode of an encoder.

## Example
Most autopilot stacks have a single wheel to control either the vertical speed or the speed itself, depending whether it's in FLC or VS mode. 
To have a single encoder control both, an alternate must be added so the encoder can sent both events. To automatically switch between the alternates a trigger is made to monitor the `AUTOPILOT_VERTICAL_HOLD`. When `AUTOPILOT_VERTICAL_HOLD` is true the encoder is set to alternate, otherwise it's in the default setting.
```json
{
  "simvar": "AUTOPILOT_VERTICAL_HOLD",
  "trigger_type": "encoder",
  "trigger_index": 5
}
```
```json
{
  "index": 5,
  "event_up": "AP_SPD_VAR_INC",
  "event_down": "AP_SPD_VAR_DEC",
  "alternate_event_up": "AP_VS_VAR_INC",
  "alternate_event_down": "AP_VS_VAR_DEC"
}
```

*[FLC]: Flight Level Change
*[VS]: Vertical Speed