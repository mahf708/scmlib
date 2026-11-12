# Response to the editor and the five reviewers

We thank the editor and the five reviewers. The manuscript has been restructured around a single mixed-layer argument:

> grid spacing → entrainment → cloud depth, cloud base and precipitation → precipitation-to-entrainment-drying regime → susceptibility.

Each link is now tested with diagnostics from the existing output. No new simulations were possible. All additional analyses use existing output on CPU nodes, and the experiments that the reviewers recommend are listed as future work in Sect. 4.3.

Numbers quoted by the reviewers were recomputed before use. Where our values differ, we use ours and say so below.

## Files and locations

New scripts are in `manuscript/scripts/`:

| Script | Purpose |
|---|---|
| `rev2_3d.py` | 3D snapshots: inversion flux budget, inversion thickness, cloud-top height spread, autoconversion enhancement, offline cloud-top sedimentation flux, near-grid share of w variance |
| `rev2_cols.py` | Column statistics: tiles, retrieval-like Nd, pooled composites, 3.75 km aggregation |
| `profiles_ts2.py` | Cloud-layer means, jumps at several offsets, free-tropospheric drift, winds |
| `rev2_analysis.py` | Susceptibility components, regime regressions, twins, S(t), peak location, relaxation fits and steady-state S, on/off split, decoupling, efficiencies, S at 55 cm⁻³ |
| `rev2_analysis2.py` | Inversion flux budget, sedimentation-flux regression, tile bootstrap, satellite composites, η sensitivity, free-tropospheric drift, in-cloud budget with coupling flag |
| `make_figures_rev2.py` | Figures |

New tables are in `dp_screamxx_sedps_12h/manuscript/tables/rev2_*.csv`, `ml_timeseries2.csv` and `cloudcover_3d.csv`.

The tracked-changes PDF is `dp_screamxx_sedps_12h/manuscript/sedps_acp_manuscript_diff.pdf`.

**Run count.** The last 312 m run with 3D turbulence (target Nd 1000, s = 2, Nd-dependent autoconversion) has not completed (`.sedps_done` = 1). The text therefore states 71 of 72 such runs: 36 pairs at 625 m and 35 at 312 m. Reviewer C counted 33 pairs at 312 m because `analysis_report5/timeseries_15min.csv` predates two runs that finished later. The tables used in the paper contain 35.

---

## Editor

**Authorship and AI policy.** These are deferred to the human study leads, as the editor requested. The author list is unchanged ("Claude, Anthropic"), with N. Mahfouz named as contact in the Acknowledgements. Reviewers A and B note that the ACP/Copernicus AI policy and COPE guidance probably preclude AI authorship. The study leads must decide on authorship, ownership of the text and interpretation, and the AI-use statement before submission.

**Data availability.** No persistent identifier could be created during the revision. The section gives the code branches and states that output and tables are available on request. A Zenodo archive (model branch, scripts, `tables/*.csv`, `fields/*.npz`, `rev2/cols/*.npz`) remains to be done by the study leads.

### Priority 1

**P1.1 Base-state regime as organising variable.** Done (new Sect. 3.4, Fig. 6).
- We reproduce B's correlation: S₁₀₀→₂₀₀ (Nd-dependent autoconversion) against ln(P_sfc/F_ent,q) of the lower-Nd run gives r = 0.92 over the 24 combinations of Δx and s.
- The regime ratio explains 84 % of the variance. Adding log Δx raises this to 86 %; log Δx alone explains 75 %.
- The relationship is weaker on the middle branch (r = 0.70), on the polluted branch (r = 0.75, where log Δx adds explanatory power: 57 % → 85 %), and with Nd-independent autoconversion (r = 0.45–0.65). It is absent on the clean branch, which is dominated by cloud cover.
- The abstract, Sect. 4.1 and conclusion 2 now say that grid spacing acts mainly by setting the cloud regime in EAMxx. We also state where this does not hold.

**P1.2 Time evolution and transience.** Done (new Sect. 3.3, Fig. 5).
- S(t) is now computed from the 15 min output with cloud-top Nd.
- At 2–4 h, S₁₀₀→₂₀₀ is 0.10–0.11 from 40 km to 2.5 km, which confirms C. It is near zero at ≤1.25 km.
- We show the cloud-top Nd of the LWP maximum against time (Fig. 5c) and the dLWP/dt–LWP phase plane at 312 m (Fig. 5d).
- Exponential relaxation fits of LWP(t), with a paired moving-block bootstrap, constrain an equilibrium only at 312 m (τ = 4–7 h). Equilibrium S on the moderate branch is −0.11 to −0.21 in 5 of 6 configurations, and −0.13 (−0.23 to +0.06) for s = 1. On the polluted branch it is −0.17 to +0.06.
- Elsewhere the fits are unconstrained, and we say so.
- z_i,eq = w_e/D (1/D = 74 h) is about 1000 m at 40 km and about 2200 m at 312 m.
- The comparison with Chen et al. (2025) is now at a similar time after perturbation, without second-hand numbers.
- "Nocturnal" and "still adjusting" appear in the abstract, Sects. 1, 2.2, 3.3 and 4.3, and the conclusions.

**P1.3 In-cloud versus cloud-fraction terms, cloud-top Nd, forcing relevance.** Done (Sect. 2.4, Sect. 3.2, Fig. 4, Table 5).
- All susceptibilities now use cloud-top Nd as the abscissa (151–162 cm⁻³ at target 200 at every Δx).
- S = S_ic + S_c on every branch, with maximum-overlap cover; the threshold definition is also quoted.
  - At 312 m the clean branch is 0.71 all-sky, made up of 0.39 in-cloud plus 0.32 cloud cover (threshold cover: 0.19 + 0.52). This reproduces D's value of 0.19.
- The optical-depth susceptibility d ln τ/d ln Nd = 1/3 + (5/6)S_ic stays positive everywhere: 0.55 → 0.29 on the moderate branch, 0.64–0.77 on the clean branch.
- Offline albedo split into Twomey, LWP and cloud-cover terms. We reproduce A's numbers within about 0.03:
  - adjustment/Twomey on the moderate branch: +58 % (40 km) to −13 % (312 m);
  - clean branch: +91 % to a factor of 2.0–3.2;
  - total moderate-branch albedo change: 0.079 → 0.046.
- S at a cloud-top Nd of 55 cm⁻³ is 0.35–0.47 (40 km to 1.25 km), 0.29 (625 m) and 0.06 (312 m).
- The abstract now says that the brightening is weakened, not that the adjustment changes sign.

### Priority 2

**P2.4 Is the entrainment change physical?** Done (Sect. 3.1, Fig. 2, Sect. 4.1).
- *Inversion flux budget from the 3D snapshots.* Resolved plus SHOC θ_l flux at its minimum below z_i, compared with −w_e Δθ_l (jump at +50 m): explicit fluxes carry 37–46 % at Δx ≤ 5 km and target Nd ≥ 200, roughly independent of Δx. The remainder includes radiative cooling in the entrainment zone and implicit mixing.
- *Inversion structure.* The inversion is 100–175 m thick (2–3 levels) at all Δx. The spread of cloud-top height is 32–41 m, less than one level.
- *Jump definition and η.* η is given for +50, +100 and +150 m and for the specified 6.7 K interface jump.
  - With the interface jump, η is 0.3–0.4 at coarse spacing and 0.58–0.75 at fine spacing. The steady reference is 0.7–0.8, and the observed range is 0.53–0.68 under the same definition.
  - η_obs is 0.9–1.2 with the +100 m definition.
  - The earlier "η > 1" was an artefact of the +100 m offset.
- *w\*-based efficiency.* A is 0.6–0.8 (≥10 km), 1.1–1.6 (5–1.25 km), 1.5–1.8 (625 m) and 2.0–2.6 (312 m). E's 2.9–3.0 used a different flux definition; we use our values.
- *Three regimes are described.* At ≥10 km the inversion is pinned (z_i rises 45 m in 12 h). At 5 km the run departs from the coarse solution after about 8 h, and 60–74 % of the resolved w variance lies below six physics spacings. At ≤2.5 km, at 312 m 28–31 % of the resolved w variance still lies at near-grid scales.
- Sect. 3.1 and Sect. 4.1 state that the 312 m runs are not an approximation to LES and are unlikely to lie on a path towards it.

**P2.5 Drizzle versus sedimentation.** Done (Sect. 3.5, Fig. 8).
- *Autoconversion switch split* (budget, target Nd ≥ 200). The rain-sink part is +4 to +6 % h⁻¹ at ≥5 km and +0.2 to +1 % h⁻¹ at 625/312 m. Δw_e(dependent − independent) is +0.2 mm s⁻¹ at 20–40 km and up to +1.4 mm s⁻¹ at ≤2.5 km.
- The term is renamed "Nd-dependent/-independent autoconversion" throughout.
- *Offline Stokes cloud-top sedimentation flux* (P3 gamma DSD). F_sed is 0.4–1.5 mm d⁻¹, and V_m is 1.0–1.2 (target 1000), 1.8–2.3 (target 200) and 3.8–5.3 cm s⁻¹ (target 20).
- Δw_e regressed on ΔF_sed (s = 2 versus 0.5, target Nd ≥ 200): −0.8 mm s⁻¹ per mm d⁻¹ at ≤2.5 km (r = −0.31), about 0 at ≥10 km.
- *Possible time-step artefact.* Cloud-top Nd relative to target decreases with s by 8–12 % at 40 km and not at 312 m, which reproduces D. This is discussed together with the process order (SHOC → SPA → P3, output after P3).

**P2.6 Robustness.** Done (Sect. 2.4, Sect. 3.7).
- *Perturbed twins* (71 pairs). The SD of ΔS is 0.007–0.010 (clean, middle and moderate branches) and 0.002–0.004 (polluted) at 625 and 312 m.
- *60 km tile bootstrap.* The SD is about 0.006 and 0.003 at sub-km spacing and up to 0.03 at 5 km. These replace the autocorrelated 15 min SD (Fig. 4, Table 5).
- The polluted-branch sign at ≤2.5 km (23 of 24 configurations) and the 312 m moderate-branch sign (all 6 configurations) are presented as outside the internal noise. Transience and structural choices are named as the main threats.
- The 625 m moderate branch changes sign with the autoconversion setting, and the location of the LWP maximum is stated to be unresolvable.

### Priority 3

**P3.7 Decoupling.** Done (Sect. 3.6, Fig. 10).
- Four metrics are used: the Jones test with the inversion base as the top of the layer, z_b − LCL of mixed-layer air, the buoyancy-flux minimum below cloud base relative to the surface value, and the cloud/subcloud w-variance ratio.
- *Coarse runs.* Δq_t is 1.1–1.5 g kg⁻¹ but the layer is coupled: Δθ_l is −0.85 to +0.11 K, the buoyancy-flux minimum is 0.4–1.1 of the surface value, and z_b is within 35 m of the LCL.
- *312 m runs at target Nd ≥ 100.* The buoyancy-flux minimum is 0.08–0.10 of the surface value and z_b − LCL is 50–70 m.
- This reproduces E's ranking.

**P3.8 Budget validity.** Done (Sects. 2.5 and 3.6, Fig. 9).
- In-cloud LWP plus an explicit cloud-cover term, with LCL sensitivities from cloud-layer air (0.6–0.9 z_i). The entrainment term is split into deepening and cloud-base parts (at 312 m, +10 to +20 and −30 to −50 % h⁻¹).
- Attribution is made only in coupled windows: 97 % of windows at ≥10 km, 58 % at 5 km, 11 % at 2.5 km and ≤3 % at ≤1.25 km.
- In coupled windows, the skill for in-cloud LWP is r = 0.72–0.76.
- No attribution is made at sub-km spacing.

**P3.9 Case fidelity.** Corrected (Sect. 2.2).
- The prescribed surface fluxes are now described as part of the protocol, and the recommendation of interactive fluxes was removed.
- The departures are now listed:
  - RRTMGP instead of the parametric radiation with its above-inversion term. θ_l at 2 km drifts by only −0.3 K in 12 h, and 300 m above z_i by ≤0.4 K, at all Δx.
  - No wind nudging or Coriolis force. The mixed-layer wind decays from 8.4 to 5.8–6.1 m s⁻¹, and the inversion shear is 3.8–4.6 m s⁻¹ at all Δx.
  - Nd varies with height.
  - The forcing is constant over 12 h.
- Specification values (jump 288.3 → 295 K, Nd 55 cm⁻³, fluxes) are taken from Wyant et al. (2007), which we read in full. The full text of Ackerman et al. (2009) could not be accessed, so it is cited only for statements in its abstract and the commonly reported ~5 m LES spacing.

**P3.10 Satellite section.** Moved to Appendix E and redone. It is labelled hypothetical because the case is nocturnal.
- Pooled composites use equal weight per run and a satellite-like filter (cf_top > 0.9, LWP > 20 g m⁻², r_e < 15 µm, τ > 3), with the Nd variance split into within-scene and between-run parts.
- Cloud-top Nd has a within-scene variance share below 1 %, so the pooled slope equals the between-run slope.
- A column-level adiabatic retrieval-like Nd (Grosvenor et al. 2018) is about 2× the model value, has a within-scene share of 46–52 %, and gives pooled slopes that are 25–50 % of the between-run slope. This holds at native resolution and at 3.75 km.
- The overcast/non-raining filter alone shifts the slope by up to +0.1.
- The unsupported caution in the former Sect. 4.3 and the former conclusion 6 were removed.

**P3.11 Economy and literature.**
- The paper is restructured around one mixed-layer argument.
- The old decomposition figure and caveats were moved to Appendix A.
- Conclusions are reduced to four.
- Fig. 10 (convergence) and the LWP table were folded into Fig. 2 and Fig. 3.
- The old satellite figure and the budget-skill appendix were removed.
- All suggested references were verified against Crossref and added (see "Literature" below).

**Future experiments.** All four suggestions are listed in Sect. 4.3: the paired-perturbation design, the 312 m pair with 10–15 m levels, the 36 h diurnal set, and s = 0 with a second matching Nd.

---

## Reviewer A

**E1 (AI authorship).** Deferred to the study leads (see Editor).

**E2 (data).** See Editor; Zenodo archiving remains open.

**A-M1 (translate S into ERF terms).** Done (Sect. 3.2, Table 5).
- We compute d ln τ/d ln Nd and an offline albedo split into Twomey, LWP_ic and cloud-cover terms using A's two-stream form.
- Our ratios agree with A's within about 0.03. For example, the moderate branch goes from +0.58 to −0.13 and the clean branch from 0.91 to 3.17.
- Not done: the two-stream calculation at fixed SZA or diurnal insolation and the PRP decomposition. They are not meaningful for a nocturnal case. The numbers are labelled potential albedo responses.
- The abstract and conclusion 1 now distinguish the sign of S from the sign of the brightening.

**A-M2 (emphasis on the ERF-relevant branch; smooth fits).**
- Added S at 55 cm⁻³ (local quadratic in ln Nd_top), the Nd_top above which |S| < 0.1 (664 → 54 cm⁻³), a single fit over all levels (0.22 → 0.10) and the S₅₀→₁₀₀ branch.
- The statement on the LWP maximum now calls it poorly constrained (a 3 % difference at 312 m and 625 m).
- The abstract leads with both the moderate and the clean branch. Carslaw et al. (2013) and Jia & Quaas (2023) are cited for the relevance of the clean branch.
- Not done: sigmoid fits. With six levels, a sigmoid adds parameters without constraint.

**A-M3 (CF versus in-cloud split).** Done (Fig. 4, Table 5, Sect. 3.2).
- S_ic and S_c are given for all branches. Both cover definitions are reconciled: 0.32 (maximum overlap) and 0.52 (threshold) at 312 m.
- The structural absence of a cloud-cover response at coarse spacing is stated.
- The cloud-cover increase with Nd-independent autoconversion at ≤2.5 km is now discussed.
- The comparison with satellite slopes now uses cautious wording.
- Not done: a separate subsection on the CF adjustment. It is integrated into Sect. 3.2 to keep the paper economical.

**A-M4 (resolution versus state).** Done; it is now the central figure (Fig. 6).
- Variance explained by state, by state plus log Δx, and by log Δx alone is reported per branch (see Editor P1.1).
- S_R on the moderate branch is 0.9 at 40 km and 2.4–2.8 at ≤2.5 km. The raining fraction of 1.0 at coarse spacing is compared with GCM behaviour.
- Pooling uses the 24 Δx × s combinations for each autoconversion setting.
- Partial: S_R is not compared quantitatively with Terai et al. (2012) beyond citing it, because our S_R is a two-point domain-mean estimate.

**A-M5 (robustness).**
- Done: tile bootstrap (60 km tiles × 8 instants), twin noise and sign counts. Our tile SDs are similar to A's (0.006 at 312 m).
- Not done: the ANOVA/linear model of ln LWP on all factors, and the time series of the spatial correlation between adjacent-Nd runs. The twin-based noise floor serves the same purpose.

**A-M6 (satellite-estimator test).**
- Done in Appendix E: pooled composites, retrieval-like Nd, 3.75 km aggregation and overcast filtering.
- Not done: reverse or orthogonal regression. Dipu et al. (2022) and Costa-Surós et al. (2020) are cited.

**A-M7 (cloud-top Nd as denominator).** Done throughout. S with the target CCN in the denominator is also computed and is close to the cloud-top values (`rev2_branch.csv`, S_target).

**A-M8 (transience, nocturnal, terminology).**
- "Susceptibility" is now used for S and "adjustment" is reserved for its radiative meaning.
- The time-dependence is a main result (Sect. 3.3).
- Gryspeerdt et al. (2021, 2022), Fons et al. (2023) and Sandu et al. (2008) are cited.
- Not done: a time-integrated S over 2–12 h. S(t) is shown instead.

**Minor comments**

| Comment | Response |
|---|---|
| m1 | Abstract distinguishes all-sky, in-cloud and cloud-cover parts. |
| m2 | Wording corrected per Forster et al. (2021). |
| m3 | Quaas et al. (2009) removed from the causal context; Jia et al. (2021) added. |
| m4 | The RF02 Nd and branch relevance are discussed in Sect. 3.2. |
| m5 | S_ic and S_c are defined in Sect. 2.4. |
| m6 | The clean-branch cover (0.68 at target 20) is emphasised. |
| m7 | The satellite comparison is softened, with the upper-bound caveat. |
| m8 | S_R added. |
| m9, m10 | Within-scene SD and filters are reported in Appendix E. |
| m11 | Dipu et al. (2022) and Costa-Surós et al. (2020) cited. |
| m12 | Sect. 4.2 now lists the GCM-like features of the coarse runs. |
| m13 | TOA longwave change: not done. |
| m14 | Table 5 now has S₅₅. |
| m15 | Fig. 4 has a zero line and bootstrap bars. |
| m16 | Fig. 3 uses cloud-top Nd. |
| m17 | Former conclusion 6 dropped. |
| m18 | Terminology defined in Sect. 2.4. |

## Reviewer B

**B-M1 (numerical entrainment).** Done (Sect. 3.1, Fig. 2e,f, Sect. 4.1).
- The flux budget at the inversion shows that explicit fluxes carry 37–46 % of the implied flux at ≤5 km, with no systematic trend with Δx.
- Inversion thickness is 2–3 levels and the cloud-top height spread is less than one level.
- The near-grid share of w variance is 60–74 % at 5 km.
- The quantity is defined as the "subsidence-corrected deepening rate" (Sect. 2.4), and the abstract states the fixed 50 m levels.
- The 5 km departure from the coarse solution after about 8 h is described.
- Not done: w spectra beyond the near-grid share, and time series of TKE at 10, 5 and 2.5 km.

**B-M2 (η and the jump definition).** Done (Fig. 8c).
- η is reported for offsets of 50, 100 and 150 m and for the interface jump, with η_obs under the same definitions (0.9–1.2 and 0.53–0.68).
- We agree with B's reading: the coarse runs entrain too little, and the fine runs lie at the upper end of the observed range.

**B-M3a (radiation and free troposphere).** Done (Sect. 2.2): FT θ_l drift −0.3 K at 2 km and ≤0.4 K at +300 m, identical across Δx; clear-sky cooling −2.6 K d⁻¹.

**B-M3b (surface fluxes are the protocol).** Corrected.

**B-M3c (winds).** Done; mixed-layer wind and inversion shear are reported, similar across Δx.

**B-M3d (Nd varies in cloud).** Cloud-top Nd is used as the abscissa, and the departure from the benchmark is stated.

**B-M3e (evaluation window).** Hour 10–12 LWP of the sub-km runs is given in the text. Not done: observed cloud-base height and cloud-base drizzle; we could not verify these values from accessible sources.

**B-M4 (312 m is not LES).** Stated explicitly in Sects. 3.1 and 4.1, with the mixing-length cap, the skewness sign and the efficiency. Not done: plotting against Δx/z_i, a comparison with the Honnert et al. (2011) partition function, and KE spectra.

**B-M5 (state dependence).** Done; central (Fig. 6). B's r ≈ 0.91 is reproduced as 0.92. The increase of S with s at 2.5/1.25 km is explained by movement along the regime curve. Not done: precipitation efficiency per unit LWP.

**B-M6 (transience and equilibrium).**
- Done: z_i,eq and 1/D; relaxation fits with steady-state S; the distinction between compensation and an absent sink (Sect. 4.1); the radiative translation.
- Not done: a prognostic mixed-layer integration with fixed η or A. The relaxation fits serve this purpose with fewer assumptions.

**B-M7 (2.5–5 km regime).** The 5 km circulations are diagnosed as near-grid-scale and late-onset. Sect. 4.1 states that the grey zone starts at about 5 km in EAMxx/SHOC and recommends specific remedies: scale-aware partitioning and inversion-consistent vertical resolution.

**B-M8 (economy).** Restructured as requested; the satellite section moved to an appendix and the decomposition caveats condensed (Appendix A).

**Minor comments**

| Comment | Response |
|---|---|
| m1 | Authorship deferred to the study leads. |
| m2 | Mixing length at coarse spacing explained in Appendix B. |
| m3 | Renamed. |
| m4 | Level spacing now stated as 50 m between 500 and 1200 m. |
| m5, m6 | z_i definition and quantisation discussed. Alternative definitions not tested. |
| m7 | Clear-sky cooling above z_i quoted. Cloud-base warming not shown. |
| m8 | DHARMA labelled as a single model. |
| m9 | "1.8 K warmer" sentence removed. |
| m10 | Inverted-V analogy softened. |
| m11 | Evaporated-fraction caveat on rain fraction added. |
| m12 | Coupling claim softened and quantified. |
| m13 | Resolved variance is relative to the domain mean (two snapshots); stated in Sect. 2.4. |
| m14 | Stevens & Bretherton (1999) and Stevens et al. (2005) cited. |
| m15 | q_t jump quoted; interface value not computed. |
| m16 | Unreferenced "few per cent" statement removed and replaced by twin noise. |
| m17 | Markers added to Fig. 3 and other figures. |
| m18 | η_obs added to Fig. 8c. |
| m19 | Four conclusions. |
| m20 | Terminology defined. |

## Reviewer C

We thank C for the scripts. We checked them before reuse and recomputed instead of copying:
- The 1 h smoothing inflates lag-1 autocorrelation.
- The peak location in layer Nd mixes in the drift in Nd.
- The relaxation fit regresses a derivative on the same smoothed series.
- The bootstrap is unpaired and truncated.

**C1 (S(t) as main result).** Done (Fig. 5a,b, from raw 15 min output with cloud-top Nd). Not done: a fit of S(t) = S∞(1 − e^{−t/τ}). We fit LWP(t) per run and derive steady-state S instead.

**C2 (phase space).**
- Done: the 312 m phase plane, relaxation τ = 4–7 h, LWP_eq 45–55 g m⁻², and steady-state S with a paired moving-block bootstrap.
- The "one hour of drift" argument was removed from the abstract and replaced by twin noise and steady-state values.
- The layer-Nd drift (about −3 % h⁻¹ at ≤625 m) is reported (Appendix B).

**C3 (time-dependent inverted V).**
- Done: peak location against time in cloud-top Nd. The peak leaves the top level after about 3 h at ≤1.25 km, 5 h at 2.5 km and 9 h at 5 km, and falls from about 200 to 80 cm⁻³ at 312 m between 5 and 12 h.
- Not used: the Hoffmann et al. (2024) Eq. (9) test. With S₁₀₀→₂₀₀ ≈ 0 it has little power.

**C4 (robustness).**
- Done: twins with our counts and values (SD of ΔS 0.007–0.010 and 0.002–0.004; 71 pairs).
- The common seed is documented (Sect. 2.1).
- The s-ordering of the polluted branch is used as an argument against noise.
- The coarse oscillation (1.5–2 h periods) is noted, together with the need for 2 h averages.

**C5 (LES comparison, citations).**
- The like-for-like timing with Chen et al. (2025) is used qualitatively. The "order of magnitude" statement was removed.
- Glassmeier et al. (2019) is no longer cited for the inverted V and is removed from the bibliography.
- The Hoffmann et al. (2020) venue is J. Atmos. Sci., as already in the bibliography.
- The co-variation with z_i is discussed through the regime analysis.
- Done: the albedo susceptibility (A10).
- Not done: conditioning S on z_i (A9) and the Hoffmann (2020) stability test (A11).

**C6 (24–48 h experiments).** Listed as future work.

**Minor comments**
- m2, m3: done.
- m4: replaced by twin noise.
- m5, m6: done.
- m7: drift reported.
- m8: count clarified (35 pairs at 312 m).
- m9: S(t) shown. The 40 km off panel was not added.
- m10: done.
- m11: Glassmeier & Feingold (2017) cited.
- m12: correspondence of S to k noted implicitly through Chen et al. (2025).
- m13: done.
- m14: not done.

## Reviewer D

**D1 (satellite section).** Redone in Appendix E.
- The within-scene Nd variance share is below 1 %, reproducing D's argument. Pooled, between-run and within-scene slopes are reported.
- Correlations and SD are given instead of extreme slopes.
- Caveats on updraft-independent activation and the time step are added.
- The former conclusion 6 and the caution in Sect. 4.3 were removed.

**D2 (satellite variables).** Done: in-cloud LWP and cloud cover with cloud-top Nd for all branches (Table 5, Fig. 4). D's in-cloud values are reproduced with the threshold cover. Method: S uses log domain means, as stated.

**D3 (retrieval).** Done (Appendix E): column-level adiabatic retrieval with standard filters, at native resolution and 3.75 km. The retrieval is about 2× the model value, and the pooled slope is diluted to 25–50 % of the between-run slope. Not done: synthetic retrieval errors and a MODIS-simulator diagnostic.

**D4 (interpretation).** Implemented in Sects. 3.2, 3.3 and 4.2:
- The inverted V is now described as a shape only.
- Natural experiments and LES are the primary comparison.
- A single fit over all levels is reported.
- State dependence is in Fig. 6.

**D5 (statistics).**
- Regression direction: the composite is regressed as E[ln LWP | ln Nd].
- The filters are stated, and overcast-only sampling is included.
- Uncertainty uses tile and twin estimates.
- Scale: 3.75 km aggregation was done; the 1 km aggregation was not.

**D6 (conclusion 6).** Dropped.

**Minor comments**

| Comment | Response |
|---|---|
| m1 | Operator definition given in Sect. 2.4. |
| m2 | Cloud-top Nd at fixed target is stated. |
| m3 | Optical-depth mask not done. |
| m4, m10 | Observed-slope comparisons softened. |
| m5 | Done. |
| m6, m11 | Not done. |
| m7 | Edge-Nd mechanism removed with the old Sect. 3.10. |
| m8, m9 | Figure replaced. |
| m12 | Abstract has no satellite sentence, as the analysis is in an appendix. |
| m13 | "Covariability" used consistently. |
| m14 | Cloud-top Nd is the abscissa. |
| m15 | Instantaneous S is shown in Fig. 5. |
| m16 | The "process-level targets" sentence removed. |

## Reviewer E

**E-M1a (no evaporation–entrainment in this model).** Stated in Sect. 2.1: Nd affects entrainment only through drizzle, sedimentation and r_e in radiation. The evaporation pathway is cited only as an LES mechanism absent here.

**E-M1b, c (drizzle–entrainment).** Done (Sect. 3.5, Fig. 8b): the autoconversion switch is split into a rain-sink part and a Δw_e part, and the term is renamed.

**E-M1d (sedimentation test).** Done: offline F_sed and the regression of Δw_e on ΔF_sed. Our V_m (1.0–1.2 cm s⁻¹ at target 1000) is larger than E's 5–7 mm s⁻¹ because we use the P3 μ–Nd relation. The coupling operates at ≤2.5 km and is absent at ≥10 km.

**E-M1e (context of the negative branch).** Comparisons with Hill et al. (2009), Hoffmann et al. (2025) and Chen et al. (2025) are now qualitative, because we could not verify the reviewer's numbers.

**E-M2a (grid-locked inversion).** Confirmed (z_i rises 45 m in 12 h at 40 km; w_e 3.6–3.9 mm s⁻¹ for Nd ≥ 100) and used in Sects. 3.1 and 4.2.

**E-M2b (5 km unlocking).** Confirmed (z_i 862 m at 8 h versus 857 m at 40 km, then rapid deepening) and described.

**E-M2c (efficiency, inversion structure).** Done (A, inversion thickness, cloud-top height spread). The optional 312 m simulation with fine vertical levels is listed as future work.

**E-M2d (η is not an efficiency).** The steady reference is given, and A is used as the efficiency.

**E-M3 (decoupling).** Done with four metrics (Fig. 10), using the inversion base as the top of the layer.

**E-M4 (budget validity).** Done (in-cloud budget, cloud-layer LCL, coupled windows only, split entrainment term). The 625/312 m thinning is no longer attributed.

**E-M5 (nocturnal).** Stated throughout. The diurnal-cycle literature (Zhang et al. 2024; Chen et al. 2024; Zhang & Zuidema 2019; Zhang & Feingold 2023) is cited. The optional 36 h diurnal set is listed as future work.

**E-M6 (312 m relative to LES).** Three regimes are named and the 312 m runs are stated not to approximate LES. The unsupported coupling claim was removed, and pockets of open cells (Stevens et al. 2005; Savic-Jovcic & Stevens 2008) are discussed in Appendix D.

**Minor comments**

| Comment | Response |
|---|---|
| m1 | High-Nd Δw_e(s) given in the text, not in the abstract. |
| m2 | Process order stated. |
| m3 | Rain-fraction caveat added. |
| m4 | Alternative z_i definition not tested. |
| m5 | Sign convention of Δq_t and Δθ_l given in the Fig. 10 caption. |
| m6 | Thresholds drawn. |
| m7 | Flux profiles not shown separately; metrics summarised instead. |
| m8 | F_rad quoted. |
| m9 | Done. |
| m10 | Low- and high-Nd Δw_e(s) separated. |
| m11 | Done. |
| m12 | Done. |
| m13 | Removed with the old Sect. 3.10. |
| m14 | Described in the text. |
| m15 | Done. |
| m16 | Prescribed fluxes stated in Sect. 2.2. |
| m17 | Done. |
| m18 | "Coupling" used. |

---

## Literature

Added; every DOI was verified against Crossref:

- Mülmenstädt et al. 2019; Gryspeerdt et al. 2016; Quaas et al. 2020
- Jia et al. 2019, 2021, 2022; Jia & Quaas 2023
- Dipu et al. 2022; Costa-Surós et al. 2020; McComiskey & Feingold 2012
- Terai et al. 2012; Platnick & Twomey 1994; Carslaw et al. 2013
- Gryspeerdt et al. 2021, 2022 (ACP) and 2022 (AMT); Fons et al. 2023
- Stevens & Bretherton 1999; Stevens, Moeng & Sullivan 1999; Matheou & Teixeira 2019
- Zhu et al. 2005; Jones et al. 2014; Seifert et al. 2015
- Honnert et al. 2011; Stevens et al. 2020; Schneider et al. 2017
- Chen et al. 2024, 2025; Glassmeier & Feingold 2017; Kokkola et al. 2025
- Zhang et al. 2024; Hoffmann et al. 2025; Zhang & Zuidema 2019; Zhang & Feingold 2023
- Stevens et al. 2005 (BAMS, pockets of open cells); Turton & Nicholls 1987; Savic-Jovcic & Stevens 2008

Not added: Grenier & Bretherton (2001), which E did not specify.

Removed from use: Glassmeier et al. (2019), which is no longer cited for the inverted V. Terai et al. (2020) and Sato et al. (2018) are still compared explicitly in Sect. 4.2. The bibliography now contains only cited entries.
