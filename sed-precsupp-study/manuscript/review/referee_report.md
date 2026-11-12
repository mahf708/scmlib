# Referee report

**Manuscript:** "Grid spacing decides which microphysical pathway controls the liquid water path response to droplet number in simulated drizzling stratocumulus" (Mahfouz and Mülmenstädt), submitted to *Atmospheric Chemistry and Physics*

**Recommendation:** Major revision

Line numbers refer to the LaTeX source `sedps_acp_manuscript.tex`. Numerical checks were made against `manuscript/tables/*.csv`, `key_numbers.txt` and `analysis_report5/`. Where I recomputed a number, the source file is named. I did not read any 3D model output.

---

## 1. Summary of the paper

The authors ran 288 doubly periodic DP-EAMxx (SCREAM) simulations of the DYCOMS-II RF02 nocturnal drizzling stratocumulus case, plus 70 sensitivity runs with "3D" turbulence switched on. Each simulation lasts 12 h under constant forcing. The matrix spans eight horizontal grid spacings (40 km to 312 m), six target droplet numbers (20–1000 cm⁻³) and three cloud-droplet sedimentation multipliers (0.5, 1, 2). The Nd dependence of KK2000 autoconversion is either kept (β = 1.79) or removed (β = 0, with the prefactor matched at Nd = 63 cm⁻³). The main claims are:

1. At 10–40 km, LWP increases monotonically with Nd (S₁₀₀→₂₀₀ ≈ 0.24–0.27), and all of this comes from precipitation suppression.
2. As the grid is refined, entrainment strengthens, clouds thin, rain production drops and most rain evaporates. The LWP maximum moves to Nd ≈ 100 cm⁻³ at 312 m, giving an inverted V whose high-Nd branch (S ≈ −0.04 to −0.05) is entrainment-driven and steepens with faster sedimentation.
3. A mixed-layer LWP budget (r = 0.88) attributes the change to entrainment efficiency (η = entrainment warming / radiative cooling rises above 1).
4. Nothing is converged at 312 m, and 3D turbulence makes no difference.
5. Cloud-top Nd gives the same susceptibilities as layer Nd, but within-scene LWP–Nd slopes are unrelated to the true susceptibility.

The authors conclude that in kilometre-scale GSRMs the LWP adjustment is "set by the grid rather than by the physics alone".

## 2. Overall assessment

The question matters, and the experimental matrix is large, carefully executed and unusually well documented: the scripts, tables and derived numbers are all available, which made this review possible. The resolution dependence of the LWP–Nd relationship in a single GSRM-class model is a useful and publishable result. The mechanism-denial idea of switching off the Nd dependence of autoconversion and scaling the droplet fall speed is sound in principle.

However, several of the paper's central causal claims are not supported by the analysis as it stands.

- **The factorial decomposition is pivot-dependent and ignores a large interaction term** (Major 1). The "suppression off" runs are heavily drizzling at high Nd, and the sedimentation sensitivity of S with suppression on is as large at 40 km as at 312 m. The statements that "precipitation suppression accounts for all of it" at coarse spacing and that sedimentation matters only at fine spacing therefore do not follow from the data.
- **The budget's r = 0.88 is a pooled statistic dominated by between-resolution variance** (Major 2). Within each sub-kilometre resolution, the budget has essentially no skill (r = 0.07–0.44, RMSE ≥ SD), and it cannot resolve the Nd dependence it is used to attribute. In addition, the zi tendency enters the budget by construction.
- **Model-specific causes are not ruled out** (Major 3–4). These include SHOC's explicit √(ΔxΔy) cap on the mixing length, the time step and radiation interval co-varying with Δx, an unexplained abrupt transition between 10 and 5 km, and prescribed surface fluxes. Any of these could make "the grid decides" a statement about this configuration of EAMxx rather than about grey-zone physics.
- **The simulations are not evaluated** against RF02 observations or the Ackerman et al. (2009) LES and Wyant et al. (2007) SCM intercomparisons (Major 5). Without that evaluation, the reader cannot judge which resolution, if any, is credible.
- **The fine-resolution results are small and transient** (Major 6). The negative high-Nd branch at 312 m corresponds to LWP differences of 2–4 g m⁻² (3–5 %) between runs that are each still losing 4–6 % h⁻¹, from a single realisation. The paper does not establish that their sign is robust.
- **There are more than 20 numerical and descriptive inconsistencies** between the text and the tables (Sect. 6). Most are minor, but several affect interpretation: the off-run LWP description, the drift of S₁₀₀→₂₀₀ in time, the "one to two orders of magnitude" claim, and the source of the negative S₂₀₀→₁₀₀₀ at 2.5–1.25 km.
- **The literature is mischaracterised in places** (Sect. 7), most importantly Mülmenstädt et al. (2024, ACP 24, 13633) and Ackerman et al. (2004). Directly relevant work is missing: Wyant et al. (2007), Boutle et al. (2014), Wang et al. (2003), Chen et al. (2014) and Ghan et al. (2016). The last two are already in the .bib file but are not cited.
- **The prose and the title overstate and simplify** (Sect. 8). The heavy use of bullets is not ACP style.

I think all of these problems can be fixed. Most of the extra simulations I request are cheap at 40 km and 2.5 km, and only a handful are needed at 312 m. The paper would then make a solid contribution. In its present form, the abstract, conclusions and title claim more than the evidence supports.

---

## 3. Major comments

### M1. The factorial decomposition (Sect. 2.5, Eq. 9, Sect. 3.4, Fig. 5) is not a clean attribution, and the coarse-resolution conclusion depends on the choice of pivot

**Problem.**

(a) *Pivot dependence.* In the "off" configuration the autoconversion rate equals the "on" rate at Nd = 63 cm⁻³ (L84). At Nd = 1000 the off runs therefore autoconvert (1000/63)^1.79 ≈ 140 times faster than the on runs. As a result, at coarse spacing every off run is drizzling. At 40 km and target 1000, surface precipitation is 23.9 W m⁻² (0.83 mm d⁻¹) off versus 0.29 W m⁻² on (`key_numbers.txt`, P_sfc_Wm2). S_off is thus a sensitivity evaluated in a strongly precipitating base state. The paper's own mechanism (Sect. 3.5: a large rain sink masks the entrainment pathway) predicts that S_off will be near zero in such a state, whatever SHOC's entrainment sensitivity is. The conclusion that "precipitation suppression accounts for the whole of S" at ≥10 km may therefore be partly an artefact of choosing 63 cm⁻³. At 312 m the off runs barely precipitate (0.01–0.17 mm d⁻¹), so the decomposition compares sedimentation effects in different precipitation regimes at the two ends of the resolution range.

(b) *Interaction term.* Eq. (9) applies the s-slope b fitted to the off runs to the on runs. The on runs have their own s-slope, and the two differ greatly (`decomposition.csv`, dS_dsed_on vs dS_dsed_off):

| Branch | Δx | dS/ds, off runs | dS/ds, on runs |
|---|---|---|---|
| S₁₀₀→₂₀₀ | 40 km | −0.013 | −0.095 |
| S₁₀₀→₂₀₀ | 20 km | −0.014 | −0.093 |
| S₁₀₀→₂₀₀ | 10 km | −0.018 | −0.084 |
| S₁₀₀→₂₀₀ | 2.5 km | +0.053 | +0.099 |
| S₁₀₀→₂₀₀ | 1.25 km | +0.046 | +0.100 |
| S₁₀₀→₂₀₀ | 312 m | −0.026 | −0.040 |

With suppression on, S₁₀₀→₂₀₀ at 40 km falls from 0.345 to 0.269 to 0.196 for s = 0.5, 1, 2. This sedimentation sensitivity is more than twice as large as at 312 m (−0.022, −0.050, −0.084). It contradicts L303 ("sedimentation and residual terms are each between −0.02 and −0.003" at ≥10 km), L407 ("SHOC's entrainment hardly responds to droplet sedimentation") and L417. In the coarse runs the sedimentation effect evidently acts through water removal and autoconversion rather than through entrainment (w_e varies by <1 mm s⁻¹). That is also a sedimentation pathway, and the decomposition hides it.

(c) *Sign at 2.5–1.25 km.* At 2.5 and 1.25 km, faster sedimentation makes S₁₀₀→₂₀₀ more *positive* (on: 0.087 to 0.231 and 0.057 to 0.200 for s = 0.5 to 2). The sedimentation term on that branch is positive (+0.053, +0.046). The general statement that "the falling branch steepens with faster sedimentation" (abstract L42, L303, L409, L446) holds only for S₂₀₀→₁₀₀₀ at ≤2.5 km and for S₁₀₀→₂₀₀ at 625–312 m.

(d) *Extrapolation to s = 0.* The residual a is an extrapolation of three points with one degree of freedom. The clean-branch S_off is strongly convex in s (−0.11, 0.00, 0.34 at 312 m). The fit RMS of "below 0.02" is not a meaningful linearity test with one residual degree of freedom.

(e) *Different denominators.* On and off runs at the same target have different diagnosed Nd (e.g. 266 vs 243 cm⁻³ at 40 km, target 200), so S_on and S_off are slopes over different ln Nd intervals.

**Why it matters.** Claims 1 and 2 of the abstract and conclusions rest on this decomposition.

**Fix.**
- Run s = 0 (no droplet sedimentation) directly rather than extrapolating. This is cheap at all resolutions.
- Repeat the off configuration with a different pivot (for example, matching at Nd = 200 or 1000, so that off runs at high Nd are non-precipitating), at least at 40 km, 2.5 km and 312 m, and show whether S_ps and S_sed are pivot-invariant.
- Better, use a 2 × 2 design that decouples the Nd seen by autoconversion from the Nd seen by sedimentation and radiation (Nd_auto ∈ {a, b} × Nd_sed/rad ∈ {a, b}). This gives partial derivatives about a common base state and makes the interaction term explicit.
- Report the interaction term (dS/ds on minus off) in Fig. 5, or as a fourth bar.
- Rewrite L303–305, L407–409, L417 and the abstract accordingly.

### M2. The mixed-layer budget is validated on the wrong statistic and is partly circular (Sect. 2.6, Sect. 3.6, App. B, Fig. 8, Fig. A1)

**Problem.**

(a) *Partly circular.* In `ml_budget.py`, w_e = (observed dz_i/dt) − w_s. The budget's dz_i/dt is therefore identical to the observed value by construction. Only dz_b/dt (from the mixed-layer LCL) and the LWP ∝ h² geometry are actually predicted. The "entrainment contribution" combines the observed deepening (+2w_e/h) with the computed effect of w_e on z_b. The separation of entrainment from subsidence also depends on w_s(z_i), which itself grows with z_i. The budget is a diagnostic decomposition and should not be presented as an independent closure.

(b) *Validated on the wrong statistic.* The quoted r = 0.88 (L42, L214, L447, App. B) pools all 1440 run-windows across resolutions, so it mainly reflects the large between-resolution and between-time variance. I recomputed the statistics by resolution from `ml_budget.csv` (3D turbulence off):

| Δx | r(pred, obs) for dLWP/dt | RMSE (g m⁻² h⁻¹) | SD(obs) (g m⁻² h⁻¹) | r for Nd anomalies, all windows | r for Nd anomalies, 10–12 h window |
|---|---|---|---|---|---|
| 40 km | 0.87 | 3.9 | 6.6 | 0.93 | 0.93 |
| 5 km | 0.90 | 5.1 | 11.2 | 0.89 | 0.85 |
| 2.5 km | 0.62 | 4.4 | 4.7 | 0.77 | −0.02 |
| 1.25 km | 0.38 | 4.8 | 4.9 | 0.57 | 0.08 |
| 625 m | 0.07 | 3.6 | 1.8 | 0.02 | 0.10 |
| 312 m | 0.44 | 2.7 | 2.2 | 0.51 | 0.57 |

"Nd anomalies" are deviations from the mean over the six Nd levels at fixed (Δx, s, suppression, window).

At exactly the resolutions where the paper attributes the Nd dependence to entrainment, the budget has little or no skill, and its RMSE exceeds the signal. At 625 m (Fig. 8c) the budget sum at high Nd is −5.5 to −5.7 % h⁻¹, while the simulated value is −1.9 % h⁻¹. The text discusses only 40 km and 312 m.

(c) *Nd dependence within the noise.* At 312 m the entrainment term varies from −28.5 to −31.7 % h⁻¹ for Nd ≥ 50 (non-monotonic: −28.5, −28.8, −27.1, −31.1, −31.7). The radiative term partly compensates (+20.9 to +23.7). The net Nd dependence of the budget sum (≈2 % h⁻¹) and of the simulated trend (−4.3 to −5.2 % h⁻¹, ≈1 % h⁻¹) is no larger than the budget error (RMSE ≈ 2.7 g m⁻² h⁻¹ ≈ 3.7 % h⁻¹). The statement that the Nd dependence at fine spacing "comes from the entrainment term" (L348, L447) is therefore not established.

(d) *Mixed-layer assumptions.* Mixed-layer theory is applied to layers the paper itself describes as decoupled (Δq_t up to 1.6 g kg⁻¹ at 5 km), and to coarse runs with q_t decreasing upward by 1.2–1.7 g kg⁻¹ and an unstable θ_l profile. LWP ∝ h² is applied to domain-mean LWP in scenes with cloud cover of 0.5–0.85.

**Fix.**
- Present the budget as a diagnostic decomposition.
- Report skill by resolution and, crucially, for the Nd contrasts that enter S. Show Fig. A1 by resolution, with Nd anomalies.
- Remove "reproduces the simulated LWP tendencies (correlation 0.88)" from the abstract, or qualify it.
- Close the budget for in-cloud LWP and cloud cover separately at sub-kilometre spacing.
- Consider a budget in which w_e is diagnosed independently, for example from the buoyancy-flux or flux-jump method of Stevens (2002), or from resolved plus SHOC fluxes at z_i. That would avoid the circularity.

### M3. Model-specific grid dependence is not separated from grey-zone physics

**Problem.** The title and abstract attribute the regime shift to "the grid" and to eddies "beginning to be resolved". Several explicit Δx-dependent ingredients are not discussed:

(a) *SHOC length-scale cap.* SHOC caps its mixing length at √(ΔxΔy) of the host column. In the EAMxx source (`shoc_check_length_scale_shoc_length_impl.hpp`) the limiter is `shoc_mix = min(sqrt(dx*dy), max(minlen, shoc_mix))`. With physics columns about 469 m apart at 312 m (about 940 m at 625 m), this limit is likely active in the upper boundary layer at the two finest grids. It directly reduces SHOC's eddy diffusivity and TKE. Part of the "collapse" of SHOC variance (L357) and of the resolved/subgrid repartition is therefore imposed by the closure rather than emerging from the dynamics. The authors should say which Δx (dynamics or physics) is passed, and show profiles of shoc_mix against √(ΔxΔy).

(b) *Time step and radiation interval.* The physics time step falls from 100 s to 15 s, and with radiation called every third step, the radiation interval falls from 300 s to 45 s. Both co-vary with Δx (Table 2). SHOC, P3 (autoconversion with qc^2.47, sedimentation sub-stepping) and the coupling between cloud-top radiative cooling and turbulence are all time-step sensitive.

(c) *Abrupt transition between 10 and 5 km.* The largest single change in nearly every quantity occurs between 10 and 5 km, where the resolved variance share is only 3–7 %:
- LWP falls from 312 to 218 g m⁻² at target 1000;
- cloud base rises from about 205 to 390 m;
- w_e jumps from about 4 to about 7.7 mm s⁻¹;
- η exceeds 1 at 5 km (1.07–1.25 for Nd ≥ 100), larger than at 2.5 or 1.25 km.

L357 says the partly resolved circulation "entrains more efficiently per unit variance". At 5 km, however, the circulation is barely resolved, and Fig. 1 shows stripe-like, roll-shaped structures with a wavelength of about 6 physics columns. That points to a numerical or dycore-scale circulation rather than resolved boundary-layer turbulence. The paper also never explains why 10 km differs from 20–40 km at high Nd (LWP 312 vs 342 g m⁻²; column LWP SD of 4–18 g m⁻² vs 0.2–4 g m⁻²), given that 10 km is described as part of the identical-column limit.

(d) *Mesoscale peak.* The "cell scale" at 5 km (48 km) is 6.4 physics-column spacings, and at 2.5 km (30 km) it is 8. These are close to the effective resolution of a spectral-element dycore, so the spectral peak at Δx ≥ 2.5 km is probably resolution-limited, not domain-limited (contrast L367, Fig. 9d, "domain-limited"). The radial spectrum is also quantised at 240/n km (48, 40, 34, 30, 27, 24, 22, 20, 18.5, 17, 16 km, …), which should be stated.

**Why it matters.** "The grid decides" is a claim about physics. If a large part of the effect is SHOC's explicit Δx dependence, the time step, or dycore-scale circulations, the result is specific to the model configuration. The GSRM implications (L415, L451) would then need to be framed accordingly.

**Fix.**
- Run Δt sensitivity at fixed Δx: for example, 2.5 km and 5 km with Δt = 15 s and radiation every step; 40 km with Δt = 15 s. Two Nd levels × s = 1 × on/off suffices.
- Run 312 m (and 625 m) with the √(ΔxΔy) cap removed or relaxed.
- Diagnose the 10 → 5 km transition and show 5 km snapshots of w.
- Discuss the effective resolution of the dycore when interpreting λ.

### M4. Prescribed surface fluxes, no Coriolis and no wind forcing exaggerate entrainment-driven thinning and the 12 h transient

**Problem.** Sensible and latent heat fluxes are fixed at 16 and 93 W m⁻² (L90). The paper's key quantitative statement is that entrainment drying (105–131 W m⁻²) exceeds the surface latent heat flux (93 W m⁻²) at 312 m. With interactive surface fluxes, a drier and warmer mixed layer would raise the latent heat flux and lower the sensible heat flux. This is a first-order negative feedback that the configuration removes. It directly affects the thinning rate (−4 to −6 % h⁻¹), the 12 h transience, and probably the size of the Nd-dependent signal.

Removing Coriolis and wind nudging (L93) also departs from the RF02 specification (Ackerman et al. 2009 prescribe geostrophic winds and f). Shear across the inversion therefore decays freely over 12 h, which changes shear-driven entrainment in a way that may depend on resolution.

**Fix.**
- Test interactive surface fluxes over a fixed SST for a subset of runs (for example, 40 km, 2.5 km and 312 m; Nd 100/200/1000; s = 1; on).
- At minimum, discuss both choices explicitly in Sect. 4.4 and quantify the expected surface-flux feedback from the mixed-layer equations already in hand.
- Justify running a nocturnal, constant-forcing case for 12 h. The standard RF02 protocol is 6 h.

### M5. No evaluation against observations or the RF02 intercomparisons

**Problem.** The paper shows that the solutions change dramatically with Δx: the 40 km and 312 m runs differ by a factor of 4 in LWP and 525 m in cloud base. It never asks which (if any) resembles RF02.

- Observed RF02 cloud base is about 450 m with the top near 795 m. Surface drizzle averaged about 0.35 mm d⁻¹ (Wyant et al. 2007), and the observed entrainment rate was about 6 mm s⁻¹ (Ackerman et al. 2009, and references therein).
- The 40 km runs have a fog-like cloud with its base at 120–250 m and an LWP of about 300 g m⁻².
- The 312 m runs deepen by 220 m in 12 h.

RF02 has a well-documented LES intercomparison (Ackerman et al. 2009, with Nd fixed at 55 cm⁻³) and an SCM intercomparison (Wyant et al. 2007) that directly addresses the "single-column limit" analysed here. Neither the SCM study nor its large inter-model LWP scatter is cited. The case was originally run for 6 h.

**Why it matters.** "Grid spacing decides" is meaningful only if we know whether the fine-resolution solution approaches a credible reference. Without this, a reader cannot tell whether finer grids are moving towards LES or away from it.

**Fix.** Add a table or figure comparing hours 2–6 at target Nd = 50 (diagnosed about 42–67 cm⁻³) with the observations and the LES ensemble range (z_i(t), z_b, LWP, w_e, cloud-base and surface precipitation, w variance profile), and cite and compare with Wyant et al. (2007) for the coarse runs. An LES of the same configuration (for example, SAM or DALES with KK2000 and the same Nd levels) would be the ideal "converged reference" called for in L419. At minimum, compare against the published ensembles.

### M6. Robustness of the small negative susceptibilities at 312 m (single realisation, transience, magnitude)

**Problem.** At 312 m, S₁₀₀→₂₀₀ = −0.05 corresponds to LWP 76.2 versus 73.6 g m⁻² (3.4 %), and S₂₀₀→₁₀₀₀ = −0.036 corresponds to 73.6 versus 69.6 g m⁻². Every run is losing 4–6 % h⁻¹ (`ml_budget.csv`), so these differences amount to less than one hour of drift. The time-sampling SD (L171) is computed with 15-min samples that are strongly autocorrelated and share one realisation. It is not a measure of the uncertainty of S. Domain-mean LWP spread across initial-condition ensembles in stratocumulus LES and CRMs is typically a few per cent, the same size as the signal. In S(t), S₁₀₀→₂₀₀ at 312 m is still decreasing at 12 h, and at 625 m and 1.25 km it is still *increasing* (Fig. 4b). The sign of S₁₀₀→₂₀₀ at fine spacing is therefore not settled even within this experiment.

**Fix.**
- Run small initial-condition ensembles (3–5 members with different perturbation seeds) for target Nd 100, 200 and 1000 at 312 m and 2.5 km, s = 1, on and off.
- Report S with ensemble confidence intervals.
- Show whether S(t) has levelled off. If not, extend a subset to 24 h.
- Rephrase the abstract and conclusions so that the negative branch is presented as a tendency in a transient, single-realisation experiment.

### M7. Definitions that are not consistent across resolutions

(a) *Cloud cover.* Defined as the fraction of columns with LWP > 10 g m⁻² (L157), cloud cover is identically 1.00 at Δx ≥ 10 km because the columns are nearly identical. SHOC's subgrid cloud fraction is ignored. The cloud-cover/in-cloud decomposition of S (L307) is therefore zero at coarse resolution by construction, and "cloud cover falls from 1.00 to 0.84" mixes a resolved quantity at fine Δx with an undefined one at coarse Δx. Use SHOC's cloud fraction (for example, the column maximum or total cloud with an overlap assumption) consistently, or combine resolved and subgrid.

(b) *Comparisons at fixed target Nd.* Diagnosed in-cloud Nd at a given target depends strongly on Δx: 29 vs 19 cm⁻³ at target 20, and 1353 vs 807 cm⁻³ at target 1000, for 40 km vs 312 m (`runs.csv`). Every cross-resolution comparison at "fixed target Nd" therefore compares different Nd. On the clean branch, with S ≈ 0.4–0.7 and ln(29/19) = 0.42, the Nd difference alone accounts for 20–30 % LWP differences. This affects Table 3, the PS gain (134 → 6 g m⁻²), the convergence percentages in Sect. 3.9, and Figs. 1 and 10. Interpolate to fixed diagnosed Nd in ln Nd for cross-resolution comparisons.

(c) *Diagnosed Nd above target.* Diagnosed Nd is 21–64 % *above* target at coarse resolution, and the layer median is about twice the cloud-top value (cloud-top/layer ratio 0.44–0.72). The explanation offered ("P3 depletes and replenishes Nd", L110) does not account for an excess. Please explain how SPA/P3 activation can produce Nd above the prescribed CCN, and why the in-cloud Nd profile is so non-uniform in the single-column limit. If this is an artefact (for example, activation at every step in SHOC-diagnosed cloudy layers near cloud base), it affects the interpretation of the coarse runs.

(d) *Entrainment rate.* w_e uses a 4 h fit (8–12 h, L161), but the budget uses 2 h fits, and all other quantities use 10–12 h. The 50 m vertical spacing and the quantisation of z_i should be discussed more carefully. The inversion rises by about 200 m (four levels) at 312 m, but by only about 70 m at 40 km.

(e) *"Surface rain"* includes the cloud-droplet sedimentation flux (L436). At 40 km the cloud base is at 120–250 m, and surface "precipitation" rises with s even when suppression is off (Nd 20: 0.78 → 1.27 mm d⁻¹ for s = 0.5 → 2). Droplet deposition at the surface may therefore be a direct water sink in the coarse runs, which may explain M1(b). Separate rain and cloud-droplet surface fluxes. They are available as separate P3 outputs or from the fluxes at the lowest level.

(f) *Resolved versus SHOC variance.* SHOC's w² is diagnosed from TKE, assuming isotropy, so it is not a prognostic second moment. The "resolved share" (Fig. 9a) compares unlike quantities, and the resolved w variance is computed on the physics grid. State this caveat.

### M8. Satellite-related section (Sect. 3.10, Sect. 4.3): conclusions are partly tautological or ill-posed

(a) *Not a retrieval.* The AeroCom-style "cloud-top Nd" is a model-diagnosed number concentration at cloud top. It is not a retrieval from τ and r_e under adiabatic assumptions (Grosvenor et al. 2018). Because the cloud-top/layer ratio is nearly constant with Nd at a given Δx, agreement in S follows almost by construction. "Sampling cloud tops does not by itself bias S" (L423) says nothing about retrieval bias. Either implement a MODIS-like retrieval (τ and r_e from the radiation code, then Nd from the adiabatic formula) or drop the "retrieval proxy" framing. Satellite studies also use in-cloud LWP over 1 km pixels, not domain-mean LWP.

(b) *Ill-posed regressions at coarse spacing.* At 10–40 km the columns are nearly identical (column LWP SD 0.2–18 g m⁻²; at 40 km, 0.2–2 g m⁻²). Regressions of ln LWP on ln Nd_top over these columns are ill-posed, yet they supply the extreme values quoted in the abstract and conclusions: "−16 to +3", where −15.9 is at 10 km, target 50. Restrict the within-scene analysis to Δx ≤ 5 km (better, ≤ 2.5 km). With only 2–3 points per decade of Nd, also report the slope's standard error, not only the mean over instants.

(c) *Discussion of confounding.* The observation that cloud-controlled Nd variability produces spurious spatial slopes is well established (Gryspeerdt et al. 2019; Mülmenstädt et al. 2024 ACP 24, 7331; Arola et al. 2022). The new element is the sign change with Δx, which follows from the dependence of drizzle and edge evaporation on resolution. That element deserves a short mechanistic explanation rather than a general statement.

### M9. Over-reach in the implications for GCMs and GSRMs (Sect. 4.2, abstract last sentence, conclusions L451)

(a) *The 40 km runs are not GCM columns.* They use Δt = 100 s, 50 m vertical spacing at the inversion and SHOC. No GCM uses this combination (typically Δt ≈ 30 min, about 100–200 m spacing at 1 km, CLUBB/UNICON/EDMF, and MG2 with subgrid-variance enhancement of autoconversion). Calling them "analogous to a GCM column using the same physics" (L236) and inferring that GCMs "would be expected to miss the negative pathway in the same way" (L417) is not justified.

(b) *Opposite finding in the cited work.* Mülmenstädt et al. (2024, ACP 24, 13633), cited at L417 as support, reached the opposite conclusion for E3SM single-column physics. They found that sedimentation-mediated entrainment is active: switching sedimentation off removes the LWP decrease, and doubling it makes the response more negative. They argued that GCM physics *can* represent the small-scale coupling. They also used a sedimentation-doubling experiment very similar to the present one. This needs to be discussed properly and credited as a methodological precedent.

(c) *One model.* The final sentence of the abstract generalises from one model with one turbulence closure to "Global storm-resolving models at kilometre scale". GSRMs with other closures (Smagorinsky–Lilly, scale-aware TKE schemes, blended schemes in the sense of Boutle et al. 2014) may behave quite differently. Restrict the claim to EAMxx/SHOC, or support it with discussion of other models.

---

## 4. Minor comments

1. **L42, abstract.** Rain production "falls by more than an order of magnitude" only at the higher Nd. At target 20 it falls from about 2.0 to 1.2 mm d⁻¹. Qualify with "at Nd = 200 cm⁻³".
2. **L42, abstract.** "entrainment strengthens [as the grid is refined]". w_e is non-monotonic: it peaks at 5 km and dips at 2.5–1.25 km (L378). Say so.
3. **L42, abstract.** "358 simulations" includes 70 runs used only in Appendix C. Say "288 simulations, plus 70 with 3D turbulence".
4. **L42, abstract.** The abstract runs to about 290 words and lists many numbers. Trim to about 200–250 words and keep three or four key numbers.
5. **L53.** \citet{bogenschutz2023rrm} is a regionally refined global configuration with enhanced vertical resolution, not a doubly periodic study. Reword: "Doubly periodic (Bogenschutz et al., 2023) and regionally refined (Bogenschutz et al., 2023b) configurations of SCREAM…".
6. **L70.** "which we confirmed in the model output" — state how (for example, P3 condensation/evaporation tendencies identically zero).
7. **L70.** Does P3 in this EAMxx version apply a subgrid cloud-water variance enhancement to autoconversion (as MG2 does)? If not, autoconversion at coarse resolution uses an in-cloud mean qc with no Jensen correction, while at 312 m resolved variability partly provides one. This is a resolution-dependent bias in rain production and is directly relevant to Sect. 3.5.
8. **L84.** 63 cm⁻³ is not "the geometric centre of the Nd range". The geometric centre of 20–1000 is 141 cm⁻³, and the geometric mean of the six levels is 147 cm⁻³; 63 is the centre of 20–200. The rates are also equal at a *diagnosed* Nd of 63, not a target of 63. Mention that RF02's observed Nd is about 55–65 cm⁻³, which may be the real motivation.
9. **L84.** "Switching suppression off… leaves rain itself… intact." It changes rain substantially in both directions (see M1). Show the autoconversion ratio off/on as a function of Nd.
10. **L106, L113.** Two 312 m runs with 3D turbulence on were still running. Complete them before submission, or remove the caveat.
11. **L108.** Table 2 lists Δt_dyn of 8.33 s at 5 km and 6.25 s at 2.5 km (Δt_phys/Δt_dyn = 12) but 2.50 s at 1.25 km (ratio 24). Explain or correct.
12. **L110.** Diagnosed Nd is computed from only two 3D snapshots (10 and 12 h). Is it stable in time? Compare with the 15-min cloud-top Nd.
13. **L157.** Defining z_b as the lowest level where domain-mean cloud fraction reaches half its maximum quantises z_b to 25–50 m levels. Combined with h ≈ 290 m at 312 m (about six levels), this limits the precision of h and of the LWP ∝ h² budget.
14. **L159–161.** State the sign convention for w_s (negative = downward).
15. **L171.** Explain why S is computed with time-varying LWP but fixed (snapshot) Nd.
16. **L224, App. D.** "13–20 km" (Sect. 3.1) and "15–20 km" (App. D) are inconsistent. `runs.csv` gives 12.6–18.5 km at 312 m and 15–21.8 km at 625 m.
17. **L228.** "small, bright drizzling cells" — bright in LWP, not necessarily in albedo (there is no shortwave radiation). Rephrase.
18. **L236.** 10 km does not behave like 20–40 km at high Nd (Table 3; LWP SD up to 18 g m⁻²). Do not group it with them in the "single-column limit", or explain the difference.
19. **L255.** "In these simulations, however, it emerges only once the boundary-layer eddies begin to be resolved." It emerges at 5 km, where the resolved share is 3–7 %. "Resolved" is too strong.
20. **L257.** The description of the off runs is wrong: see Sect. 6, item 1.
21. **L264.** "decreases monotonically with Δx" literally means it decreases as Δx increases. Write "decreases monotonically as Δx decreases".
22. **L292.** "This is consistent with the long adjustment time scales found in LES." Glassmeier et al. (2021) refers to non-precipitating clouds evolving over days. Be specific.
23. **L303 vs L305.** One sentence says faster sedimentation "raises LWP more in clean (large-droplet) clouds than in polluted ones"; the other says it "lowers LWP most at the lowest Nd". Both may hold over different Nd ranges, but as written they contradict each other. Specify the Nd ranges.
24. **L305.** The effective-radius range 10–17 μm spans all s and suppression settings. For s = 1 with suppression on it is 12.5–13.7 μm. Using r_e in a Stokes fall speed is a crude approximation; P3 uses the mass-weighted fall speed of a gamma distribution.
25. **L321.** "roughly doubles (Fig. 7c)" — give numbers (66.9 → 128.2 W m⁻² at target 200).
26. **L323.** The inverted-V mechanism in Wood (2007) and Hoffmann et al. (2020) is the cloud-thinning versus precipitation competition. Credit Ackerman et al. (2004), who first identified that the sign depends on the ratio of surface precipitation to entrainment drying. This is precisely the ratio in Fig. 6c.
27. **L332.** "(Table 3)" is cited for radiative cooling, but Table 3 contains only LWP. Point to `runs.csv` or add F_rad to a table.
28. **L336.** The fall-speed proxy uses cloud-top r_e from the AeroCom operator. Why not the P3 mass-weighted fall speed at cloud top, which is available from the state? The proxy and Fig. 7a mix all Nd, s and suppression settings, so the w_e decrease could be driven by Nd through radiation rather than by sedimentation. Show the partial dependence on s at fixed Nd.
29. **L357.** "SHOC's variance collapses" — see M3(a). Show the shoc_mix profile.
30. **L362.** The resolved skewness is positive at 312 m (0.09–0.24) but negative at 625 m (−0.32 to −0.72). Calling the finest boundary layer "structurally different again" without explanation is unsatisfying. Is the skewness computed on the physics or the dynamics grid, and over which levels? Positive skewness at the finest grid may indicate a numerical effect (for example, near-grid-scale updrafts), with a third of the variance still subgrid.
31. **L362.** Skewness at Δx ≥ 10 km comes from resolved variance of about 10⁻⁸ m² s⁻² (`runs.csv`, w2_res_bl) and is meaningless. Make sure it is not plotted, and say so.
32. **L367.** Wood and Hartmann (2006) report aspect ratios of up to about 30–40 for boundary layers about 1 km deep. The 13–20 at 312 m is on the low side, and the 2.5 km value (33) agrees better. "Within the range" is weak support. Discuss.
33. **L369.** "3D turbulence… is not a factor". It is fine to say the effect is small, but the test is weak: SHOC's horizontal diffusion is tiny relative to the dycore's hyperviscosity. Consider testing the hyperviscosity or sponge settings instead.
34. **L378.** "typical grey-zone signature" — cite an example (for example, Honnert et al. 2020; de Roode et al. 2019; Boutle et al. 2014).
35. **L415.** Terai et al. (2020) used an ultra-parameterised multiscale model (UPCAM, 250 m CRM versus 4 km), not a GSRM, and found a *weaker positive* LWP response, not a negative one. Correct the characterisation. This is the closest prior work to the present study, so compare with it explicitly.
36. **L429.** "The free troposphere of RF02 is relatively moist, so the negative pathway may be stronger in drier cases." This needs a reference or a number (q_t jump 6.4 g kg⁻¹).
37. **L432.** Also acknowledge that LES of RF02 used Δz ≈ 5 m near the inversion. Reference Bogenschutz et al. (2023b) for vertically enhanced physics. A test with refined vertical spacing (for example, 25 or 10 m near the inversion) at 312 m would be valuable.
38. **L434.** \citet{wood2006} (MCC spatial variability) is not a reference for aerosol processing. Replace it, for example with Wood et al. (2011) or Kazil et al. (2011) "Modeling chemical and aerosol processes in the transition from closed to open cells…" (verify the exact reference before citing).
39. **L435.** \citet{xue2006} (trade cumulus) and \citet{wang2009} (MCC and drizzle) are weak support for "droplet-size dependence of cloud-top evaporation contributes to the entrainment pathway". Add Wang, Wang and Feingold (2003) and Bretherton et al. (2007), and arguably Hoffmann and Feingold (2019).
40. **Sect. 4.4.** Add the time step, radiation-interval co-variation, prescribed surface fluxes, SHOC's Δx cap, and the absence of Coriolis as limitations (see M3 and M4).
41. **App. A.** The P3 diagnostic bug is a useful finding, but it belongs in a code issue or pull request and in one sentence of the Methods, not in an appendix of a science paper. Report the GitHub issue number or PR.
42. **Code and data availability.** ACP requires persistent identifiers (for example, Zenodo DOIs) for the code (the model branch and analysis scripts) and for the derived data. Personal GitHub branches are not sufficient.
43. **Placeholders and draft notes.** L2 ("DRAFT…"), L491 ("[Authors: add DOI.]"), L493 ("Both authors must review…[Authors: confirm or revise.]") and L498 ("[Authors: add funding statement…]") must be resolved. Check the AI-use statement against current Copernicus policy and keep it factual and brief.

---

## 5. Technical corrections

- **L19 (title).** See Sect. 8.
- **L51.** "This is precipitation suppression, which increases LWP" — rewrite as one sentence (Sect. 8).
- **L53.** "Simple Cloud-Resolving E3SM Atmosphere Model". Bogenschutz et al. (2023) uses "Simple Convection-Permitting E3SM Atmosphere Model" in its title; check the current official expansion and be consistent.
- **L106.** "Of these, 70 were complete at the time of writing" — not appropriate for a submitted manuscript.
- **L143.** "rain fraction set to one" — explain what this means in P3.
- **L157.** Write "LWP > 10 g m⁻²" consistently with the \gmm macro.
- **L240 (Fig. 1 caption).** Maps are at hour 12, but labels are 10–12 h means; state this more prominently. The "bone" colormap gives very little contrast in the 0–100 g m⁻² range, where all 312 m fields lie. Use a perceptually uniform map (for example, cividis or viridis) or a per-row colour scale.
- **L261 (Fig. 2).** The legend in panel (c) overlaps the 40/20/10 km curves. In panel (d) the 312 m "on" curve leaves the axes below 10⁻³. The viridis colours for 40/20/10 km cannot be told apart.
- **L270 (Fig. 3).** The x-axis is categorical. Note this, or use a log Δx axis. Error bars (temporal SD) are not uncertainties (M6).
- **L274 (Table 4).** Three decimals overstate the precision; use two. The final column header should say "target Nd at max LWP".
- **L311 (Fig. 5).** Add the interaction term (M1).
- **L340 (Fig. 7).** The legend in (a) covers data, and its markers do not match the plotted symbols. The panel label "(c)" collides with the y-axis label. Add a proxy-to-fall-speed conversion axis.
- **L352 (Fig. 8).** Add 5 km and 1.25 km, or a summary panel, and add error bars from the budget RMSE.
- **L373 (Fig. 9 caption).** "(dotted: Δx ≥ 10 km)" applies only to (c), since (b) has no dotted lines. Panel (d) is labelled "domain-limited"; see M3(d).
- **L398 (Fig. 11).** Panel (c) should exclude Δx ≥ 10 km (M8b).
- **L467 (Fig. A1).** The panel label "(c)" overlaps the y-axis label. Show it by resolution (M2).
- **L483 (Fig. A3).** Panels (b) and (c) have no legend, and the figure appears before the paragraph that cites it.
- **Throughout.** "inverted V" (L284, L292, L323, L409) versus "inverted-V" (L51, L255, abstract). Use the hyphen only as a compound adjective ("inverted-V shape"), consistently.
- **Throughout.** "target Nd", "Nd target" and in-cloud Nd are mixed. The S subscripts (S₂₀→₅₀ etc.) use target values while S is computed with diagnosed Nd. Define this once and keep to it.
- **Throughout.** "Sc-like and Cu-like" (L359): define Sc and Cu, or write them out.
- **Throughout.** "AeroCom-style" is undefined on first use (L152).
- **L161, L336, L378.** w_e is quoted from 8–12 h fits, but the budget uses 2 h fits. State this in Fig. 8.

---

## 6. Verified inconsistencies

Source files: `T` = `/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/tables/`; `A5` = `.../analysis_report5/`.

| # | Quoted value / statement | Location | Correct value | Source |
|---|---|---|---|---|
| 1 | Off runs: LWP "decreases slightly with Nd, except at 5 and 2.5 km where it first increases" | L257 | Off LWP increases from 20 to 50 cm⁻³ at 2.5 km (117→137), 1.25 km (116→127) and 625 m (103→109), and increases monotonically at 5 km (135→160). It is flat at 312 m (79→79). S₂₀→₅₀,off = 0.20 at 2.5 km, which is not "nearly independent". | T/key_numbers.txt (LWP, S_low) |
| 2 | "At Δx ≤ 1.25 km, S₁₀₀→₂₀₀ and S₂₀₀→₁₀₀₀ start near zero and drift negative" | L289 | S₁₀₀→₂₀₀ (on, s = 1) *increases*: 1.25 km 0.004→0.070; 625 m −0.002→0.028. Only 312 m drifts negative (0.004→−0.050). S₂₀₀→₁₀₀₀ does drift negative. | T/s_time.csv; key_numbers S_high(t) |
| 3 | S₂₀→₅₀ "sub-kilometre… 0.51–0.63 in hours 2–4" | L290 | Sub-km is 0.556–0.625; the value 0.513 is at 1.25 km | key_numbers S_low(t) |
| 4 | Rain/entrainment-drying ratio "falls by one to two orders of magnitude at fixed Nd" | L321 | Factor about 3.6 at Nd 20 (0.65→0.18); about 320 at 200 (0.143→4.5×10⁻⁴); about 280 at 1000. Range is 0.5–2.5 orders of magnitude. | key_numbers P_sfc_Wm2, F_ent_moist |
| 5 | Surface precip at 312 m "below 0.01 mm d⁻¹ for Nd ≥ 100" | L257 | 0.011 mm d⁻¹ at target 100; ≤ 0.002 mm d⁻¹ for ≥ 200 | T/runs.csv (precip_sfc) |
| 6 | Raining fraction "at most 0.1 % for Nd ≥ 200 at Δx ≤ 1.25 km" | L323 | 0.13 % at 1.25 km, target 200 | runs.csv (rain_frac) |
| 7 | SHOC BL variance at Δx ≥ 10 km "0.28–0.38 m² s⁻²" | L357 | 0.33–0.41 (on, s = 1); 0.28–0.41 including off | key_numbers w2_sgs_bl |
| 8 | 2.5–5 km S₁₀₀→₂₀₀ "about a third to two thirds of the 40 km value" | L415 | 0.111/0.269 = 0.41; 0.200/0.269 = 0.74, i.e. about 40–75 % | key_numbers S_high |
| 9 | "LWP decreases by 20–40 % with each halving below 1.25 km" | L415 | 12–23 % (1.25 km→625 m) and 23–39 % (625→312 m); 12–40 % overall | Table 3 / key_numbers |
| 10 | Pivot 63 cm⁻³ is "the geometric centre of the Nd range" | L84 | Geometric centre of 20–1000 is 141; geometric mean of the six levels is 147. 63 = √(20·200). | arithmetic |
| 11 | Cell scale "13–20 km at 625 and 312 m" (Sect. 3.1) vs "15–20 km" (App. D) | L224, L486 | λ_peak 12.6–18.5 km (312 m), 15.0–21.8 km (625 m) | runs.csv (lambda_peak) |
| 12 | "At 5 km the cells fill the domain (48 km is one fifth of the domain)" | L367 | Self-contradictory. 48 km is the n = 5 wavenumber, about 6.4 physics-column spacings, and probably resolution-limited | runs.csv; Table 2 |
| 13 | Negative S₂₀₀→₁₀₀₀ at fine spacing "comes from the sedimentation term… and from the residual" | L303 | True at 625 m and 312 m only. At 2.5 km and 1.25 km the sedimentation term is +0.008 and −0.005; the negative S comes from S_ps (−0.021, −0.018) and the residual (−0.014, −0.007) | T/decomposition.csv |
| 14 | At Δx ≥ 10 km, "sedimentation and residual terms are each between −0.02 and −0.003" (implying sedimentation is unimportant) | L303 | True for the off-derived b·s. With suppression on, dS₁₀₀→₂₀₀/ds = −0.084 to −0.095 at 10–40 km, more than twice the 312 m value (−0.040) | decomposition.csv (dS_dsed_on) |
| 15 | High-Nd branch "steepens with faster sedimentation" (general) | L42, L303, L446 | At 2.5 and 1.25 km, S₁₀₀→₂₀₀,on *increases* with s (0.087→0.231; 0.057→0.200) | key_numbers S_high |
| 16 | η "exceeds one at Δx ≤ 2.5 km for Nd ≳ 100–200"; entrainment strengthens with refinement | L336, L42 | At 5 km η = 1.07–1.25 for Nd ≥ 100, larger than at 2.5 km (0.86–1.08) and 1.25 km (0.96–1.07); w_e at 5 km (7.0–8.1 mm s⁻¹) exceeds 2.5 km (5.7–7.3) | key_numbers eta_ent, we_812 |
| 17 | Budget "reproduces simulated LWP tendencies (correlation 0.88)" | L42, L214, L447 | 0.877 pooled is correct, but per resolution r = 0.44 (312 m), 0.07 (625 m), 0.38 (1.25 km), 0.62 (2.5 km), with RMSE ≥ SD at sub-km. For Nd anomalies in the 10–12 h window: 0.57, 0.10, 0.08, −0.02 | T/ml_budget.csv (recomputed) |
| 18 | 312 m budget: radiative "+18 to +24 % h⁻¹" for Nd ≥ 50; entrainment "becomes more negative with increasing Nd" | L346 | Radiative +20.9 to +23.7 for Nd ≥ 50 (+17.9 only at Nd 20). Entrainment −28.5, −28.8, −27.1, −31.1, −31.7 (non-monotonic) | ml_budget.csv (t_end = 12, s = 1, on) |
| 19 | Within-scene slopes "−16 to +3" (abstract-level claim) | L389, L449 | Range is correct (−15.9 to +3.25), but the −15.9 extreme is at 10 km, where columns are nearly identical (column LWP SD 4 g m⁻²); at 20–40 km the SD is 0.2–4 g m⁻² | runs.csv (slope_scene, LWP_sd_offline) |
| 20 | S₁₀₀→₂₀₀ at Δx ≥ 10 km grows "from 0.12… to 0.27" | L288 | 0.12 → 0.24 (10 km), 0.27 (20, 40 km) | s_time.csv |
| 21 | Decoupling at Δx ≤ 5 km "decreases to 0.2–0.6 g kg⁻¹ at Nd = 1000" | L365 | 0.21–0.64 g kg⁻¹ (5 km value 0.64) | key_numbers dqt |
| 22 | Radiative cooling referenced to "(Table 3)" | L332 | Table 3 contains only LWP; F_rad is not tabulated | Table 3 |
| 23 | Fig. 9 caption: "(b)… and (c)… (dotted: Δx ≥ 10 km)" | L373 | Dotted lines appear only in (c) | fig09_structure.png |
| 24 | Intro: doubly periodic SCREAM studies "(bogenschutz2023, bogenschutz2023rrm)" | L53 | bogenschutz2023rrm is a global regionally refined, vertically enhanced configuration, not doubly periodic | bib entry / GMD 16, 335 |
| 25 | Δt_phys/Δt_dyn ratio | Table 2 | 12 at ≥ 2.5 km but 24 at ≤ 1.25 km (60/2.5 s) — please confirm | Table 2 |

**Values I checked and found correct:**
- 358/288/70 runs.
- S₁₀₀→₂₀₀ = 0.24–0.27 at 10–40 km.
- PS gain 134 → 6 g m⁻² at target 1000.
- LWP 135→342 g m⁻² at 40 km; 214 → 74 g m⁻² (5 km → 312 m, target 200).
- Cloud cover 0.84 and 0.50 at 312 m.
- z_i 863 → 1016 m, z_b 195 → 720 m, h 668 → 296 m.
- Mixed layer 1.8 K warmer.
- Diagnosed Nd 21–64 % above / 21 % below to 11 % above target.
- In-cloud Nd at max = 84 cm⁻³ at 312 m.
- S table values (Table 4).
- S_ps = 0.28–0.30 / 0.08–0.10; 0.12, 0.09, 0.09, 0.02.
- Clean-branch S_sed 0.13 and 0.30–0.34; residual −0.16 to −0.28; S_ps 0.54–0.73; S_off = −0.11, 0.00, 0.34; cloud-cover part 0.53/0.73.
- Rain production 0.55 → 0.03 mm d⁻¹; evaporated fraction 0.40 → 0.93.
- w_e 3.7/6.8/7.4/8.1 mm s⁻¹.
- η 0.45–0.67 and 1.23–1.27.
- Entrainment drying 105–131 and 55–78 W m⁻².
- Resolved shares (3–7 %, 4–9 %, 9–19 %, 28–38 %, 54–67 %).
- Skewness values.
- Convergence percentages (24 %, 36–40 %, 12–23 %, 10–18 %, 7–20 %, ratio 1.3–2.0).
- Cloud-top/layer Nd ratios (44–72 %, 77–95 %); max |S_top − S| (0.10, 0.04, 0.01).
- 3D-turbulence differences (−1.0 to +1.4 g m⁻², −0.005 to +0.007, −0.13 to +0.02 mm s⁻¹).
- Budget correlations (0.89, 0.87, 0.88); RMSE 4.2 vs SD 8.4; bias −1.1.
- 98 % of runs thinning, ≤ 4.4 g m⁻² h⁻¹, ≤ 6 % h⁻¹ (from `ml_budget.csv`; note that `A5/lwp_trend_h10-12.csv` gives "rel" values that appear to be per 2 h, so do not mix the two files).
- Mixed-layer warming of 0.07–0.10 K h⁻¹ at 312 m.

---

## 7. Literature issues

### 7.1 Mischaracterised or weakly supporting citations

1. **Ackerman et al. (2004, Nature 432, 1014)**, cited at L51 for "the sedimentation–entrainment feedback alone can make LWP decrease with Nd when the overlying air is dry". Ackerman et al. attribute the LWP response to a balance between moistening from reduced surface precipitation and drying from entrainment of overlying air. They do not isolate droplet sedimentation; Bretherton et al. (2007) did that later. Cite Ackerman et al. (2004) for the precipitation-versus-entrainment-drying balance and the humidity dependence. Credit them in Sect. 3.5, where the surface-rain to entrainment-drying ratio (Fig. 6c) is essentially their diagnostic.
2. **Mülmenstädt et al. (2024, ACP 24, 13633), "Can GCMs represent cloud LWP adjustments…"**, cited at L53 and L417 as evidence that GCM parameterisations fail to reproduce entrainment-driven adjustments. As noted in M9, that study found that both mechanisms are active in E3SM SCM physics. Sedimentation controls the negative response there (off removes it; doubling strengthens it). The authors concluded that GCM physics may be able to parameterise the coupling, and that the problem lies in the small global-mean effect and possibly in the LES and observational evidence. The present text implies the opposite. This needs correcting, especially since the second author is the lead author of that paper. The same paper is a direct precedent for the sedimentation-factor design and should be acknowledged in Sect. 2.1.
3. **Terai et al. (2020, JAMES)**, cited at L53 and L415 as a GSRM showing a weaker or negative adjustment. It is an ultra-parameterised multiscale model (UPCAM; CRM at 250 m versus a 4 km MMF), not a GSRM. It found a *weaker increase* in LWP, caused by weaker LWP increases in non-raining clouds and a smaller raining fraction. That result is strikingly similar to the present mechanism and deserves a direct comparison rather than a "cf.".
4. **Sato et al. (2018, Nat. Commun.)**. They attribute the LWP decrease in their global cloud-system-resolving model to explicitly simulated condensation and evaporation responses to aerosol. That is precisely the droplet-size-dependent evaporation pathway that is *absent* here (SHOC saturation adjustment, L70). Say so explicitly when comparing (L415). It strengthens the authors' caution, but the mechanisms differ.
5. **Toll et al. (2019, Nature)**, cited at L51. "Pollution tracks show LWP responses of both signs that are weak on average" is correct. "LWP decreases may therefore offset a substantial part of the Twomey effect" (citing Toll and Glassmeier) slightly overstates Toll et al., who emphasise a *weak* average decrease offsetting about 23 % of the Twomey cooling. Give the number.
6. **Gryspeerdt et al. (2019, ACP)**, cited at L51 and L255. The characterisation (inverted V; confounding; the observed negative slope as an upper bound) is broadly correct. At L255, "matches the shape seen in satellite composites" should note that Gryspeerdt et al. regard the observed negative branch as an upper bound on the causal effect (volcanic and ship-track slopes are much weaker, about −0.15 or less). A model-produced inverted V therefore does not validate the observed slope.
7. **Glassmeier et al. (2021, Science)**. Correctly cited for slow adjustment time scales and the ship-track overestimate. Note that their steady-state adjustment for non-precipitating Sc (about −0.6) is an order of magnitude more negative than S₂₀₀→₁₀₀₀ ≈ −0.04 here. This is worth discussing: the transience, the absence of evaporation–entrainment, or the model formulation may explain it.
8. **Bretherton et al. (2007, GRL)**. Correctly characterised.
9. **Wood and Hartmann (2006)**. Appropriate for cell scales (L164, L367), but not for aerosol processing (L434). See minor comment 32 on aspect ratios.
10. **Xue and Feingold (2006)** (trade cumulus) and **Wang and Feingold (2009)** (MCC and drizzle), cited at L435 for Sc cloud-top evaporation–entrainment. Weak support; see minor comment 39.
11. **Bogenschutz et al. (2023b, GMD)**, cited at L53 as a doubly periodic study. It is a regionally refined global study (Sect. 6, item 24).
12. **Karset et al. (2020, JGR)**. Appropriate (size-dependent evaporation and entrainment in a GCM).

### 7.2 Important missing references (all verified to exist)

- **Wyant, M. C., et al. (2007).** A single-column model intercomparison of a heavily drizzling stratocumulus-topped boundary layer. *J. Geophys. Res.*, 112, D24204, doi:10.1029/2007JD008536. This is the RF02 SCM intercomparison and is essential for the "single-column limit" discussion.
- **Boutle, I. A., Eyre, J. E. J., and Lock, A. P. (2014).** Seamless stratocumulus simulation across the turbulent gray zone. *Mon. Wea. Rev.*, 142, 1655–1668, doi:10.1175/MWR-D-13-00229.1. A direct precedent for stratocumulus in the grey zone, including scale-aware blending.
- **Wang, S., Wang, Q., and Feingold, G. (2003).** Turbulence, condensation, and liquid water transport in numerically simulated nonprecipitating stratocumulus clouds. *J. Atmos. Sci.*, 60, 262–278. On the Nd dependence of turbulence without drizzle, and on the limitations of saturation adjustment (directly relevant to L70 and L435).
- **Chen, Y.-C., et al. (2014).** Satellite-based estimate of global aerosol–cloud radiative forcing by marine warm clouds. *Nat. Geosci.*, 7, 643–646. The key observational study showing that the LWP response depends on precipitation state and free-tropospheric humidity. It is already in `sedps_refs.bib` but not cited.
- **Ghan, S., et al. (2016).** Challenges in constraining anthropogenic aerosol effects on cloud radiative forcing using present-day spatiotemporal variability. *PNAS*, 113, 5804–5811. Directly relevant to Sect. 3.10 and Sect. 4.3. Already in the .bib file but not cited.
- **Stevens, B., et al. (2005)** is cited, but the RF02 entrainment literature (**Stevens et al. 2003, QJRMS 129, 3469, "On entrainment rates in nocturnal marine stratocumulus"**) is in the .bib file and not cited. Use it for the observed entrainment rates.
- **For grey-zone boundary layers:** also consider Beare (2014, BLM, "A length scale defining partially-resolved boundary-layer turbulence simulations") and Efstathiou and Beare (2015, QJRMS). Verify the exact citations before adding.
- **For MMF/CRM resolution dependence of aerosol effects:** Wang, M., et al. (2011, ACP, "Aerosol indirect effects in a multi-scale aerosol-climate model PNNL-MMF") (verify before adding).

The .bib file also contains other unused entries (bryan2003, christensen2022, feingold2010, lu2005, matheou2011, mulmenstadt2021, seifert2015, wood2005). Either cite them where relevant or remove them.

---

## 8. Style and writing

The scientific writing is clear in places, but much of the manuscript reads like a briefing note rather than an ACP paper. It relies heavily on bullet lists (53 `\item`s), bold run-in paragraph headings (13 `\paragraph`s), short declarative "reveal" sentences, contrastive "not X but Y" and "neither X nor Y" framings, and summarising aphorisms. ACP papers are normally continuous prose with subsections, measured claims and few rhetorical devices. Specific passages follow, with plain rewrites.

### 8.1 Title

The current title is "Grid spacing decides which microphysical pathway controls the liquid water path response to droplet number in simulated drizzling stratocumulus". It has three problems.

- "Decides" is anthropomorphic and asserts a causal claim (grid as cause) that the paper has not isolated from time step and closure effects (M3).
- "Microphysical pathway" is inaccurate, because the entrainment pathway is not microphysical.
- The title does not name the model or the configuration, which ACP readers expect for a single-model study.

Alternatives in conventional ACP style:

- "Horizontal resolution dependence of the liquid water path response to droplet number in doubly periodic EAMxx simulations of drizzling stratocumulus"
- "Sensitivity of stratocumulus liquid water path adjustments to horizontal grid spacing from 40 km to 312 m in DP-EAMxx"
- "Precipitation suppression and sedimentation–entrainment pathways across the turbulence grey zone: liquid water path adjustments in simulations of DYCOMS-II RF02"

The running title (L28) is fine.

### 8.2 Section headings

- L314, "Why precipitation suppression loses its leverage" → "Resolution dependence of the precipitation sink".
- L405, "A grid-controlled regime shift" → "Resolution dependence of the dominant adjustment pathway".
- L284, "Transient development of the inverted V" → "Temporal evolution of the susceptibility".
- L448 (conclusion item heading), "The clean branch is robust; bulk quantities are not converged" → avoid "robust" (S₂₀→₅₀ varies from 0.56 to 0.97 with s at 312 m, and from 0.17 to 0.74 over time at 2.5 km). Suggested: "Clean-branch susceptibility varies less with grid spacing than bulk quantities".

### 8.3 Specific passages (quote → suggested rewrite)

1. **L42, abstract, last sentence.** "Global storm-resolving models at kilometre scale therefore sit in a regime where the sign and magnitude of the LWP adjustment are set by the grid rather than by the physics alone."
   → "At kilometre-scale grid spacings typical of global storm-resolving models, the sign and magnitude of the simulated LWP adjustment in EAMxx depend on the grid spacing."
   (This removes the "not X but Y" framing and restricts the claim to the model studied.)
2. **L42.** "…whose high-Nd branch (S = −0.04 to −0.05 at 312 m) is entrainment-driven, persists without precipitation suppression and steepens with faster sedimentation." This is a rhetorical triplet, and the claim is over-stated (M1, M2).
   → "At 312 m the high-Nd branch (S = −0.04 to −0.05) is also present with precipitation suppression switched off, and its slope increases with the sedimentation factor."
3. **L51.** "Smaller droplets coalesce less efficiently, so drizzle is suppressed and liquid water is retained. This is precipitation suppression, which increases LWP (Albrecht, 1989)."
   → "Smaller droplets coalesce less efficiently, which suppresses drizzle and tends to increase LWP (precipitation suppression; Albrecht, 1989)."
4. **L55.** "How the balance of adjustment pathways changes across this range of grid spacings has not been isolated. The answer matters for…"
   → "To our knowledge, the change in the balance between adjustment pathways across this range of grid spacings has not been quantified. Such a quantification is needed to interpret…"
5. **L62.** "This lets us separate the two pathways directly, in the spirit of mechanism-denial experiments."
   → "This mechanism-denial approach allows the two pathways to be separated."
6. **L222.** "Three changes stand out as the grid is refined." followed by bullets (colon-then-reveal).
   → "As the grid is refined, the cells become smaller (…), the domain-mean LWP decreases (…), and clear gaps appear (…)." Write it as one paragraph.
7. **L236.** "They are the "single-column" limit of the model, analogous to a GCM column using the same physics."
   → "These runs approximate a single-column configuration of the model physics." (Drop the GCM analogy; see M9.)
8. **L255.** "Figure 2 and Table 3 show the central result."
   → "Figure 2 and Table 3 show the LWP response to Nd."
9. **L255.** "In these simulations, however, it emerges only once the boundary-layer eddies begin to be resolved."
   → "In these simulations it appears only at Δx ≤ 5 km."
10. **L303.** "Faster droplet sedimentation thus raises LWP more in clean (large-droplet) clouds than in polluted ones, so the entrainment-driven falling branch steepens with s (Fig. 3c), as proposed by Bretherton et al. (2007)."
    → "On this branch, a larger sedimentation factor increases LWP more at Nd = 200 than at Nd = 1000 cm⁻³, so S₂₀₀→₁₀₀₀ becomes more negative with s (Fig. 3c), consistent with the mechanism of Bretherton et al. (2007)."
11. **L305.** "Droplet sedimentation then acts as a water sink akin to drizzle rather than as a brake on entrainment" — metaphor plus "rather than".
    → "At these large droplet sizes, sedimentation mainly removes cloud water, as drizzle does, and its effect on entrainment is secondary."
12. **L316.** "Precipitation suppression can raise LWP only to the extent that precipitation is a significant sink of boundary-layer water. Figure 6 shows that this sink shrinks as the grid is refined, for three reasons." followed by an italicised enumerated list.
    → Rewrite as prose: "The effect of precipitation suppression on LWP is limited by the size of the precipitation sink. Figure 6 shows that this sink decreases with grid spacing because rain production decreases in the thinner clouds, a larger fraction of the rain evaporates below cloud base, and entrainment drying increases."
13. **L323.** "With almost no rain left to suppress, the precipitation-suppression pathway has nothing to act on, and the falling branch set by entrainment is exposed. … Here, however, the location of its turning point is set by the grid."
    → "When surface precipitation is negligible, precipitation suppression has little effect on LWP, and the decrease of LWP with Nd associated with entrainment dominates (Ackerman et al., 2004; Wood, 2007; Hoffmann et al., 2020). In these simulations the Nd at which this transition occurs depends on grid spacing."
14. **L348.** "The resolution dependence of the LWP response is therefore, at root, a resolution dependence of entrainment efficiency."
    → "The budget suggests that the resolution dependence of the LWP response is associated mainly with the resolution dependence of entrainment." (Also hedge, per M2.)
15. **L357.** "Even at 312 m, a third of the variance is still subgrid." → Fine as content, but merge it into the preceding sentence.
16. **L369.** "It is not a factor in the results above."
    → "The 3D turbulence option therefore has a negligible effect on the results."
17. **L378.** "We stress, however, that the sign of S₁₀₀→₂₀₀ at 312 m could still change with further refinement…"
    → "The sign of S₁₀₀→₂₀₀ at 312 m may change with further refinement…"
18. **L407.** "That is the classic Albrecht (1989) picture, and broadly the behaviour of GCMs."
    → "This behaviour corresponds to the precipitation-suppression mechanism of Albrecht (1989) and resembles that of many GCMs (…)."
19. **L409.** "As the boundary-layer eddies begin to be resolved, two things happen together. First, … Second, … The first effect removes the leverage of precipitation suppression; the second supplies a negative entrainment pathway. The two effects together move the turning point…"
    → "At finer grid spacing, entrainment increases (η > 1), and the boundary layer warms, dries and deepens. The cloud thins and its base rises, so that rain production decreases and more of the rain evaporates. In addition, w_e becomes more sensitive to droplet sedimentation (Fig. 7a). Together these changes shift the LWP maximum from Nd ≥ 1000 to about 100 cm⁻³."
20. **L411.** "Our contribution is to show that, in a model that spans the grey zone, the competition is tilted by the grid itself."
    → "In EAMxx, the balance between these time scales depends on horizontal grid spacing across the grey zone."
21. **L415.** "The 2.5 km susceptibility is thus neither the GCM-like answer nor the sub-kilometre answer."
    → "At 2.5 km, S₁₀₀→₂₀₀ lies between the values obtained at 40 km and at 312 m."
22. **L423.** "Sampling cloud tops does not by itself bias S here." — reveal style, and over-reaching (M8).
    → "In these simulations, using cloud-top instead of layer-mean Nd changes S by at most 0.1."
23. **L446.** "It is entrainment-driven." — a stand-alone punch sentence and an over-claim.
    → Merge and hedge: "…and becomes steeper with faster droplet sedimentation, consistent with a sedimentation–entrainment feedback."
24. **L451.** "Interpreting GSRM aerosol forcing will require grey-zone-aware turbulence closures or explicit convergence tests in LES-like configurations."
    → "These results suggest that estimates of aerosol–cloud adjustments from GSRMs should be accompanied by resolution-sensitivity tests, and they motivate grey-zone-aware turbulence closures."

### 8.4 Structural style issues

- **Bullets.** Bullet and enumerated lists appear in Sects. 2.2, 2.3, 2.6, 3.1 (twice), 3.3, 3.5, 3.6 (budget), 3.7 (skewness), 3.8 and the conclusions. Apart from the conclusions (where ACP tolerates a numbered list) and possibly the factor list in Sect. 2.3 (which duplicates Table 1 and can be deleted), convert them to prose.
- **Bold run-in headings.** The `\paragraph{}` headings ("Moderate and polluted branches.", "Clean branch.", "Cloud cover.", "Entrainment rates and efficiency.", "LWP budget.", "Resolved and parameterised variance.", "Sc-like and Cu-like regimes.", "Decoupling.", "Cell scale.", "3D turbulence.") fragment the Results. Use `\subsubsection` sparingly, or plain paragraphs with topic sentences.
- **Italic run-ins.** Italicised run-ins inside list items ("*Thinner clouds produce less rain.*", "*At 40 km*", "*Single case and forcing.*") add a third level of emphasis. Remove them, except perhaps in the Limitations list.
- **Signposting.** There is a lot of over-signposting ("Figure X shows the central result", "The following limitations bear on how far the results generalise", "The main conclusions are as follows").
- **Tense.** Methods and results are mostly in the past/present mix that ACP accepts. Make sure results describing the simulations use one tense consistently (present tense for what figures show).
- **Precision.** Many quoted numbers carry three significant figures (for example, Table 4 to three decimals, "1.23–1.27") that exceed their precision given M6. Round to two.
- **Units and notation.**
  - Use "cm⁻³" consistently.
  - "g m⁻² h⁻¹" and "% h⁻¹" are fine.
  - "mm d⁻¹" versus "mm day⁻¹" in figure labels: Fig. 2d uses "mm d⁻¹", which is consistent.
  - The KK2000 equation (Eq. 1) should state the units (kg kg⁻¹ s⁻¹ with q_c in kg kg⁻¹).
  - "w_s" sign convention (see minor comment 14).
  - "S" is used both as a generic susceptibility and in S_ps, S_on and S_off without a hat or other distinction. That is acceptable but should be defined once in a short notation paragraph.
- **LaTeX and Copernicus conventions.**
  - The comment on L2 must be removed.
  - `\paragraph` is permitted, but Copernicus typesetting renders it as bold run-in text, which looks unusual in ACP.
  - Table 4 uses `$0.393$\,(0.007)`; use `0.39 (0.01)`.
  - The figure files contain panel titles; Copernicus prefers information in captions, though titles are acceptable.
  - Make sure every figure uses the same font size (Figs. 6 and 7 have small legend text at the printed width).
  - Fig. A3 is placed before its first reference.
  - The `\noappendix` placement is correct.
  - In the bibliography, check that the Copernicus style renders "Mülmenstädt" correctly. It does in the .bbl.
  - Make sure the code/data section uses `\codedataavailability` correctly with persistent DOIs.
- **Abbreviations.** "AeroCom-style", "SPA", "pg2", "IOP", "Sc", "Cu" and "RF02" should be defined at first use. SPA is used at L70 before it is explained.

---

## 9. Summary of requested additional work (in priority order)

1. Run s = 0, and run the off configuration with a different pivot (or a 2 × 2 Nd_auto × Nd_sed design) at 40 km, 2.5 km and 312 m. Report interaction terms (M1).
2. Validate the budget by resolution and on Nd contrasts. Reframe it as diagnostic. Remove or qualify the r = 0.88 claim (M2).
3. Run Δt and radiation-interval tests at fixed Δx; test the SHOC √(ΔxΔy) cap at 312/625 m; diagnose the 10 → 5 km transition (M3).
4. Run an interactive-surface-flux subset, or provide a quantitative discussion (M4).
5. Compare with RF02 observations, the LES intercomparison (Ackerman et al. 2009) and the SCM intercomparison (Wyant et al. 2007) (M5).
6. Run small initial-condition ensembles at 312 m and 2.5 km; show S(t) to steady state, or limit the claims accordingly (M6).
7. Use consistent definitions across resolutions (cloud fraction, comparisons at matched Nd, separating rain from droplet deposition) (M7).
8. Revise the satellite section (M8) and the GCM/GSRM implications (M9).
9. Correct all items in Sect. 6 and the literature issues in Sect. 7; rewrite in conventional ACP prose (Sect. 8).
