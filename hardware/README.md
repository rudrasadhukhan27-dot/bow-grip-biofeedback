# Hardware

## Pin map

| Signal | ESP32 pin | Notes |
|---|---|---|
| FSR (thumb) | D35 | Voltage divider to GND; primary grip signal |
| FSR (second) | D34 | Unused in this build |
| EMG output | D32 | BioAmp EXG Pill, powered from **3.3 V** |
| IMU SDA | D21 | MPU-6050 at `0x68` |
| IMU SCL | D22 | |
| Motor gate | D25 | IRLZ44N gate via series resistor |

All analog inputs are on ADC1, which stays usable while the radio is active.

## Notes that cost time to learn

- **Power the BioAmp from 3.3 V, not 5 V.** At a 3.3 V supply its output cannot exceed the ESP32's ADC range, so no divider or level shifter is needed.
- **The motor needs a flyback diode** (1N4007) across its terminals and a logic-level MOSFET. Without the diode, switching spikes couple into everything.
- **Battery feeds VIN**, never the 3V3 pin — the 3V3 pin bypasses the regulator.
- **Many MPU-6050 modules are clones** that fail to initialise with some libraries even when an I²C scan finds them at `0x68`. `MPU6050_tockn` works; note it reports acceleration in g.
- **Sensor placement matters more than sensor count.** A second FSR on the middle finger recorded almost nothing — that finger applies negligible force in a violin bow hold. Thumb and index are the pressure points.
- **The bow is part of the calibration.** Changing to a different bow altered thumb contact geometry enough to shift the grip distribution substantially and invalidated a five-session run. Treat the instrument as a fixed experimental condition.

## Enclosure

`electronics_box_snap.stl` + `electronics_lid_snap.stl` — 86 × 56 × 29 mm snap-fit case, 26 mm internal depth, 2 mm walls, 3 mm floor. Front window with a 3 mm frame; two 18 × 10 mm side slits for cabling, one offset 15 mm toward the front.

Print the lid plate-down (lip upward) for a support-free top surface. Snap engagement is 0.8 mm with 0.3 mm lip clearance per side — reduce engagement to ~0.5 mm if the lid will not seat or if printing in brittle PLA, increase to ~1.0 mm if it is loose.
