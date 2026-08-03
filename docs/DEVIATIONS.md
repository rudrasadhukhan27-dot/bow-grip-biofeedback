# Deviations from Pre-Registration

The pre-registration in [`pre_registration.md`](pre_registration.md) was locked on 07/07/2026 and has not been edited. Every difference between what was planned and what happened is recorded here.

---

## Threshold value (planned, resolved as specified)

The pre-registration fixed the *rule* — 85th percentile of the participant's own A1 baseline grip — and left the number to be derived. Pooling all five A1 sessions (n = 70,025 samples) gave **1301 raw ADC units**. Per-session A1 85th percentiles were 1215, 1284, 1424, 1171, 1339, a tight cluster indicating a stable baseline. This value was set in firmware before B1 and held constant for B1 and B2.

`ZONE2_START`, the point where the feedback ramp steepens, was set to the A1 95th percentile (1584). This parameter was not pre-specified; it affects only the shape of the haptic response, not the outcome measure.

**Units:** analysis was performed in raw ADC, which the pre-registration permits ("raw ADC if analyzed before calibration"). Force calibration to grams was not completed.

---

## Sessions per phase

Transfer test ran **3 sessions** rather than the planned 2. All other phases ran 5 as planned.

---

## Discarded and repeated runs

Three separate attempts were made at the A2 withdrawal phase. All were real playing sessions and are counted as practice exposure in the trend analysis; only the third is used for phase comparisons.

| Attempt | Sessions | Outcome |
|---|---|---|
| 1 | 5 | **Excluded.** EMG electrodes were not applied. Grip data is valid and retained for trend analysis; EMG is absent. |
| 2 | 5 | **Excluded.** A different bow was used, altering thumb contact geometry enough to shift the grip distribution substantially (elevated zero-fraction and elevated upper percentiles simultaneously). Retained for trend analysis only. |
| 3 | 5 | **Analysed.** Original bow, electrodes applied. |

Total playing sessions: **33**. Sessions used for phase comparisons: **23**.

---

## Controlled conditions — one omission discovered during the study

**The bow was not listed as a controlled condition** in section 7 of the pre-registration. It should have been. Changing bows between runs invalidated five sessions, as above. Subsequent sessions all used the original bow, and any replication should treat the instrument as a fixed experimental condition alongside repertoire, tempo, and dynamic level.

---

## Session scheduling — the most consequential deviation

The pre-registration did not specify spacing between sessions. In execution, **all sessions within a phase were recorded on a single day, 13–21 minutes apart.**

| Date | Phase | Sessions | Clock times |
|---|---|---|---|
| 08 Jul 2026 | A1 | 5 | 18:46, 19:00, 19:13, 22:51, 23:06 |
| 09 Jul 2026 | B1 | 5 | 17:31, 17:50, 18:03, 18:19, 18:34 |
| 23 Jul 2026 | A2 | 5 | 16:45, 17:06, 17:25, 17:41, 17:56 |
| 25 Jul 2026 | B2 | 5 | 17:53, 18:10, 18:31, 18:45, 19:00 |
| 28 Jul 2026 | Transfer | 3 | 17:11, 17:26, 17:44 |

(The two discarded A2 attempts were also recorded on 23 Jul, earlier in the same afternoon.)

Three consequences follow, and they are stated here rather than buried:

**1. Phase is perfectly confounded with day.** There are **5 distinct testing days, not 23 independent sessions.** No analysis can separate "which phase" from "which day."

**2. The reported inferential statistics are pseudo-replicated.** The Mann-Whitney tests in `RESULTS.md` treat five same-day recordings as independent replicates. They are not; they are consecutive recordings within one sitting. The nominal *p* values (0.004) therefore **overstate the strength of evidence**. Treated properly, the design yields one observation per condition, which cannot be tested inferentially. The phase comparisons should be read as **descriptive**, supported by complete non-overlap and effect magnitude, not as significance tests.

Partial mitigation: within-day trends are flat. Regressing log overgrip on within-day session order gives *p* > 0.2 for every day (A1 *p* = 0.61, B1 *p* = 0.87, A2 *p* = 0.92, B2 *p* = 0.42, TR *p* = 0.20). Improvement is not occurring within sittings, so the same-day sessions behave as repeated measurements of a stable daily state rather than as a within-day learning curve.

**3. A 14-day unmeasured gap sits inside the largest effect.** B1 ended 09 Jul; A2 began 23 Jul. Overgrip fell from 6.22% to 1.37% — a 78% relative reduction — across an interval in which nothing was recorded and ordinary violin practice presumably continued. This unmeasured period is the single most plausible driver of the study's headline reduction, and it further undermines any attribution to the haptic feedback.

Consistent with this, the decline fits elapsed calendar time better than session count (*r* = −0.858, *p* = 1.7 × 10⁻⁷ versus *r* = −0.809, *p* = 3.0 × 10⁻⁶ across the 23 analysed sessions), which is what a between-day consolidation process would predict and a within-session practice process would not.

**Any replication should space sessions across separate days**, one per day, with practice between sessions logged.

---

## Time of day

The pre-registration fixed session time at 17:00. A1 sessions 4 and 5 were recorded at **22:51 and 23:06**, following a 3.5-hour break after session 3. All other sessions fell between 16:45 and 19:00.

The two late sessions are the baseline phase, where fatigue or time-of-day effects would tend to *increase* measured overgrip and thus inflate the baseline against which all later phases are compared. Their values (6.02% and 16.69%) span the phase range and are not obvious outliers, but the deviation is noted.

---

## Secondary outcome substitutions

**Dynamometer replaced by FSR maximum grip press.** No hand dynamometer was available. Pre- and post-session grip strength was instead recorded as three maximum squeezes on the bow, captured by the thumb FSR. This is less precise than a dynamometer — contact geometry varies between repetitions and the sensor saturates above roughly 3300 ADC — so it is reported as an approximate fatigue index rather than a calibrated strength measure.

**Post-session grip presses were omitted in the A1 phase.** They were recorded from B1 onward. Pre/post fatigue comparison is therefore unavailable for A1.

**EMG spectral fatigue could not be computed.** The pre-registration specified median-frequency shift, which requires roughly 1000 Hz sampling. Achieved rates were 21–100 Hz, so EMG is reported as an amplitude/envelope measure only.

**Borg CR-10 and 0–10 discomfort ratings were not collected.** Section 6 of the pre-registration specified both as per-session secondary outcomes. Neither was recorded in any session, and no session log was kept. The subjective secondary outcomes are therefore entirely absent from this study.

---

## Sampling rate

The firmware targets 100 Hz. Achieved effective rates were **21–50 Hz for sessions 1–10** and a stable **100 Hz from session 11 onward**, after the serial baud rate was reduced from 230400 to 115200. The I²C IMU read is the limiting factor at the lower rates.

Grip and bow motion are low-frequency signals, so the outcome measure is not materially affected, but the rate is recovered per session from the `t_ms` column rather than assumed.

---

## Data corruption and its correction

At 230400 baud the serial stream produced intermittently malformed rows, most visibly the mode column bleeding into adjacent fields. Affected rows fail validation and are discarded by the logger.

From session 11 the baud rate was lowered to 115200 and row-level validation was tightened. Rejection rate thereafter was **0.00%** in every session.

---

## Analysis: playing-period segmentation

The pre-registered outcome is percentage of **playing** time above threshold. Early exploratory analyses computed this over whole files, which inflated the rate by including the MVC clenches and maximum grip presses — deliberate maximal squeezes performed before and after each recording.

The reported analysis segments the bowing period from IMU gyroscope magnitude (2 s rolling mean > 25 °/s, longest contiguous block) before computing the outcome. This is a refinement of the pre-registered procedure, not a change of measure; it removes contamination the pre-registration did not anticipate.

---

## Transfer test repertoire

The pre-registration specified untrained repertoire but did not name it in advance. Three different untrained pieces were used, one per session, rather than a single piece repeated:

| Session | Piece | Extent |
|---|---|---|
| TR s01 | Albinoni — *Allegro assai* | first 20 bars |
| TR s02 | Mel Bonis — *Allegretto non troppo* | first 20 bars |
| TR s03 | Florence Price — *Elfentanz* | first 38 bars |

Session 1 was played at a slower tempo than the other two. Because tempo affects bow-change frequency, and bow changes are where overgrip concentrates, transfer sessions are reported individually rather than pooled and the slower session is flagged in interpretation.

Using real repertoire rather than further scales makes this a stronger generalisation test than repeating a single untrained piece would have been, at the cost of the three sessions not being directly comparable to one another.

---

## Sensor configuration

**The second FSR was removed.** It was mounted on the middle finger, which applies negligible force in a violin bow hold, and recorded near-zero throughout A1. Grip is therefore **thumb contact force** from a single sensor. Firmware takes the stronger of the two FSR channels, so a single working sensor is functionally equivalent.

**Power source changed from battery to USB.** The lithium battery over-discharged to 0.7 V and was not replaced. All sessions ran on USB power via a tethered cable. This does not affect the signal but does constrain movement, and is noted as a practical limitation of the setup as tested.

---

## Confound status — H1 outcome

The pre-registration states that the practice effect is "addressed by the reversal design." **It was not adequately addressed.** The observed pattern was a monotonic decline across cumulative practice with no rebound on withdrawal, and feedback status contributed nothing beyond the trend (*p* = 0.77). H1 is reported as **not supported**: the study demonstrates a large durable reduction but cannot attribute it to the haptic feedback.

This is a limitation of the design as executed, and is stated as such in [`../RESULTS.md`](../RESULTS.md) rather than reframed.

---

## Session spacing — not as pre-registered in spirit

The pre-registration fixed a session time of day (5 pm) but did not specify spacing between sessions. In execution, all 33 sessions fell on **7 calendar dates**, with each phase's 5 sessions run consecutively within about 90 minutes on a single day:

| Date | Sessions | Phase |
|---|---|---|
| 2026-07-08 | 5 | A1 |
| 2026-07-09 | 5 | B1 |
| 2026-07-18 | 5 | A2 attempt 1 (excluded) |
| 2026-07-22 | 5 | A2 attempt 2 (excluded) |
| 2026-07-23 | 5 | A2 |
| 2026-07-25 | 5 | B2 |
| 2026-07-28 | 3 | Transfer |

Two consequences:

1. **Sessions within a phase are not independent observations.** Five consecutive 8-minute recordings separated by a few minutes each are closer to one long session than to five spaced ones. Effect-size statistics that treat sessions as independent (NAP, Tau, Mann-Whitney) are correspondingly optimistic, and the effective n per phase is nearer 1 than 5.

2. **Within-day fatigue is uncontrolled and works against the observed effect.** The pre-registration controlled fatigue by fixing session duration and time of day, which does not address five back-to-back sessions.

Phase is also perfectly confounded with date: every session in a phase shares a single day, so any day-specific factor — electrode placement that day, ambient temperature, how the participant felt — is indistinguishable from phase. A replication should space sessions across separate days.
