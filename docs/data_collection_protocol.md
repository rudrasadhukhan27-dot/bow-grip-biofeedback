# Data Collection Protocol — Bow-Grip Study (1 + B)

This is the complete, do-it-in-order guide from "device built" to "data ready to analyze." It covers what to collect, how, the exact session steps, the study sequence, and the mistakes that silently ruin a dataset. Everything you need is here, including the logging firmware and laptop logger (the two pieces not yet built).

---

## 0. What you are collecting and why (read once)

**The recorded signal (continuous, every session):** force from both FSRs, EMG from the forearm, and motion from the IMU — all timestamped at 100 Hz. From this one stream you get *both* halves of the project:
- **B (prediction):** can overgrip be forecast ~200–300 ms before it happens, from grip + motion? (analyzed offline later)
- **Option 1 (causation):** does feedback produce a *lasting* drop in overgrip? (proven by the A-B-A-B sequence)

**The single most important rule:** during RECORD sessions the motor is OFF. You collect clean data motor-off; the motor only runs in the FEEDBACK phases. EMG is microvolt-level and the motor pollutes it, so never record clean data with it buzzing.

---

## 1. One-time prerequisites (do all of these before session 1)

### 1.1 Hardware verified
All three sensor types respond (already done): FSR1 (D35), FSR2 (D34), EMG (D32), IMU (0x68 on D21/D22). Motor on D25 buzzes.

### 1.2 Flash the logging firmware
This replaces the test sketch. It samples at 100 Hz, streams CSV over USB serial, and has a RECORD/FEEDBACK mode (motor off vs on). The motor curve bug is fixed here. **Full code in Appendix A.**

### 1.3 Set up the laptop logger
A short Python script reads the serial stream and writes a timestamped CSV file per session. **Full code in Appendix B.** Test it: run it, confirm a CSV fills with rows, open it, check all 10 columns have sensible numbers.

### 1.4 Calibrate the FSRs to real force units (do once)
ADC counts aren't publishable; convert them to grams-force. **Procedure in Appendix C.** Save the calibration curve — you apply it later in analysis, not on the device.

### 1.5 Lock your pre-registration (write it BEFORE collecting)
Decide and write down, and do not change once data starts:
- **Hypothesis** (e.g., "feedback reduces overgrip rate, and the reduction persists when feedback is removed").
- **Primary outcome metric** — pick ONE now. Recommended: **overgrip rate = % of playing time grip exceeds your personal overgrip threshold.** (Alternatives: overgrip events per minute; % of bow changes that are overgrip events.)
- **Overgrip threshold definition** — e.g., grip force above the 85th percentile of your own relaxed-baseline playing, in calibrated grams. Define the rule, not the number (the number comes from baseline data).
- **Phase structure and session counts** (Section 4).
- **Repertoire, tempo, dynamics** held constant (Section 1.6).

### 1.6 Fix the experimental conditions (these stay identical every session)
Variability here masks the effect you're hunting, so nail them down:
- **Repertoire:** the same one or two etudes/scales every session. Pick material with frequent bow changes (where overgrip lives).
- **Tempo:** fixed BPM with a metronome. Same every session.
- **Dynamics:** same dynamic level (e.g., mezzo-forte) throughout. This is critical — it removes the "loud notes legitimately need force" confound, so a force spike means overgrip, not music.
- **Time of day:** same window each day (fatigue and warmth vary across the day).
- **Warm-up:** a fixed, identical warm-up before every recording.
- **Electrode placement template:** mark the electrode spots (photo + measure from a bony landmark) so EMG placement is repeatable. Placement drift changes EMG amplitude between sessions.

### 1.7 Consent/ethics (if anyone other than you participates)
Written informed consent; parental consent for under-18s. Check your school's human-subjects process — required before collecting from others and for competitions like ISEF.

---

## 2. The data you collect (exact contents)

### 2.1 Continuous stream (logged automatically, 100 Hz)
Each CSV row: `wallclock_iso, t_ms, fsr1, fsr2, emg, ax, ay, az, gx, gy, gz, mode`
- `t_ms` device timestamp (keeps all channels aligned — this is your sync).
- `fsr1, fsr2` raw 0–4095 (convert to grams later via calibration).
- `emg` raw 0–4095.
- `ax,ay,az` accel (g), `gx,gy,gz` gyro (deg/s) — bow motion.
- `mode` R or F.

### 2.2 Per-session metadata (write in the session log, Appendix D)
Subject ID, date, **time of day**, **phase** (A1/B1/A2/B2/Transfer), **condition** (motor OFF or ON), repertoire, tempo (BPM), dynamic level, warm-up done (y/n), electrode placement OK (y/n), battery charged (y/n), any anomalies (slips, interruptions, motor accidentally on, etc.), file name.

### 2.3 Per-session calibration recordings (short, every session)
- **MVC (max voluntary contraction):** 3 × 5-second maximum forearm clenches at the start. Used to normalize EMG so it's comparable across sessions (electrode placement varies day to day — without this, EMG amplitudes aren't comparable). Log the file/time markers.
- **Rest baseline:** 30 s of quiet (instrument held, not playing) to capture resting grip/EMG.

### 2.4 Optional secondary outcomes (recommended, low effort)
- **Grip endurance / strength:** squeeze the digital dynamometer (peak-hold) before and after the session; the drop is a fatigue biomarker. (You can drop this once you've validated EMG-based fatigue against it — see Section 6.)
- **Subjective:** Borg CR-10 perceived exertion and a 0–10 forearm discomfort rating, immediately post-session.

---

## 3. Single-session procedure (run this exact sequence every time)

1. **Setup (5 min):** charge confirmed, device on, electrodes placed per template (clean skin first), glove/FSRs on, IMU seated on hand. Start the logger on the laptop with a new filename (Section 7 naming).
2. **Confirm signals (1 min):** wiggle bow → IMU moves; clench → EMG moves; press fingers → FSRs move. Abort and fix if any channel is dead.
3. **MVC recording (1 min):** mode = RECORD. Record 3 × 5 s maximum clenches, ~10 s rest between. Note the times.
4. **Rest baseline (1 min):** hold instrument quietly, 30 s, no playing.
5. **Pre-session measures:** dynamometer max (×3, record peak); note nothing hurts.
6. **Fixed warm-up:** identical every session.
7. **The recording (the data):** mode per the phase (RECORD = motor off for A-phases; FEEDBACK = motor on for B-phases). Play the fixed repertoire at the fixed tempo and dynamic for a fixed duration (e.g., 8–12 min). Keep the logger running the whole time.
8. **Post-session measures:** dynamometer max (×3), Borg CR-10, discomfort rating.
9. **Stop & save:** stop logger, confirm the CSV saved and has rows, back it up immediately (Section 7).
10. **Fill the session log** (Appendix D) completely before you forget.

Keep every session the same length and structure. Your statistical power comes from many comparable sessions, not from any one long one.

---

## 4. The study sequence (the A-B-A-B reversal)

Run phases in order. **Each phase = 5–8 sessions** (minimum 3; 5+ is much safer). Same repertoire/tempo/dynamics throughout all phases.

| Phase | Mode | Motor | Purpose |
|-------|------|-------|---------|
| **A1 baseline** | RECORD | OFF | your natural overgrip rate |
| **B1 intervention** | FEEDBACK | ON | does overgrip drop while feedback is on? |
| **A2 withdrawal** | RECORD | OFF | **the key phase** — does the drop persist with feedback gone? |
| **B2 re-intervention** | FEEDBACK | ON | does the effect return, confirming feedback caused it? |
| **Transfer test** | RECORD | OFF | play *untrained* repertoire — did the improvement carry over? |

**The logic:** a drop in B1 alone proves nothing. A drop that **persists into A2** = learning. A pattern that tracks feedback on/off/on/off across all phases = causal evidence from one subject. The transfer test at the end (music the device never trained on) is what shows the skill actually changed, not just task-specific correction.

**If you have 1–2 other violinists:** run the same sequence on each (they can do fewer sessions). Your own deep run is the spine; they are replication. A busy participant who can only do 1–2 sessions is a "generalization probe," not a full subject — use their data descriptively, don't force it into the reversal.

---

## 5. The prediction (B) data — what to ensure during collection

B is analyzed offline from the same recordings, so you don't do anything special on the device. But make sure the **A1 baseline (motor-off) sessions contain plenty of natural overgrip events** — that's the raw material for training the predictor. Practically: the baseline material should provoke overgrip (frequent bow changes, your normal playing). You need many events across several baseline sessions for the offline model to learn from. Nothing to configure — just don't skimp on baseline sessions.

---

## 6. Validate EMG-based fatigue early (do this in the first 2–3 sessions)

Record both the dynamometer drop and the EMG. Later you'll check offline whether the EMG fatigue signal (its frequency content shifting down over a session) tracks the grip-strength drop. Once they agree, you can rely on EMG alone and stop the per-session dynamometer step. Do this validation early so you're not stuck doing manual grip tests forever.

---

## 7. Data management (do this rigorously — lost/mislabeled data is unrecoverable)

- **File naming:** `S1_A1_s03_2026-07-14.csv` = subject S1, phase A1, session 03, date. Be consistent.
- **One folder per subject;** a master spreadsheet (the session log) with one row per session.
- **Back up after every session** — copy the CSV to a second location (cloud + drive). A corrupted laptop mid-study with no backups ends the project.
- **Never edit raw CSVs.** Do all cleaning in analysis scripts on copies.
- Keep the **MVC and rest-baseline timestamps** in the log so you can find them in each file.

---

## 8. Quality control & pitfalls (the things that quietly ruin datasets)

**Every session, check:**
- Motor is OFF during RECORD phases (verify — a stray buzz pollutes EMG).
- All channels live before recording (no dead/railed sensor).
- Electrodes on the marked spots; skin cleaned.
- Battery charged (brownouts corrupt data).
- Logger actually wrote rows (open the file).

**Confounds to control (these mimic or hide the effect):**
- **Practice effect:** you improve just from repetition. The A-B-A-B reversal is your defense — only feedback-linked changes (appearing/disappearing with the motor) count as the effect.
- **Fatigue / time of day:** same time window, fixed session length.
- **Dynamics drift:** hold the dynamic level constant, or loud passages get mislabeled as overgrip.
- **Electrode drift:** same placement every time (template + MVC normalization).
- **Placebo/expectation:** be aware you know when feedback is on; report it as a limitation.

**Do NOT:**
- Change the threshold, repertoire, tempo, or electrode position mid-study.
- "Clean up" raw files by hand.
- Decide your outcome metric *after* seeing the data (that's fishing — lock it in pre-registration).
- Skip the withdrawal phase (A2) — it's the phase that proves learning.

---

## 9. What you'll have at the end

Per session: a 100 Hz CSV (force, EMG, motion), MVC + rest baselines, pre/post measures, and a complete metadata row. Across the A-B-A-B sequence plus transfer test, that's enough to (a) build and validate the offline overgrip predictor [B], and (b) test whether feedback produced a lasting, causal reduction in overgrip [Option 1]. Analysis (feature extraction, leave-one-session-out validation, single-case statistics like Tau-U, calibration to grams, EMG fatigue) happens offline on these files.

---

# Appendix A — Logging firmware (flash this)

Samples 100 Hz, streams CSV over USB serial, RECORD/FEEDBACK mode via serial command (`R` = record/motor-off, `F` = feedback/motor-on). Motor curve fixed (real two-zone ramp). Set baud to 230400 in your logger to match. Keep the board still at power-up (gyro calibration).

```cpp
#include <Wire.h>
#include <MPU6050_tockn.h>

const int FSR1_PIN=35, FSR2_PIN=34, EMG_PIN=32, SDA_PIN=21, SCL_PIN=22, MOTOR_PIN=25;
const int MOTOR_CH=0, MOTOR_FREQ=20000, MOTOR_RES=8;
MPU6050 mpu(Wire);
bool imuOK=false;
char mode='R';

// ---- feedback curve (set GRIP_THRESH/ZONE2_START from your calibration & baseline) ----
const int GRIP_THRESH=1600, ZONE2_START=2800;
const int MIN_MOTOR=60, ZONE1_MAX=110, MAX_MOTOR=220;
int gripToMotor(int g){
  if(g<=GRIP_THRESH) return 0;
  if(g<=ZONE2_START){ float t=(float)(g-GRIP_THRESH)/(ZONE2_START-GRIP_THRESH);
    return (int)(MIN_MOTOR + t*(ZONE1_MAX-MIN_MOTOR)); }
  float t=(float)(g-ZONE2_START)/(4095-ZONE2_START);
  int d=(int)(ZONE1_MAX + t*(MAX_MOTOR-ZONE1_MAX));
  return d>MAX_MOTOR?MAX_MOTOR:d;
}

unsigned long lastSample=0;
const unsigned long SAMPLE_US=10000;  // 100 Hz

void setup(){
  Serial.begin(230400);
  analogReadResolution(12);
  analogSetPinAttenuation(FSR1_PIN,ADC_11db);
  analogSetPinAttenuation(FSR2_PIN,ADC_11db);
  analogSetPinAttenuation(EMG_PIN,ADC_11db);
  ledcSetup(MOTOR_CH,MOTOR_FREQ,MOTOR_RES);
  ledcAttachPin(MOTOR_PIN,MOTOR_CH);
  ledcWrite(MOTOR_CH,0);
  Wire.begin(SDA_PIN,SCL_PIN);
  bool seen=false;
  for(byte a=1;a<127;a++){ Wire.beginTransmission(a); if(Wire.endTransmission()==0 && a==0x68) seen=true; }
  if(seen){ mpu.begin(); mpu.calcGyroOffsets(false); imuOK=true; }
  Serial.println("# t_ms,fsr1,fsr2,emg,ax,ay,az,gx,gy,gz,mode");
}

void loop(){
  if(Serial.available()){
    char c=Serial.read();
    if(c=='R'||c=='r'){ mode='R'; ledcWrite(MOTOR_CH,0); }
    if(c=='F'||c=='f'){ mode='F'; }
  }
  unsigned long now=micros();
  if(now-lastSample>=SAMPLE_US){
    lastSample+=SAMPLE_US;
    int f1=analogRead(FSR1_PIN), f2=analogRead(FSR2_PIN), e=analogRead(EMG_PIN);
    float ax=0,ay=0,az=0,gx=0,gy=0,gz=0;
    if(imuOK){ mpu.update();
      ax=mpu.getAccX(); ay=mpu.getAccY(); az=mpu.getAccZ();
      gx=mpu.getGyroX(); gy=mpu.getGyroY(); gz=mpu.getGyroZ(); }
    int grip = (f1>f2)?f1:f2;
    if(mode=='F') ledcWrite(MOTOR_CH, gripToMotor(grip)); else ledcWrite(MOTOR_CH,0);
    Serial.print(millis()); Serial.print(',');
    Serial.print(f1); Serial.print(','); Serial.print(f2); Serial.print(','); Serial.print(e); Serial.print(',');
    Serial.print(ax,3); Serial.print(','); Serial.print(ay,3); Serial.print(','); Serial.print(az,3); Serial.print(',');
    Serial.print(gx,2); Serial.print(','); Serial.print(gy,2); Serial.print(','); Serial.print(gz,2); Serial.print(',');
    Serial.println(mode);
  }
}
```

To switch modes during a session, send `R` or `F` from the serial monitor / logger. Default is RECORD.

---

# Appendix B — Laptop logger (Python)

Install once: `pip install pyserial`. Find your port (Arduino IDE shows it, e.g. `/dev/cu.usbserial-0001` on Mac, `COM5` on Windows). Run: `python logger.py S1_A1_s01_2026-07-14.csv`

```python
import serial, csv, time, sys

PORT = '/dev/cu.usbserial-0001'   # <-- set your port
BAUD = 230400
fname = sys.argv[1] if len(sys.argv) > 1 else 'session.csv'

ser = serial.Serial(PORT, BAUD, timeout=1)
print('Logging to', fname, '— Ctrl+C to stop')
with open(fname, 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['wallclock_iso','t_ms','fsr1','fsr2','emg','ax','ay','az','gx','gy','gz','mode'])
    n = 0
    try:
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if not line or line.startswith('#'):
                continue
            p = line.split(',')
            if len(p) != 11:
                continue
            w.writerow([time.strftime('%Y-%m-%dT%H:%M:%S'), *p])
            n += 1
            if n % 500 == 0:
                print(n, 'samples')
    except KeyboardInterrupt:
        print('Stopped.', n, 'samples saved to', fname)
```

To send `R`/`F` mode commands, you can use the Arduino Serial Monitor (close the logger first, since only one program can hold the port) — or send from a second tiny script. Simplest workflow: set the mode in the Serial Monitor, close it, then start the logger.

---

# Appendix C — FSR force calibration (do once)

Goal: map raw ADC → grams-force so your data is in real units.

1. Mount the FSR as it'll be used (on the glove fingertip pad).
2. Press it against a **digital kitchen/jewelry scale** through a small rigid flat cap (so force transfers evenly to the sensor).
3. At several force levels spanning light→hard (e.g., 50, 100, 200, 400, 700, 1000+ g), hold steady and record BOTH the scale reading (grams) and the firmware's ADC value for that FSR.
4. Take 6–8 points. Repeat for FSR1 and FSR2 separately (they differ).
5. In Python, fit a curve (ADC→grams) per sensor — a smooth monotonic fit (polynomial or piecewise/interpolation). Save the curves.
6. Apply these in analysis to convert all logged ADC to grams. Don't put this on the device; keep raw ADC in the CSV and convert offline (reversible, documented).

Note: FSRs are approximate (±10–20%) and drift; recalibrate occasionally and report this as a limitation.

---

# Appendix D — Session log sheet (one row per session)

| Field | Example |
|-------|---------|
| Subject ID | S1 |
| Date | 2026-07-14 |
| Time of day | 16:30 |
| Phase | A1 |
| Session # | 03 |
| Condition (motor) | OFF |
| Repertoire | Etude X + scale |
| Tempo (BPM) | 92 |
| Dynamic | mf |
| Warm-up done | y |
| MVC recorded (times) | 00:20, 00:35, 00:50 |
| Rest baseline (time) | 01:10 |
| Dynamometer pre (kg) | 38 / 38 / 37 |
| Dynamometer post (kg) | 34 / 35 / 34 |
| Borg CR-10 post | 4 |
| Discomfort 0–10 | 2 |
| Electrodes on template | y |
| Battery charged | y |
| File name | S1_A1_s03_2026-07-14.csv |
| Anomalies | none |

---

*Design note: this is a within-subject (n-of-1, optionally + a couple replications) study by intent. Its rigor comes from many comparable sessions and the reversal structure, not sample size — which is exactly why one well-run subject can carry it. Lock the conditions, keep every session identical, back up everything, and don't decide the outcome metric after seeing the data.*
