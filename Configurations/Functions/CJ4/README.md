# Citation CJ4 configuration 

## Filter: "Cessna CJ4 Citation"

## Setup

### prerequisites
- [MobiFlight](https://www.mobiflight.com/) mod installed

### encoders (from left to right, starting with index `1`)

#### suffixes
- `d` - down
- `u` - up
- `p` - (short) press
- `l` - long press

#### configuration
- 1d. heading - decrease
- 1u. heading - increase
- 1p. heading - sync bug with current heading
- 1l. N/A

- 2d. barometric pressure - decrease
- 2u. barometric pressure - increase
- 2p. barometric pressure - synchronize with actual barometric pressure
- 2l. N/A

- 3d. (Auto Pilot) altitude - decrease
- 3u. (Auto Pilot) altitude - increase
- 3p. N/A
- 3l. N/A

- 4d. (Auto Pilot) speed/vertical speed - decrease
- 4u. (Auto Pilot) speed/vertical speed - increase
- 4p. N/A
- 4l. N/A

- 5d. COM1 radio decrease whole (alt: fraction)
- 5u. COM1 radio increase whole (alt: fraction)
- 5p. switch between whole and fraction
- 5l. swap COM1 frequency

- 6d. NAV1 radio decrease whole (alt: fraction)
- 6u. NAV1 radio increase whole (alt: fraction)
- 6p. switch between whole and fraction
- 6l. swap NAV1 frequency

- 7d. (MobiFlight) PFD Upper Menu selection decrease/data decrease
- 7u. (MobiFlight) PFD Upper Menu selection increase/data increase
- 7p. alternate
- 7l. (MobiFlight) PFD Upper Menu selection data push

- 8d. (MobiFlight) PFD/MFD range decrease
- 8u. (MobiFlight) PFD/MFD range increase
- 8p. N/A
- 8l. N/A

### buttons (starting with first row, from `1` to `8`, 2nd row starts with `9` to `16`)
1. toggle Flight Director
2. (MobiFlight, Auto Pilot) Heading (HDG)
3. (Auto Pilot) Altitude (ALT)
4. (MobiFlight, Auto Pilot) Vertical Speed (VS)
5. (MobiFlight, Auto Pilot) Approach (APPR) 
6. (MobiFlight) PFD Format (FRMT)
7. (MobiFlight) PFD Terrain/WX (TRN/WX)
8. decrease Flaps level
9. (Auto Pilot) toggle Auto Pilot (AP)
10. (MobiFlight, Auto Pilot) (lateral) Navigation (NAV)
11. (MobiFlight, Auto Pilot) Vertical Navigation (VNAV)
12. (MobiFlight, Auto Pilot) Flight Level Change (FLC)
13. toggle Yaw Damper (YD)
14. toggle Master Battery
15. toggle Gear
16. increase Flaps level

### faders
1. spoilers

## Known issues

1. no LED feedback on LNAV and VNAV buttons
