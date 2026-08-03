# Build Guide — Adding the Research Sensors to Your Device

This adds the **EMG (BioAmp EXG Pill)**, **IMU (MPU-6050)**, and optional **pulse sensor (MAX30100)** to your existing bow-grip device, without disturbing the FSR + motor circuit that already works.

**Golden rule for this build:** don't rewire what already works. Your FSRs and motor stay exactly as they are. You are *adding* three sensors, not rebuilding.

---

## Read this before touching anything

Three constraints that shape every step below:

1. **Fix the power blocker first.** Your known issue (ESP32 dropping out when seated in the perfboard) must be solved *before* you add sensors. Adding three more things to the 3.3V rail will only make a marginal power path worse, and you'll waste hours chasing "the new sensor broke it" when really the rail was already weak. Get the bare device booting reliably on battery first.

2. **All analog inputs must be on ADC1 pins.** The ESP32's ADC2 pins stop working for analog reads when WiFi/Bluetooth is active — and you stream over Bluetooth. So FSR1, FSR2, **and** the new EMG signal must all sit on **ADC1** pins: GPIO 32, 33, 34, 35, 36, or 39. Before you start, confirm your two FSRs are already on ADC1 pins. If either FSR is on an ADC2 pin (0, 2, 4, 12–15, 25–27), move it now, or its readings will be garbage once Bluetooth is on.

3. **Power everything from the 3.3V rail, not 5V.** Your device runs LiPo → TP4056 → 3.3V; there is no 5V rail on battery. This actually makes the EMG wiring *safer* (see Step 2).

---

## The pin map

**Keep as-is (already on your board):**
- FSR1 → existing ADC1 pin
- FSR2 → existing ADC1 pin
- Vibration motor → existing pin via your MOSFET driver
- 3.3V rail and GND → as wired

**Add (new):**
| New part | Pin on ESP32 | Notes |
|----------|-------------|-------|
| BioAmp **OUT** (EMG signal) | a free **ADC1** pin (e.g. GPIO32 or 33) | analog input |
| BioAmp **VCC** | **3.3V** | NOT 5V — see Step 2 |
| BioAmp **GND** | GND | |
| MPU-6050 **SDA** | **GPIO21** | I²C data |
| MPU-6050 **SCL** | **GPIO22** | I²C clock |
| MPU-6050 **VCC** | 3.3V | |
| MPU-6050 **GND** | GND | |
| MAX30100 SDA/SCL (optional) | GPIO21 / GPIO22 | shares the I²C bus |
| MAX30100 VIN / GND (optional) | 3.3V / GND | |

GPIO21/22 are the ESP32's default I²C pins — confirmed standard across ESP32 references.

---

## Step 0 — Confirm the baseline

Power the existing device on battery. Verify: it boots and stays on, both FSRs read sensible values, and the motor buzzes. If anything here is flaky, stop and fix it before adding sensors. You want a known-good starting point so any new problem is clearly caused by the new part.

---

## Step 1 — Add the IMU (MPU-6050) on the bow

This is the easiest sensor, so do it first to get the I²C bus working.

1. Mount the MPU-6050 on the **bow** (near the frog, with the FSRs) — it must be on the bow because it senses *bow motion*, which is your anticipation signal.
2. Wire it: **VCC → 3.3V, GND → GND, SDA → GPIO21, SCL → GPIO22.** The GY-521 module has an onboard regulator and pull-up resistors, so 3.3V power is the safe, standard choice.
3. These four lines now have to travel from the bow to the wrist unit. VCC and GND can share the existing 4-pin bow connector (the FSRs already carry power/ground across it). SDA and SCL go through your **new 2-pin connector**.
4. **Test before continuing.** Upload an I²C scanner sketch. The MPU-6050 should appear at address **0x68**. If it doesn't show up, check SDA/SCL aren't swapped, and if still nothing, add 10kΩ pull-up resistors from SDA→3.3V and SCL→3.3V (most GY-521 boards already have these, but a long bow cable can need them).

Do not move on until the scanner sees 0x68.

---

## Step 2 — Add the EMG (BioAmp EXG Pill) — the careful one

**Why this step needs care:** the ESP32's ADC can only safely accept up to **3.3V** on an input pin. The BioAmp's OUT signal is centered at half its supply voltage and swings around it. If you powered the BioAmp at **5V**, its output could swing well above 3.3V and **stress or damage your ESP32's ADC pin**. The official Upside Down Labs ESP32 example handles this by powering at 5V *and* adding a 2.2kΩ + 1kΩ voltage divider on the OUT line to scale it down.

**Your simpler, safe path:** because your device only has a 3.3V rail, **power the BioAmp from 3.3V**. At a 3.3V supply, the output physically cannot exceed 3.3V, so it's safe to wire OUT directly to the ESP32 ADC with **no divider needed**. This is both safe and fewer parts — it works out neatly for your battery design.

Wiring:
1. **Double-check VCC and GND orientation before powering.** The datasheet has a hard warning: if the power pins are swapped, the board is destroyed permanently. Verify against the silkscreen.
2. BioAmp **VCC → 3.3V**, **GND → GND**.
3. BioAmp **OUT → a free ADC1 pin** (e.g. GPIO32).
4. Plug the included **BioAmp cable** into the board's JST socket, and snap **3 gel electrodes** onto the cable.
5. Electrode placement (from the datasheet, for EMG): the two signal electrodes (IN+ / IN−) go **along the forearm extensor muscle belly**, and the reference (REF) goes on a **bony spot** like the elbow or wrist bone.
6. Optional but worth it: wipe the skin clean (or use prep gel) before sticking electrodes — cleaner signal.

**Note on board version:** if your specific board is the **2025 edition**, it's natively 3.3V-compatible and this is all standard. If it's an **older (pre-2025) version**, powering at 3.3V is still electrically safe; if the EMG signal comes out weak, that's a software gain/normalization fix, not a safety problem — do not "fix" it by jumping to 5V without adding the divider.

**Test:** with the device running, open the Arduino Serial Plotter (or Upside Down Labs' Chords Web) and watch the EMG channel while you clench your forearm. You should see the trace jump with muscle activation. If it works, this sensor is done.

---

## Step 3 — (Optional) Add the pulse sensor (MAX30100)

Be warned: **this is the sensor most likely to fight you.** The common red/purple MAX30100 breakout boards are known to be finicky on the ESP32's 3.3V I²C bus (their onboard pull-ups are referenced to 1.8V), and there are documented cases of the MAX30100 returning zeros while an MPU-6050 on the *same* bus works fine. Treat it as a nice-to-have, not a blocker.

1. Wire it onto the **same I²C bus**: SDA → GPIO21, SCL → GPIO22, VIN → 3.3V, GND → GND. It lives on the **wrist unit** (it reads your pulse at the wrist), so no bow connector needed.
2. Run the I²C scanner again. The MAX30100 should appear at **0x57** (alongside the MPU-6050 at 0x68 — different addresses, so they coexist).
3. If it returns 0x57 but gives zero data, that's the known pull-up issue. Options: try a dedicated MAX30100 library's known ESP32 workaround, modify the board's pull-ups, or simply **drop this sensor** — your core project (EMG + IMU + FSR) does not depend on it.

Don't let this sensor delay the rest of the build. If it misbehaves for more than an hour, set it aside.

---

## Step 4 — The bow connector

Your bow now carries six lines to the wrist: power, ground, FSR1, FSR2 (existing 4-pin), plus SDA and SCL for the IMU (new 2-pin). Confirm the 2-pin connector is seated and that you didn't mix pitches within one connector (housing and pins must match). The IMU's power/ground tap off the existing 4-pin lines on the bow side, so the 2-pin only carries the two I²C signals.

---

## Step 5 — Firmware changes

Your firmware grows from "read 2 analog + drive motor" to "read 3 analog + read IMU + stream + switch modes." Concretely:

1. **Read three analog channels** now: FSR1, FSR2, and EMG (the new ADC1 pin).
2. **Read the IMU** over I²C — initialize `Wire.begin(21, 22)`, talk to address 0x68. Use a library like `Adafruit_MPU6050` or `MPU6050` to pull the 6 values (accel x/y/z, gyro x/y/z).
3. **(Optional) read the MAX30100** via a MAX30100 library if you kept it.
4. **Timestamp every sample** with `millis()` and **stream the whole row over Bluetooth** (BluetoothSerial) to your laptop, which logs CSV. One timestamp per row is what keeps grip and motion aligned — that shared clock *is* your sensor sync.
5. **Add a mode switch:** RECORD (motor off, logging on — for data collection) vs FEEDBACK (motor on, feedback curve runs — for the intervention phase).
6. **Fix the motor curve bug** before you ever use FEEDBACK mode. Your `exponentialMap()` currently collapses to a constant output of 60 because every gradient term is multiplied by `(60 − MIN_MOTOR)`, and `MIN_MOTOR` is 60, so that's × 0. The motor never ramps and never reaches MAX_MOTOR. Decide your real zone ceilings and replace those `60` literals before relying on feedback.

**Keep EMG and motor apart in time.** The vibration motor is electrically noisy; recording microvolt-level EMG while the motor buzzes on the same rail will pollute the signal. This is fine in practice because your data-collection phase runs motor-OFF anyway — just be aware of it during the feedback phase.

---

## Step 6 — Validation checklist (do these in order)

- [ ] Bare device boots and stays powered on battery (power blocker resolved)
- [ ] Both FSRs confirmed on ADC1 pins
- [ ] I²C scanner sees MPU-6050 at 0x68
- [ ] EMG trace responds to forearm clench in the Serial Plotter
- [ ] (Optional) MAX30100 at 0x57 returning real data — or consciously dropped
- [ ] Bluetooth stream logs a clean CSV row: timestamp, FSR1, FSR2, EMG, 6× IMU
- [ ] Motor curve bug fixed before enabling FEEDBACK mode

---

## Cross-reference notes (what changed vs. earlier plans, and why)

- **FSR + motor pins:** I did not re-specify your exact existing FSR/motor GPIO numbers, because the safe move is to leave the working circuit untouched — verify only that the FSRs sit on ADC1 pins.
- **BioAmp power:** earlier we said "power everything off 3.3V" — validated and correct, and it turns out to be the *safety-critical* choice here (it's what lets you skip the voltage divider the official 5V wiring would otherwise require).
- **IMU on the bow:** unchanged and essential — it's the bow-motion/anticipation signal for the prediction (B) work.
- **MAX30100:** confirmed as the weakest link of the three; kept optional, exactly as we'd flagged.
- **2-pin connector:** still only needed because the IMU is on the bow.

*Validated against: the BioAmp EXG Pill datasheet, the Upside Down Labs / Crowd Supply ESP32 integration guide, and standard ESP32 MPU-6050 / MAX30100 references.*
