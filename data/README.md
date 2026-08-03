# Session data

33 playing sessions from a single participant. 23 in this directory were used for phase comparisons; 10 in [`excluded/`](excluded/) were discarded for documented reasons but are published because they still represent real practice exposure and are used in the trend analysis.

## Files

| Pattern | Phase | Feedback | n |
|---|---|---|---|
| `S1_A1_s01–05.csv` | A1 baseline | off | 5 |
| `S1_B1_s01–05.csv` | B1 intervention | on | 5 |
| `S1_A2_s01–05.csv` | A2 withdrawal | off | 5 |
| `S1_B2_s01–05.csv` | B2 re-intervention | on | 5 |
| `S1_TR_s01–03.csv` | Transfer, untrained repertoire | off | 3 |

Transfer sessions used a different piece each: s01 Albinoni *Allegro assai* (bars 1–20, played slower than the other two), s02 Mel Bonis *Allegretto non troppo* (bars 1–20), s03 Florence Price *Elfentanz* (bars 1–38).

### Excluded

| Pattern | Reason |
|---|---|
| `excluded/S1_A2_attempt1_noEMG_s01–05.csv` | EMG electrodes were not applied. Grip data valid; EMG channel meaningless. |
| `excluded/S1_A2_attempt2_differentbow_s01–05.csv` | A different bow altered thumb contact geometry enough to shift the grip distribution. |

Both are retained in the practice-exposure trend analysis. Neither is used for phase comparisons. See [`../docs/DEVIATIONS.md`](../docs/DEVIATIONS.md).

## Columns

| Column | Meaning |
|---|---|
| `wallclock_iso` | **Cleared.** Host timestamps removed before publication; column retained so field positions match the analysis code. |
| `t_ms` | Device millisecond timestamp — use this for all timing |
| `fsr1` | Thumb force, raw ADC 0–4095 |
| `fsr2` | Second FSR channel — not a signal, see below |
| `emg` | BioAmp EXG Pill output, raw ADC 0–4095, DC-centred |
| `ax, ay, az` | Accelerometer, g |
| `gx, gy, gz` | Gyroscope, deg/s |
| `mode` | `R` motor off, `F` feedback active |

## Before you analyse

- **Use `t_ms`, not row index.** Effective sample rate varies: roughly 21–50 Hz for A1 and B1, a stable 100 Hz from A2 onward after a serial baud fix. Recover it per file.
- **Segment the bowing period first.** Each file begins with MVC clenches, a rest baseline, and maximum grip presses — deliberate maximal squeezes that will inflate any whole-file statistic. The published analysis isolates bowing via gyroscope magnitude (2 s rolling mean above 25 °/s, longest contiguous block). See [`../analysis/predict.py`](../analysis/predict.py).
- **`fsr2` is not a signal.** The second sensor sat on the middle finger, which applies negligible force in a violin bow hold. It was removed early on. Grip means thumb contact force.
- **Grip is floor-censored.** Very light contact and no contact both read 0. This affects median and mean grip in later sessions; it does not affect the overgrip metric, which counts samples above 1301.
- **EMG is an amplitude measure**, not a spectral one — the sample rate is far too low for median-frequency fatigue analysis.
- **EMG is not comparable across the electrode re-application** between B1 and A2. Absolute levels shift roughly threefold at that boundary.

## Overgrip threshold

1301 raw ADC — the 85th percentile of the pooled A1 baseline grip distribution (n = 70,025). Derived once from baseline and held fixed for every later phase, as pre-registered.
