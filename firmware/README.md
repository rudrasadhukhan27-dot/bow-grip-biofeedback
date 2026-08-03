# Firmware

| Sketch | Purpose |
|---|---|
| `logger_firmware.ino` | Main firmware. Streams CSV at 115200 baud; `R`/`F` switches record/feedback. |
| `sensor_check.ino` | Bench test. Verifies FSR, EMG, IMU, and motor; flags common FSR fault signatures. |

## Before collecting data

Run `sensor_check.ino` and confirm:

- **FSR** — steady baseline when untouched, smooth rise when pressed. Values jumping between 0 and 4095 indicate a loose connection or a missing divider resistor, not real force.
- **EMG** — mid-range value that moves when you clench. A flat trace usually means electrode contact, not wiring.
- **IMU** — roughly 1 g total acceleration at rest; gyroscope responds to rotation.
- **Motor** — audible and palpable buzz. Watch for a board brownout when it starts; if the sketch restarts, the motor's current draw is sagging the supply rail.

## Setting the feedback threshold

`GRIP_THRESH` and `ZONE2_START` in `logger_firmware.ino` must come from the wearer's own baseline. Collect the baseline phase with the motor off, pool the grip samples, and take the 85th and 95th percentiles. A guessed threshold either fires constantly or never.

## Requirements

- ESP32 Arduino core **3.x** — the sketches use `ledcAttach(pin, freq, res)` and pin-addressed `ledcWrite`, which replaced `ledcSetup`/`ledcAttachPin`
- [MPU6050_tockn](https://github.com/tockn/MPU6050_tockn)
