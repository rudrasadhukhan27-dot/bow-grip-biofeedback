# Results

Single-subject (n = 1) study of a haptic bow-grip biofeedback wearable. Pre-registered A-B-A-B reversal design with a transfer test. All analyses follow the pre-registration in `docs/pre_registration.md` except where explicitly noted.

---

## 1. Data collected

| Phase | Feedback | Sessions | Status |
|---|---|---|---|
| A1 baseline | off | 5 | analysed |
| B1 intervention | on | 5 | analysed |
| A2 withdrawal (attempt 1) | off | 5 | excluded — EMG electrodes omitted; grip data retained for trend analysis |
| A2 withdrawal (attempt 2) | off | 5 | excluded — different bow altered thumb contact geometry |
| A2 withdrawal (attempt 3) | off | 5 | analysed |
| B2 re-intervention | on | 5 | analysed |
| Transfer | off | 3 | analysed |

33 playing sessions in total; 23 used for phase comparisons. All 33 are treated as practice exposure in the trend analysis, since the participant was playing in every one.

**Sessions were not spaced across days.** Each phase was recorded within a single afternoon, sessions 13–21 minutes apart: A1 on 08 Jul, B1 on 09 Jul, A2 on 23 Jul, B2 on 25 Jul, transfer on 28 Jul. There are therefore **5 testing days, and phase is perfectly confounded with day**. This has direct consequences for the statistics below and is detailed in [`docs/DEVIATIONS.md`](docs/DEVIATIONS.md).

Data quality after the baud-rate correction (session 11 onward) was 0.00% row rejection at a sustained 100 Hz. Earlier sessions ran at 21–50 Hz effective rate with intermittent serial corruption; the strict-validation logger discards affected rows.

---

## 2. Primary outcome

**Definition (pre-registered):** percentage of playing time during which grip force exceeds the participant's personal overgrip threshold.

**Threshold:** 1301 raw ADC units — the 85th percentile of the pooled A1 baseline grip distribution (n = 70,025 samples). Per-session A1 85th percentiles were tightly clustered (1171–1424), indicating a stable baseline. Fixed for the remainder of the study.

**Segmentation:** the bowing period is isolated from IMU gyroscope magnitude (2 s rolling mean > 25 °/s, longest contiguous block). This excludes the MVC clenches and maximum grip presses, which are deliberate maximal squeezes and would otherwise inflate the outcome. Whole-file analyses reported earlier in development were biased upward for this reason.

### Phase results

| Phase | Feedback | Mean | Median | Range |
|---|---|---|---|---|
| A1 baseline | off | **12.57%** | 8.94 | 6.02 – 23.25 |
| B1 intervention | on | **6.22%** | 4.98 | 3.71 – 9.17 |
| A2 withdrawal | off | **1.37%** | 1.55 | 0.13 – 2.82 |
| B2 re-intervention | on | **1.30%** | 1.06 | 0.70 – 2.33 |
| Transfer | off | **0.55%** | 0.47 | 0.40 – 0.80 |

Transfer sessions used three different untrained pieces, one per session, rather than one piece repeated: Albinoni *Allegro assai* (bars 1–20), Mel Bonis *Allegretto non troppo* (bars 1–20), and Florence Price *Elfentanz* (bars 1–38). Per-session overgrip was 0.40%, 0.80%, and 0.47% respectively. Session 1 was played at a slower tempo, which reduces bow-change frequency and therefore overgrip opportunity; it is the lowest of the three but not by a margin that changes the conclusion. All three fall far below every baseline session regardless.

### Effect sizes versus baseline

| Contrast | NAP | Tau | Nominal *p* |
|---|---|---|---|
| A1 vs B1 | 76.0% | +0.52 | 0.111 |
| A1 vs A2 | **100.0%** | +1.00 | 0.004 |
| A1 vs B2 | **100.0%** | +1.00 | 0.004 |
| A1 vs Transfer | **100.0%** | +1.00 | 0.018 |

Every session in A2, B2, and the transfer test falls below every baseline session. Complete non-overlap is among the strongest criteria available in single-case visual analysis, and the magnitude of separation is not in doubt.

**The *p* values above are reported for completeness but should not be relied on.** They treat five same-day recordings as independent replicates. Because every phase was collected within a single afternoon, the effective sample is **one observation per condition**, and no inferential test is appropriate. These comparisons are **descriptive**.

Partial mitigation: within-day trends are flat (log-overgrip regressed on within-day session order gives *p* = 0.61, 0.87, 0.92, 0.42, 0.20 for A1, B1, A2, B2, transfer). The same-day sessions behave as repeated measurements of a stable daily state rather than as a within-day learning curve, which is what makes the day-level means meaningful.

---

## 3. Causal analysis — null result

The reversal design was intended to attribute the improvement to the haptic feedback. It does not.

**Withdrawal produced no rebound.** Removing feedback after B1 (6.22%) was followed by a *further* decrease in A2 (1.37%), not a return toward baseline. Reinstating feedback in B2 changed nothing (1.30%; A2 vs B2 *p* = 1.000).

**The data are described by a monotonic trend in practice exposure.** Regressing log overgrip on session index across all 33 playing sessions:

- slope = −0.093 per session (≈ **8.9% relative decline per session**)
- *r* = −0.70, *p* = 5.8 × 10⁻⁶
- R² = 0.490

**Feedback status adds nothing to that model.** Including a feedback-on indicator:

- coefficient = +0.108 (wrong sign for a beneficial effect)
- *F* = 0.09, *p* = **0.765**
- R² rises from 0.490 to 0.492

**The first feedback exposure was not distinguishable from baseline** (A1 vs B1, NAP 76%, *p* = 0.111) — precisely where a causal effect should be most visible.

**A 14-day unmeasured gap contains the largest single drop.** B1 was recorded on 09 Jul and A2 on 23 Jul. Overgrip fell from 6.22% to 1.37% across that interval — a 78% relative reduction — with no data collected and ordinary practice presumably continuing. The decline also fits elapsed calendar time better than session count (*r* = −0.858, *p* = 1.7 × 10⁻⁷ versus *r* = −0.809, *p* = 3.0 × 10⁻⁶), consistent with a between-day consolidation process rather than within-session correction. Whatever occurred during those two weeks is unmeasured and is the most plausible single driver of the headline reduction.

### Interpretation

Something in this protocol produced a large, durable reduction in bow-grip overtension. The design cannot identify what. Three explanations remain equally consistent with the data:

1. **Motor practice** — 33 repetitions of the same two scales.
2. **Measurement reactivity** — knowing that grip is being recorded.
3. **Proprioceptive attention** — a sensor physically pressed against the thumb makes grip salient, feedback or not.
4. **Unmeasured activity during the 14-day gap** between B1 and A2, which brackets the largest observed change.

The haptic feedback specifically is *not* supported as the causal agent. Claims in this repository are limited accordingly.

---

## 4. Secondary outcome: EMG

EMG activation (mean absolute deviation from session median, during the bowing period) declined within each electrode-setup era:

- A1 → B1: 1525 → 404
- A2 → B2 → transfer: 170 → 97 → 124

A roughly threefold discontinuity coincides with the electrode re-application between B1 and A2, so absolute levels either side of that boundary are not comparable. The within-era declines corroborate the grip findings directionally but cannot be pooled.

Because sampling ran at 21–100 Hz, EMG here is an **amplitude/envelope** measure. Spectral fatigue analysis (median-frequency shift) requires ~1000 Hz sampling and is not possible with this dataset.

---

## 5. Prediction of overgrip onset

**Task.** At each moment during playing, predict whether an overgrip onset will occur within a target window ahead. Onsets are upward crossings of the 1301 threshold sustained ≥100 ms: **297 onsets across the five A1 baseline sessions.**

**Method.** Sessions resampled to a uniform 50 Hz grid. Candidate moments are restricted to the bowing period, currently below threshold, and outside a 0.5 s refractory window after any prior above-threshold sample. 21 features from a causal lookback window: grip level, rolling means (200/500/1000 ms), rolling standard deviations, slopes, deltas, headroom to threshold, gyroscope magnitude statistics, accelerometer variability, EMG deviation. Classifier: histogram gradient-boosted trees. Validation: **leave-one-session-out**.

### Lead-time curve

| Window | Prevalence | Average precision | Lift | ROC-AUC | Grip-level baseline |
|---|---|---|---|---|---|
| 0–200 ms | 1.22% | 0.260 | 21.4× | 0.902 | 0.143 |
| 100–300 ms | 1.25% | 0.114 | 9.2× | 0.815 | 0.056 |
| **200–400 ms** (pre-registered) | 1.26% | **0.093** | **7.4×** | **0.859** | 0.045 |
| 300–500 ms | 1.28% | 0.106 | 8.2× | 0.861 | 0.050 |
| 500–700 ms | 1.33% | 0.079 | 5.9× | 0.823 | 0.072 |
| 800–1000 ms | 1.52% | 0.072 | 4.7× | 0.796 | 0.054 |

The model consistently beats both chance and a grip-level-only baseline. Performance falls sharply past 200 ms and then plateaus — most of the predictable signal lies in the final fifth of a second before onset.

### Event-level performance

Constraining to ≤2 false alarms per minute, per-fold recall of onset events was 3.1%, 0%, 100%, 0%, 2.6%. The mean of 21.2% is carried entirely by one fold containing only six events; the median is ~3%. **A practical warning system is not achievable at this performance level.**

### Feature importance

Permutation importance is dominated by grip-derived features: 1 s rolling maximum, 500 ms and 200 ms standard deviations, rolling means. **IMU bow-motion features contribute negligibly.**

This reframes the result. The model is not anticipating overgrip from independent bow kinematics; it is recognising a squeeze that has already begun to develop. The honest description is *early detection*, not *prediction*.

---

## 6. Sensor validity check

The proportion of samples reading exactly zero rose across the study (≈6% early, 57% in the final transfer session), and median grip fell from ~900 to 0. Two explanations were possible: genuine relaxation below the FSR's activation floor, or progressive contact degradation.

Two checks were run:

1. **Maximum grip-press peaks** at the start of each session were stable throughout: A1 2824–3185, B1 2511–2839, A2 2803–3300, B2 2839–3193, transfer 2799–3202. High-force response did not drift.
2. **Comparison against a fresh FSR** at matched low forces showed the original sensor activating at *lower* force than the new unit — its low-force sensitivity had not degraded.

Sensor wear is therefore rejected as the explanation. The zeros reflect genuine light contact falling below the sensor's activation floor. The consequence is that grip data is **floor-censored** in later sessions: median and mean grip are directional only, while the overgrip metric — which counts samples above a high threshold — is unaffected.

---

## 7. Summary of claims

**Supported:**
- A low-cost wearable can continuously measure bow-grip force, forearm EMG, and bow motion during unmodified violin practice.
- Over 33 sessions, overgrip fell ~95%, persisted without feedback, and generalised to untrained repertoire, with complete non-overlap between baseline and all later phases (*p* = 0.004).
- Overgrip onset carries statistically detectable precursor signal a few hundred milliseconds ahead (ROC-AUC 0.86 at 200–400 ms), about twice a naive grip-level baseline.

**Not supported:**
- That the haptic feedback caused the improvement (*p* = 0.77 for feedback beyond trend).
- That the prediction model is deployable (≈3% median event recall at a tolerable alarm rate).
- Any generalisation beyond this individual.

---

## 8. Session spacing — a limitation affecting all phase statistics

All 33 sessions fell on **7 calendar dates**, with each phase's five sessions run consecutively within roughly 90 minutes on a single day (see `data/README.md` for the schedule).

Consequences:

- **Sessions within a phase are not independent.** NAP, Tau, and Mann-Whitney statistics above treat them as independent observations, which they are not. The effective sample size per phase is nearer 1 than 5, and the reported *p*-values should be read as descriptive rather than inferential.
- **Phase is perfectly confounded with date.** Any day-specific factor — electrode placement, ambient conditions, how the participant felt — is indistinguishable from phase.
- **Within-day fatigue is uncontrolled**, though it would work against the observed effect rather than producing it.

Re-running the trend against **elapsed calendar time** rather than session index gives *r* = −0.639, *p* = 6.2 × 10⁻⁵, R² = 0.409 — the same conclusion as the session-index model (*r* = −0.700, R² = 0.490), with time explaining slightly less variance than cumulative sessions. Both support a practice-driven decline; neither supports the feedback.

A replication should space sessions across separate days.
