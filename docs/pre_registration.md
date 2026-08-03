# Pre-Registration — Bow-Grip Haptic Biofeedback Study

**Locked before data collection. Not modified after session 1.**

**Date locked:** 07/07/2026
**Investigator:** Rudra Sadhukhan

> Reproduced as locked. Everything that differed in execution is recorded separately in [`DEVIATIONS.md`](DEVIATIONS.md) rather than edited into this document.

---

## 1. Background & aim

An open, low-cost wearable measures violin bow-grip force (FSR), forearm muscle activation (EMG), and hand/bow motion (IMU). This study tests, within a single participant (with optional replication), whether haptic feedback reduces bow-grip overtension in a way that lasts, and whether overtension can be predicted before it occurs.

## 2. Hypotheses

- **H1 (primary, causal):** Haptic feedback reduces the overgrip rate during playing, and the reduction persists when feedback is removed (i.e. motor learning, not just real-time correction).
- **H2 (prediction):** Bow-grip overtension events can be predicted ~200–300 ms before onset from grip + motion signals, better than a force-rising baseline. (Analyzed offline.)

## 3. Design

Single-case experimental design, A-B-A-B reversal with a final transfer test, in one primary participant (S1). Optional 1–2 additional violinists as replication/generalization probes.

| Phase | Feedback (motor) | Sessions (planned) |
|---|---|---|
| A1 baseline | OFF | 5 |
| B1 intervention | ON | 5 |
| A2 withdrawal | OFF | 5 |
| B2 re-intervention | ON | 5 |
| Transfer test | OFF | 2 |

## 4. Primary outcome measure (locked)

**Overgrip rate** = percentage of playing time during which grip force exceeds the participant's personal overgrip threshold. Computed offline from the 100 Hz recording.

## 5. Overgrip threshold rule (locked now; number derived from A1 baseline)

Grip force above the **85th percentile** of the participant's own A1 relaxed-playing grip distribution (in calibrated grams-force; raw ADC if analyzed before calibration). The rule is fixed here; the numeric threshold is computed from A1 baseline data and then held constant for all later phases.

## 6. Secondary outcomes

- EMG-derived fatigue (downward shift of EMG median frequency across a session), normalized to per-session MVC.
- Grip-strength decline (dynamometer, pre vs post session) — used to validate the EMG fatigue metric early, then optional.
- Subjective: Borg CR-10 exertion; 0–10 forearm discomfort, post-session.

## 7. Controlled conditions (identical every session)

- **Repertoire:** A minor harmonic 3 octaves, D major 3 octaves
- **Tempo:** 76 BPM
- **Dynamic level:** mf
- **Time of day:** 5 pm
- **Fixed warm-up:** basic bowing drills for 5 min
- **Electrode placement:** per marked template (photo + landmark measurement)
- **Session recording duration:** 8 min

## 8. Signal & data collected

100 Hz stream: FSR1, FSR2, EMG, accel (x,y,z), gyro (x,y,z), timestamp, mode. Plus per session: 3×5 s MVC, 30 s rest baseline, pre/post dynamometer, Borg CR-10, discomfort, full metadata log.

## 9. Analysis plan (locked)

- **H1:** single-case analysis across phases — visual analysis (level/trend/overlap) plus a quantitative index (Tau-U or randomization test). Effect judged by whether overgrip rate drops in B phases and persists into A2, tracking feedback on/off across all four phases.
- **H2:** offline predictor (gradient-boosted trees on windowed features) trained/validated with leave-one-session-out cross-validation; report precision-recall (AUC-PR) and a lead-time curve; baseline to beat = "predict when force is already rising."
- **Transfer test:** compare overgrip rate on untrained repertoire vs baseline.

## 10. Confounds controlled

Practice effect (addressed by the reversal design), fatigue/time-of-day (fixed window + fixed duration), dynamics drift (held constant), electrode-placement drift (template + MVC normalization), expectation/placebo (acknowledged as a limitation).

## 11. Scope & limitations (stated in advance)

Findings are within-individual; generalization to violinists broadly is explicitly future work. "Overgrip" is an operational definition justified by held-constant dynamics, not a clinical label. Prediction accuracy expected to be modest and reported honestly against baselines.

## 12. Ethics

Self-experimentation for S1. Any additional participants: written informed consent (parental consent if under 18), per institutional human-subjects requirements, obtained before their data collection.
