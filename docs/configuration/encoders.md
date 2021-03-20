# Encoders
The `encoders` element consists of a list of encoders. Each `encoder` object can contain the following elements. 

| Element                | Mandatory          | Description |
|------------------------|:------------------:|----------|
| `index`                | :white_check_mark: | Index of the encoder. 1-8 for layer A, 9-16 for layer B  |
| `event_up`             | :white_check_mark: | The event to execute for CW rotation ticks |
| `event_down`           | :white_check_mark: | The event to execute for CCW rotation ticks |
| `alternate_event_up`   | :negative_squared_cross_mark: | The alternate event to execute for CW rotation ticks |
| `alternate_event_down` | :negative_squared_cross_mark: | The alternate event to execute for CCW rotation ticks |
| `event_press`          | :negative_squared_cross_mark: | The event to execute when the button is pressed down |
| `event_short_press`    | :negative_squared_cross_mark: | The event to execute when the button is pressed and released |
| `event_long_press`     | :negative_squared_cross_mark: | The event to execute when the button is pressed for 0.5 seconds and released |

## Event up, down
The most basic configuration of an encoder just consists of the `index` and the `event_up` / `event_down`. The next example modifies the Baro setting of the airplane. It does this by sending the `KOHLSMAN_INC` event when the encoder is rotated CW and sending the `KOHLSMAN_DEC` event for CCW rotation.   
```json
{
  "index": 1,
  "event_up": "KOHLSMAN_INC",
  "event_down": "KOHLSMAN_DEC",
},
```
These events also support manual events and conditional events, information about those can be found in the advanced section.

## Event press
The `event_press`, `event_short_press` and `event_long_press` give the option to fire off an event when a button is pressed.
```json
{
  "index": 1,
  "event_up": "KOHLSMAN_INC",
  "event_down": "KOHLSMAN_DEC",
  "event_press": "BAROMETRIC"
},
```
These events also support manual events and conditional events, information about those can be found in the advanced section.

## Alternate events
Sometimes you want to have a single encoder control multiple things. This can be achieved by setting up an alternate. The next example shows how to control the NAV1 radio. The encoder is able to control the whole increments and the fractional increments. When the button has a short press it sees the `{alternate}` keyword and therefore knows that the encoder must be switched between whole and fractional.
```json
{
  "index": 6,
  "event_up": "NAV1_RADIO_WHOLE_INC",
  "event_down": "NAV1_RADIO_WHOLE_DEC",
  "alternate_event_up": "NAV1_RADIO_FRACT_INC",
  "alternate_event_down": "NAV1_RADIO_FRACT_DEC",
  "event_short_press": "{alternate}",
  "event_long_press": "NAV1_RADIO_SWAP"
},
```

*[CW]: ClockWise
*[CCW]: CounterClockWise