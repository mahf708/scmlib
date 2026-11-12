> **Disclaimer:** This is an AI-simulated referee report written by Claude. It is not a review by, and does not state the opinions of, any real person.

# Referee report: Reviewer C (perspective informed by the published work of F. Glassmeier)

**Manuscript:** "Horizontal resolution dependence of the liquid water path response to droplet number in doubly periodic EAMxx simulations of drizzling stratocumulus", submitted to *Atmospheric Chemistry and Physics*

**Recommendation:** Major revision

**Material read.**
- LaTeX source `scmlib/sed-precsupp-study/manuscript/sedps_acp_manuscript.tex`. Line numbers ("L") refer to this file.
- The compiled PDF, all figures, and `manuscript/tables/*.csv`.
- `analysis_report5/timeseries_15min.csv`.
- The earlier referee report and the authors' response in `manuscript/review/`. I read these but formed my own view, which on statistical robustness differs from the earlier report's (see C4).

**Supporting analysis.** The figures and CSV files cited as R1–R4 and `rc_*.csv` are in `manuscript/review/panel/reviewer_C_files/`. They were produced by `rc_analysis.py` and `rc_steady_state.py`, which read only the 15-min time series and `susceptibility.csv`.

**How the persona was chosen.** Before writing, I checked by web search that this perspective fits the published record. F. Glassmeier (TU Delft, Geoscience and Remote Sensing) has published on:
- LES ensembles of nocturnal marine stratocumulus;
- Gaussian-process emulation of stratocumulus susceptibility;
- LWP adjustment timescales and steady states, with Hoffmann, Yamaguchi and Feingold;
- the ship-track argument in Glassmeier et al. (2021, *Science*).

The requested focus matches that record, so I did not adjust the persona. The Hoffmann et al. (2020) steady-state paper appeared in *J. Atmos. Sci.*, not ACP, and is cited that way below.

---

## 1. Summary

The authors ran 288 DP-EAMxx simulations of DYCOMS-II RF02, each 12 h long. Horizontal grid spacing ranges from 40 km to 312 m, target N_d from 20 to 1000 cm⁻³, and the cloud-droplet sedimentation factor takes three values. The N_d dependence of KK2000 autoconversion is either on or off. The paper defines susceptibilities S = Δln LWP/Δln N_d from hour 10–12 means and reports these findings:
- S on the moderate branch is positive (about 0.25) at 10–40 km.
- It decreases monotonically as the grid is refined and is weakly negative (about −0.05) at 312 m. The LWP maximum (the "turning point" of the inverted V) moves to about 100 cm⁻³.
- The weak negative branch persists without the N_d dependence of autoconversion and steepens with faster sedimentation.

The revision is careful about caveats. The previous round removed most overstatements, and the abstract now says the negative branch is "smaller than one hour of LWP drift in these single, transient runs".

The data set is valuable. I expect the resolution dependence of the precipitation sink (Sect. 3.5) and the grid-dependent sign of within-scene LWP–N_d covariability (Sect. 3.9) to be cited widely.

My main concern is how the time dimension is treated. The paper treats S(10–12 h) as the result and treats its time evolution as a caveat. In these runs, however, every N_d level starts from the same cloud at t = 0, so S(t) is an adjustment trajectory. The base state is itself still spinning up at coarse spacing and spinning down at fine spacing. Part of the "resolution dependence" is therefore a dependence of adjustment rates and of how far each configuration has moved from a common initial state, not only of an end state.

With the existing 15-min data, I find:
1. At 2–4 h, S₁₀₀→₂₀₀ is the same at all Δx ≥ 2.5 km. The spread across Δx builds up over the run.
2. At 312 m, LWP relaxes toward an equilibrium with a well-defined e-folding time of about 4–8 h. The hour 10–12 values are about one e-folding past hour 6, and the extrapolated steady-state susceptibility has a wide range that includes zero.
3. The turning point of the inverted V is still moving at 12 h.
4. The 3D-turbulence on/off twins, which already exist, give a direct estimate of the sampling noise. It is small (σ_S ≈ 0.01–0.02). In a 240 km domain the threat to the conclusions therefore comes from transience, not from internal variability.

These points can be addressed largely by reframing the paper and adding analyses of data that already exist. A short set of 24–48 h runs would strengthen the paper considerably (Sect. 5).

---

## 2. Recommendation

**Major revision.** No new simulations are strictly required for publication if the claims are restated as statements about an 11 h adjustment trajectory and the time-resolved analyses below are added. I recommend a small set of extended runs (C6) and would rate the paper considerably higher with them.

---

## 3. Major comments

### C1. S(10–12 h) is a point on an adjustment trajectory, not a property of the configuration. Make the trajectory the primary result.

All runs at a given Δx start from the same profiles (LWP ≈ 160 g m⁻² at t = 0). N_d is imposed from the start. S(t = 0) is therefore zero by construction, and S(t) describes how LWP adjusts to an N_d perturbation applied at t = 0. This is the same quantity as the adjustment slope k(t) in the LES-ensemble literature: Glassmeier et al. (2021) and Chen et al. (2025) define k from paired runs with and without a perturbation. The difference here is that the unperturbed base state is not in equilibrium either.

From the time series (R2; `rc_S_extrapolation.csv`; suppression on, s = 1):

| Δx | S₁₀₀→₂₀₀, 2–4 h | S₁₀₀→₂₀₀, 10–12 h | dS/dt, 8–12 h fit (h⁻¹) |
|---|---|---|---|
| 40 km | 0.12 | 0.26 | +0.020 |
| 10 km | 0.12 | 0.24 | +0.012 |
| 5 km | 0.11 | 0.20 | +0.021 |
| 2.5 km | 0.11 | 0.11 | +0.020 |
| 1.25 km | 0.02 | 0.07 | +0.016 |
| 625 m | 0.00 | 0.03 | −0.001 |
| 312 m | 0.00 | −0.05 | −0.007 |

The table shows two things:
- At 2–4 h there are only two groups: Δx ≥ 2.5 km (about 0.11) and Δx ≤ 1.25 km (about 0). The monotonic decrease with Δx reported in Sect. 3.3 builds up over the run.
- Except at 625 m, S is still changing at 0.01–0.02 h⁻¹ at the end of the run, and it changes in opposite directions at the two ends of the resolution range.

A simple relaxation model makes the consequence concrete. If S relaxes exponentially, dS/dt = (S∞ − S)/τ, so S∞ ≈ S(12 h) + τ·dS/dt. At 312 m this gives S∞,₁₀₀→₂₀₀ of −0.09, −0.12 and −0.20 for τ = 5, 9 and 20 h. These timescales span the values in Chen et al. (2025), Hoffmann et al. (2024) and Glassmeier et al. (2021). At 1.25 km it gives 0.16–0.40, and at 40 km 0.38–0.69. S∞,₂₀₀→₁₀₀₀ at 312 m changes little (−0.04 to −0.05), because that branch has nearly levelled off.

This is a crude extrapolation, and I do not suggest the authors report it as a result. It does show that the ranking of resolutions and the magnitudes depend on the averaging window, and that the window was chosen without regard to the adjustment timescale.

**Requests.**
- Present S(t), not only S(10–12 h), as the main result. Fig. 4a–c is a good start but uses 2 h windows. Show it at the native 15-min resolution, with the instantaneous layer N_d, as in R2.
- State in the abstract and conclusions that the susceptibilities are values about 11 h after an N_d perturbation imposed on a common, non-equilibrium initial state.
- Separate the resolution dependence of the *rate* of adjustment from that of its *magnitude*. One option is to fit S(t) = S∞(1 − e^{−(t−t₀)/τ}) per configuration and report τ and S∞ with their (large) uncertainties.

### C2. Trajectory and phase-space view: the base state drifts much more than the signal, and the drift goes in opposite directions at the two ends of the resolution range

R1 shows trajectories in ln LWP–ln N_d space for each N_d level, with isochrones every 2 h, for suppression on and s = 1. R4 shows the corresponding LWP–dLWP/dt phase plane, the format used in Hoffmann et al. (2020) and Glassmeier et al. (2021).

**(a) Common-mode drift dominates the differential signal.** Between hours 6 and 11.5, ln LWP changes as follows:
- At 312 m, by −0.31, −0.34 and −0.37 at targets 100, 200 and 1000. The Δln LWP between targets 100 and 200 changes by only −0.03, about 10 % of the common drift.
- At 40 km, by +0.23 to +0.39, with a differential change of +0.08.

The 40 km and 312 m clouds therefore move in opposite directions through phase space during the analysis window, and S is a small difference between nearly parallel trajectories. The common drift largely cancels in S.

For this reason the comparison in L213 and the abstract ("smaller than the LWP decrease of each run in one hour") does not measure the uncertainty of S. The relevant measures are:
- the drift of the *difference*, i.e. dS/dt (about 15 % of S per hour at 312 m on the moderate branch);
- the noise of the difference (C4).

Please replace this argument.

**(b) Relaxation toward a steady state at 312 m.** At 312 m, dLWP/dt is tightly linear in LWP over hours 6–12 (correlation −0.78 to −0.94 for N_d ≥ 50 with suppression on, and −0.86 to −0.97 with it off; `rc_relaxation_fits.csv`). That is, dLWP/dt ≈ −(LWP − LWP_eq)/τ, with:
- τ ≈ 5.7–7.8 h with suppression on (4.1–5.9 h with it off);
- LWP_eq ≈ 44–55 g m⁻², about 25–35 % below the 12 h values.

This is the behaviour expected from Hoffmann et al. (2020), and τ lies between the roughly 5 h LWP-perturbation timescale of Chen et al. (2025) and the roughly 9 h thermodynamic timescale used by Hoffmann et al. (2024). L233 should therefore be revised. It says adjustment timescales are "longer than the simulation, as in LES … (Glassmeier et al., 2021)". In fact, at 312 m the LWP relaxation timescale is about half the run length. What has not converged is the small differential between runs, and possibly the slow inversion-height adjustment (at 312 m, z_i still rises by about 13 m h⁻¹ in hours 10–12 for most runs, cf. the slow manifold of Bretherton et al., 2010).

At 2.5 km–625 m and high N_d, LWP is nearly stationary in hours 6–12 (|dln LWP/dt| ≲ 1–3 % h⁻¹), and τ cannot be constrained. At 10–40 km, high-N_d LWP is still rising by 5–7 % h⁻¹, and the fitted LWP_eq is unconstrained (330–870 g m⁻² at targets 200–1000 at 40 km).

**(c) Steady-state extrapolation with uncertainty** (`rc_steady_state_S.csv`). Using LWP_eq from (b), with a 1 h moving-block bootstrap of the tendency residuals giving a 90 % interval, at 312 m with suppression on:

| s | branch | S, 10–12 h | S_eq (90 % interval) |
|---|---|---|---|
| 1 | S₁₀₀→₂₀₀ | −0.05 | −0.14 (−0.42 to +0.21) |
| 1 | S₂₀₀→₁₀₀₀ | −0.04 | +0.01 (−0.12 to +0.12) |
| 2 | S₁₀₀→₂₀₀ | −0.08 | −0.25 (−0.56 to −0.04) |
| 2 | S₂₀₀→₁₀₀₀ | −0.07 | −0.16 (−0.39 to +0.01) |

With suppression off, s = 1 gives S₁₀₀→₂₀₀ = −0.05 (−0.19 to +0.19). In other words, the 12 h runs do not determine the sign of the steady-state susceptibility at 312 m and s = 1, even though, by C4, the 12 h values themselves are robust to sampling noise. The sedimentation dependence (more negative for s = 2) is the more robust feature, which agrees with the paper's emphasis.

**(d) N_d drifts along the trajectory, with opposite signs at coarse and fine spacing.** The layer N_d in the 15-min output changes with time:
- by −2.4 to −2.8 % h⁻¹ at Δx ≤ 625 m in hours 6–12, because the cloud rises into air with lower CCN and P3 floors N_d at the height-dependent CCN (Sect. 2.3);
- by +1.1 to +1.6 % h⁻¹ at 10–40 km and high N_d.

Over 10 h this is roughly −25 % at 312 m (e.g. 228 → 163 cm⁻³ at target 200). The trajectories in R1 therefore move diagonally, with d ln LWP/d ln N_d along the trajectory of about +2 at 312 m.

This does not bias S much, because at 312 m all high-N_d targets drift alike and the Δln N_d between them is nearly preserved. It does matter for three reasons:
- It is an artefact of the configuration that LES with constant or processed N_d does not have, so it should be discussed when comparing timescales with LES.
- It means the perturbation is not constant in time.
- Any reader who regresses LWP on N_d across time in one run would obtain a spurious slope of about +2.

The text at L87 quotes an N_d drift of < 17 % from snapshots at 6 and 12 h. Please report the full 2–12 h drift as well, and its sign by Δx.

**Requests.**
- Add a phase-space figure (R1-type trajectories with isochrones, or R4-type tendency phase planes) for at least 40 km, 2.5 km and 312 m.
- Distinguish the timescales: LWP relaxation, approach of S, and inversion-height drift.
- Report the relaxation fits (τ, LWP_eq and their uncertainty) where they are constrained.
- Drop the one-hour-drift argument.

### C3. The inverted V is time-dependent. Report the turning point as a function of time, and test it against the Hoffmann et al. (2024) heuristic.

R3 (`rc_peak_location.csv`) gives the N_d of maximum LWP, from a parabola in ln N_d through the three highest points (suppression on, s = 1):
- At 312 m it falls from 150–350 cm⁻³ at 3–5 h to about 105 cm⁻³ at 9 h and about 90 cm⁻³ at 12 h, and it is still falling.
- At 625 m and 1.25 km it oscillates between about 150 and 300 cm⁻³ with a period of several hours.
- At 2.5 km the turning point drops below the top N_d level only at about 5 h; at 5 km, only at about 9.5 h.
- At 10–40 km it stays at the upper N_d bound throughout.

The statement that the inverted V "appears only at Δx ≤ 5 km" (L202) therefore holds at 12 h. At 5 km it holds only after hour 9.5, and at 6 h it would read "Δx ≤ 2.5 km". The location of the maximum "about 100 cm⁻³ at 312 m" (abstract, conclusion 1) is a 12 h snapshot.

This matters for the comparison with satellite composites (L202, Sect. 4.3). The central argument of Glassmeier et al. (2021) is that a snapshot of an evolving adjustment, as in ship tracks observed hours after emission, misrepresents the adjustment that is relevant for climate. Satellite inverted-V composites mix clouds of all ages and meteorologies. A 12 h snapshot of an idealised trajectory is neither an early-time ship-track analogue nor a climatological steady state. The paper should say which of the two it is closer to.

Hoffmann et al. (2024) provide a simple, testable framework. In their heuristic model, the low-N_d slope m_l and the high-N_d slope m_h of the steady-state L(N) are linked by m_l = (2/3)(m_h + 1), and the transition lies near N ≈ 100 cm⁻³. Applying this to the paper's own susceptibility table (`rc_hoffmann2024_eq9.csv`), suppression on:
- **Sub-kilometre spacing, s ≤ 1.** S₁₀₀→₂₀₀ predicts S₂₀→₅₀ = 0.63–0.69, close to the simulated 0.56–0.76.
- **Sub-kilometre spacing, s = 2.** The simulated S₂₀→₅₀ (0.97–1.00) is much larger than predicted (0.61–0.69).
- **10–40 km.** The prediction (0.78–0.90) is far above the simulated 0.37–0.41. These runs have no thermodynamically limited, non-precipitating regime, so the heuristic is not expected to apply there.

Caveats apply: the 12 h values are not steady states, and the sub-kilometre S₂₀→₅₀ includes a cloud-cover part of 0.33–0.53. Even so, this offers a physically based way to interpret where the turning point lies and why it moves with Δx, which the present Discussion (L323) states only qualitatively.

**Requests.**
- Show the turning point against time for each Δx (and for s = 0.5 and 2).
- Qualify the abstract and conclusion 1 accordingly.
- Consider the Eq. (9) consistency test of Hoffmann et al. (2024) as an interpretive diagnostic.

### C4. Statistical robustness: quantify the uncertainty with data you already have. The answer is more favourable than the paper assumes.

The paper (L131, L213, L341) says the spread in S reflects temporal sampling only. It asserts that "initial-condition spread in domain-mean LWP … is typically of a few per cent" without a citation, and on that basis it calls the sign at 312 m "not established". I agree that a single realisation needs a noise estimate. I disagree that the present data cannot provide one, and the estimate they give is smaller than the paper implies.

**(a) 3D-turbulence twins as perturbation pairs.** The 71 runs with the horizontal SHOC diffusion switched on (Appendix C) differ from their twins by a tiny, mostly non-systematic change to the dynamics (Sect. 3.7: |ΔLWP| < 1.5 %). They are, in effect, perturbed-physics twins. From the 15-min series (`rc_t3d_twins_LWP.csv`, `rc_t3d_twins_S.csv`):
- The RMS relative LWP difference between twins grows from 0.2 % at 2 h to 0.7–0.9 % at 10–12 h, at both 625 m and 312 m. Its mean is +0.3–0.5 %, which is the systematic part.
- The difference in S (10–12 h) between twins has a standard deviation of 0.008–0.010 on the clean and moderate branches and 0.002–0.004 on the polluted branch. The maximum |ΔS| is 0.016 over the six (s, suppression) configurations per branch at each grid spacing. The LWP statistics above use all 33 (312 m) and 36 (625 m) pairs.
- At 312 m, s = 1, suppression on: S₁₀₀→₂₀₀ = −0.048 (off) versus −0.055 (on), and S₂₀₀→₁₀₀₀ = −0.035 versus −0.036.

A propagation check agrees. A per-run noise of about 0.9 % in ln LWP over Δln N_d ≈ 0.68 gives σ_S ≈ 0.02 on the moderate branch. Over Δln N_d ≈ 1.6 it gives σ_S < 0.01 on the polluted branch. The 12 h susceptibilities at 312 m are therefore about 2.5σ (moderate) and more than 4σ (polluted) from zero.

Two caveats apply. The twins probably share the initial random perturbation, and their divergence is still growing at 12 h, so this is a lower bound on true initial-condition spread. Please state which seed each run uses. If all N_d levels share a seed, the differences benefit from common random numbers early on, and that should also be stated.

Even so, in a 240 km domain with about 150–350 mesoscale cells, the evidence points to transience (C1, C2c) and structural choices (mixing-length cap, vertical grid) as the main threats to the sign of S at 312 m, not internal variability. The text should say so. The proposed 3–5-member ensembles (L341) remain useful for confirming the noise level, but the paper should not imply that they would settle the sign of the steady-state response.

**(b) Temporal sampling SD.** The 15-min samples within a window are strongly autocorrelated. The lag-1 autocorrelation of the detrended S series in hours 8–12 is 0.4–0.9, typically 0.6–0.9 (`rc_S_extrapolation.csv`), so a 2 h window holds only about 1–3 effective samples. Report the SD with an effective sample size, or replace it with the twin-based estimate.

**(c) Low-frequency oscillations at coarse spacing.** L211 says LWP at Δx ≥ 5 km oscillates on timescales of about 15 min. After removing a quadratic trend from hours 4–12, the dominant periods are about 1.4–2 h at 40 km (residual SD about 4 g m⁻² at targets 200 and 1000) and about 4 h at 5 km. S₁₀₀→₂₀₀ at 40 km oscillates by about ±0.04 around its trend (R2). A 2 h window is about one period, so the window mean depends on phase. Please characterise this oscillation. It may be a column-physics limit cycle involving SHOC, radiation (called every 300 s) and microphysics. Then either average over whole periods or fit a trend.

**(d) Structural consistency across s.** The monotonic dependence of S₂₀₀→₁₀₀₀ on s at all Δx ≤ 2.5 km is itself evidence against noise: noise would not be ordered by s across four resolutions. This point could be made explicitly.

### C5. Comparison with LES-ensemble results: compare like with like, and check the citations

- **Like-for-like timing (L327).** The text says the 312 m slope "is an order of magnitude smaller than the steady-state adjustments inferred from LES of non-precipitating stratocumulus (Glassmeier et al., 2021)". This compares an 11 h transient with a steady state. A fair comparison uses the LES k at a similar time after perturbation. With the k∞ ≈ −0.64 and τ ≈ 20 h attributed to Glassmeier et al. (2021) by Chen et al. (2025), k(11 h) ≈ −0.64(1 − e^{−11/20}) ≈ −0.27. Chen et al. (2025) find δL converging within roughly 8–12 h, median k at 11–12 h more negative than this curve, k rarely below −0.4 within 24 h, and k more negative at low baseline N. On a like-for-like basis the 312 m value (−0.05) is about five times weaker, not an order of magnitude. That is still a substantial difference, and it is worth explaining. The candidate reasons in L327 are appropriate:
  - no size-dependent cloud-top evaporation in SHOC's saturation adjustment;
  - 50 m vertical spacing;
  - the free-tropospheric humidity of RF02;
  - drizzle.

  Please rephrase, and give the comparison time explicitly.
- **Regime.** Glassmeier et al. (2021) and Chen et al. (2025) concern nocturnal, *non-precipitating* stratocumulus. The 312 m runs at N_d ≥ 100 cm⁻³ are effectively non-precipitating (surface rain ≤ 0.011 mm d⁻¹), so this subset is the right one to compare. The 40 km runs are a different regime.
- **Citation check (L50).** "LES ensembles reproduce the inverted-V shape and indicate long adjustment time scales (Glassmeier et al., 2019, 2021)". Glassmeier et al. (2019) is mainly an emulator study of cloud-fraction and cloud-albedo susceptibilities (∂ln rCRE/∂ln N, ∂ln rCRE/∂ln LWP). Please check that it supports the inverted-V statement, or cite it for what it shows: that cloud-fraction susceptibility controls the rCRE susceptibility. That is relevant here, because S₂₀→₅₀ at sub-kilometre spacing is half or more a cloud-cover effect.
- **Boundary-layer depth as a co-variate.** Possner et al. (2020) show that the magnitude of the negative LWP susceptibility roughly triples as boundary-layer depth increases from about 300 m to more than 1200 m. In these runs z_i at target 200 rises from 863 m (40 km) to 1016 m (312 m), and it increases with time at every Δx. Part of the resolution and time dependence of the high-N_d branch may therefore reflect boundary-layer depth. Please discuss this, or condition S on z_i, for example by comparing S at matched z_i using S(t) from different times.
- **Radiative relevance.** At sub-kilometre spacing, cloud cover contributes 0.33–0.53 to S₂₀→₅₀. The LES-ensemble work emphasises that the radiatively relevant quantity combines cloud fraction and in-cloud albedo. Even with shortwave radiation off, an offline albedo or rCRE susceptibility could be computed from the column LWP and cloud-top N_d. It would show whether the resolution dependence of S matters radiatively.

### C6. What 24–48 h experiments would add, and how to design them

The paper already lists "extend a subset to 24 h or longer" (L341). From the C1–C3 analysis I would rank the expected gains as follows:
1. **Sign of the steady-state polluted and moderate branches at 312 m and 625 m.** Under the C2 relaxation fits (τ ≈ 4–8 h), 24 h is about 2–3 e-foldings past hour 6, enough to see whether S levels off. Only then can S∞ be compared meaningfully with LES k∞.
2. **Whether the positive coarse-resolution response saturates.** At 40 km, high-N_d LWP is still rising by about 15–20 g m⁻² h⁻¹ at 12 h.
3. **Whether the turning point of the inverted V settles** (R3).
4. **The slow, inversion-height part of the adjustment** (Bretherton et al., 2010), which constant forcing over 12 h cannot reach.

A design that separates the base-state spin-up from the N_d adjustment would be much more informative than simply running the present setup for longer:
- Spin up each Δx for 6–12 h at a reference N_d (e.g. 100 cm⁻³, s = 1).
- Restart with N_d perturbed to 200 and 1000 cm⁻³, keeping an unperturbed control.
- Integrate for 24–36 h.

This is the paired-perturbation design of Glassmeier et al. (2021) and Chen et al. (2025). It yields k(t) relative to a control on the same trajectory, removes the common-mode drift (C2a) from the denominator, and makes τ directly comparable with LES. The 625 m and 312 m restart capability is already in place (Sect. 2.3).

A minimal set:
- Δx: 40 km, 2.5 km, 625 m and 312 m;
- N_d: 100 (control), 200 and 1000;
- s: 1 and 2;
- suppression on;
- 2–3 seeds for the controls at 312 m.

That is roughly 30 runs, most of them cheap.

Constant nocturnal forcing for 48 h is unrealistic. Interactive surface fluxes (Sect. 4.4), and later a diurnal cycle (Chen et al., 2024), would be natural follow-ups. They need not be part of this paper.

---

## 4. Minor comments

1. **Abstract (L39).** Replace "smaller than one hour of LWP drift" with a statement based on dS/dt and on a noise estimate (C2a, C4). Add "about 11 h after the N_d perturbation" or similar wherever S is quoted.
2. **L131.** S uses N_d from the 3D snapshots at 10 and 12 h, while the 15-min layer N_d (`Nd_layer_cm3`) is available. Using it would give consistent instantaneous S(t), as in R2. In my recomputation the two agree within about 0.01 on S₁₀₀→₂₀₀ at 312 m and 40 km.
3. **L211.** "LWP oscillates on time scales of about 15 min": see C4c. The dominant variability at 40 km has periods of about 1.4–2 h.
4. **L213.** "Initial-condition spread … typically of a few per cent" needs a citation. It is also larger than the twin-based estimate for this domain (C4a).
5. **L233.** Distinguish the LWP relaxation timescale (about 4–8 h at 312 m) from the timescale over which S approaches its limit (C2b).
6. **L202 / conclusion 1.** The inverted V and its maximum are time-dependent (C3).
7. **L87.** Report the 2–12 h drift of layer N_d by Δx, and its sign (C2d).
8. **Appendix C / Sect. 2.3.** The text says 35 completed 3D-turbulence pairs at 312 m. `timeseries_15min.csv` contains 33 runs with 3D turbulence on at 312 m: target 1000 with s = 1, suppression off, and with s = 2, suppression off, are missing in addition to the failed run. Please check this, or state that the 15-min file is incomplete.
9. **Fig. 4.** Add the native 15-min S(t) and the 3D-turbulence twins (dotted) to (a–c), as in R2. Add a 40 km suppression-off panel to (d–f) for symmetry.
10. **Fig. 3.** The error bars are the temporal SD. Replace them with, or add, the twin-based σ_S (C4a). Without that the reader cannot judge which differences are significant.
11. **L288.** For the cell aspect ratios (λ/z_i = 13–20), the network description of closed-cell organisation in Glassmeier and Feingold (2017) may help interpret whether cell size is still adjusting at 12 h. Is λ also time-dependent?
12. **Notation.** The LES literature uses k for the adjustment slope and reserves "susceptibility" for radiative quantities in some papers. A sentence stating that S here corresponds to k in Glassmeier et al. (2021) and Chen et al. (2025) would help readers.
13. **L341.** "Initial-condition ensembles of three to five members …" Please add that the twin analysis already bounds the noise (C4a), and give the paired-perturbation design (C6) as the preferred extension.
14. **Sect. 3.6 budget.** The budget can be written in the tendency form of Hoffmann et al. (2020): radiative cooling against entrainment warming and drying around the steady state. Expressing the 312 m budget at the fitted LWP_eq, rather than at the transient state, would show which terms balance in the steady state.

---

## 5. Feasible additional analyses with existing data

All of the following run in seconds on a login node from `timeseries_15min.csv` and the existing tables. My versions are in `reviewer_C_files/` for the authors to check and improve.

| # | Analysis | Purpose | My result (if done) |
|---|---|---|---|
| A1 | S(t) at 15-min resolution, using simultaneous 1 h means of LWP and layer N_d (R2, `rc_S_t_15min.csv`) | Primary result (C1) | The spread in S₁₀₀→₂₀₀ across Δx ≥ 2.5 km builds up over the run. S is still changing at 0.01–0.02 h⁻¹ at 12 h except at 625 m. |
| A2 | Phase-space trajectories and isochrones (R1); LWP–dLWP/dt phase plane (R4) | Trajectory interpretation (C2) | Common drift is about 10× the differential signal. At 312 m: monotonic relaxation. At 2.5 km and low N_d: limit cycles. At 40 km: sustained thickening with 1.4–2 h oscillations. |
| A3 | Linear relaxation fits dLWP/dt = −(LWP − LWP_eq)/τ over 6–12 h, with block bootstrap (`rc_relaxation_fits.csv`, `rc_steady_state_S.csv`) | Timescales; steady-state extrapolation (C2b, c) | 312 m: τ ≈ 4–8 h, r = −0.78 to −0.97. S_eq,₁₀₀→₂₀₀ = −0.14 (−0.42 to +0.21) for s = 1. Unconstrained at 1.25 km–625 m (near-stationary) and at 10–40 km (still thickening). |
| A4 | N_d of maximum LWP against time (R3, `rc_peak_location.csv`) | Time evolution of the inverted V (C3) | 312 m: about 90 cm⁻³ at 12 h and still falling. 625 m and 1.25 km oscillate between about 150 and 300 cm⁻³. 5 km turns over only after about 9.5 h. |
| A5 | 3D-turbulence twins as perturbation pairs (`rc_t3d_twins_*.csv`) | Noise estimate for S (C4a) | σ_ΔS ≈ 0.008–0.010 (moderate and clean branches), ≈ 0.002–0.004 (polluted branch). RMS LWP difference 0.7–0.9 % at 10–12 h. |
| A6 | Lag-1 autocorrelation and effective sample size of the detrended S | Honest temporal-sampling error (C4b) | r₁ = 0.6–0.9, so about 1–3 effective samples per 2 h window. |
| A7 | Hoffmann et al. (2024) Eq. (9) test, m_l = (2/3)(m_h + 1) (`rc_hoffmann2024_eq9.csv`) | Physical interpretation of the turning point (C3) | Consistent at sub-kilometre spacing with s ≤ 1. Inconsistent at 10–40 km and for s = 2. |
| A8 | Spectral analysis of the detrended coarse LWP | Characterise the coarse oscillation (C4c) | 40 km: periods 1.4–2 h. 5 km: about 4 h. |
| A9 | S conditioned on z_i, using S(t) from all times and Δx | Separate boundary-layer depth from resolution (C5, Possner et al., 2020) | Not done |
| A10 | Offline albedo or rCRE susceptibility from column LWP and cloud-top N_d | Radiative relevance of the cloud-cover part (C5) | Not done |
| A11 | Hoffmann et al. (2020) stability criterion: does w_e increase with LWP along each trajectory? (requires 2 h-window w_e from `ml_budget.csv`) | Whether a stable steady state exists at each Δx | Not done |

---

## 6. Literature drawn on (verified by web search on 2026-11-11; DOIs checked)

1. Glassmeier, F., Hoffmann, F., Johnson, J. S., Yamaguchi, T., Carslaw, K. S., and Feingold, G.: Aerosol-cloud-climate cooling overestimated by ship-track data, *Science*, 371, 485–489, 2021, https://doi.org/10.1126/science.abd3980. Used for the time dependence of the adjustment slope and the snapshot-versus-steady-state argument. The k∞ ≈ −0.64 and τ ≈ 20 h values are quoted as summarised by Chen et al. (2025); I did not read the full text.
2. Glassmeier, F., Hoffmann, F., Johnson, J. S., Yamaguchi, T., Carslaw, K. S., and Feingold, G.: An emulator approach to stratocumulus susceptibility, *Atmos. Chem. Phys.*, 19, 10191–10203, 2019, https://doi.org/10.5194/acp-19-10191-2019. Used for the citation check and the cloud-fraction and rCRE susceptibility points.
3. Hoffmann, F., Glassmeier, F., Yamaguchi, T., and Feingold, G.: Liquid water path steady states in stratocumulus: insights from process-level emulation and mixed-layer theory, *J. Atmos. Sci.*, 77, 2203–2215, 2020, https://doi.org/10.1175/JAS-D-19-0241.1. Used for the steady states, the relaxation and phase-plane view, and the stability criterion.
4. Hoffmann, F., Glassmeier, F., and Feingold, G.: The impact of aerosol on cloud water: a heuristic perspective, *Atmos. Chem. Phys.*, 24, 13403–13412, 2024, https://doi.org/10.5194/acp-24-13403-2024. Used for the m_l = (2/3)(m_h + 1) relation, the transition near 100 cm⁻³, and τ_t ≈ 9 h.
5. Possner, A., Eastman, R., Bender, F., and Glassmeier, F.: Deconvolution of boundary layer depth and aerosol constraints on cloud water path in subtropical stratocumulus decks, *Atmos. Chem. Phys.*, 20, 3609, 2020, https://doi.org/10.5194/acp-20-3609-2020. Used for boundary-layer depth as a co-variate of the negative susceptibility.
6. Chen, Y.-S., Zhang, J., Hoffmann, F., Yamaguchi, T., Glassmeier, F., Zhou, X., and Feingold, G.: Diurnal evolution of non-precipitating marine stratocumuli in a large-eddy simulation ensemble, *Atmos. Chem. Phys.*, 24, 12661, 2024, https://doi.org/10.5194/acp-24-12661-2024. Used for the diurnal follow-up.

Further references (not Glassmeier-authored, or not re-verified online):
- Chen, Y.-S., Prabhakaran, P., Hoffmann, F., Kazil, J., Yamaguchi, T., and Feingold, G.: Magnitude and timescale of liquid water path adjustments to cloud droplet number concentration perturbations for nocturnal non-precipitating marine stratocumulus, *Atmos. Chem. Phys.*, 25, 6141–6159, 2025, https://doi.org/10.5194/acp-25-6141-2025. Verified. Used for the roughly 5 h δL timescale, the k(11–12 h) comparison and the paired-perturbation design.
- Glassmeier, F. and Feingold, G.: Network approach to patterns in stratocumulus clouds, *Proc. Natl. Acad. Sci.*, 114, 10578–10583, 2017, https://doi.org/10.1073/pnas.1706495114. Verified.
- Bretherton, C. S., Uchida, J., and Blossey, P. N.: Slow manifolds and multiple equilibria in stratocumulus-capped boundary layers, *J. Adv. Model. Earth Syst.*, 2, 14, 2010, https://doi.org/10.3894/JAMES.2010.2.14. DOI taken from the manuscript's bibliography, not re-verified.
