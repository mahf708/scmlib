# Referee report: Reviewer A (perspective informed by the published work of J. Quaas)

> **Disclaimer:** This is an AI-simulated review written for internal pre-submission use. It is not written by Johannes Quaas and does not represent his opinions. Its emphases are modelled on themes in his published work. Copernicus journals prohibit AI-generated referee reports, so this text must not be submitted to ACP as a review.

**Manuscript:** "Horizontal resolution dependence of the liquid water path response to droplet number in doubly periodic EAMxx simulations of drizzling stratocumulus" (LaTeX source `scmlib/sed-precsupp-study/manuscript/sedps_acp_manuscript.tex`, compiled PDF of 11 Nov 2026)

**Journal:** Atmospheric Chemistry and Physics

**Recommendation:** Major revision on scientific grounds. One editorial issue must be resolved before the manuscript can be submitted at all (Sect. 0).

**What I read:** the LaTeX source and figures, and the tables in `dp_screamxx_sedps_12h/manuscript/tables/` (`runs.csv`, `susceptibility.csv`, `cloudcover_3d.csv`, `matched_nd.csv` and others). I also read the previous referee report and the authors' response. That referee covered in depth:

- the pivot dependence of the factorial decomposition;
- the circularity of the mixed-layer budget;
- the SHOC mixing-length cap and time-step co-variation;
- the prescribed surface fluxes;
- the evaluation against observations;
- many numerical inconsistencies.

I do not repeat those points. Here I concentrate on four things:

- what the results mean for aerosol effective radiative forcing (ERF);
- how they bear on the interpretation of satellite LWP–N_d relationships;
- the statistics and the causal framing;
- what is still missing for ACP.

**Reviewer calculations:** the few numbers I computed myself come from the existing tables or the `fields/*.npz` files. They are labelled as reviewer calculations.

**Background work by J. Quaas and co-authors that shaped the emphases of this review (all verified):**

1. Quaas, J., et al. (2009). Aerosol indirect effects – general circulation model intercomparison and evaluation with satellite data. *ACP*, 9, 8697–8717. https://doi.org/10.5194/acp-9-8697-2009
2. Gryspeerdt, E., Quaas, J., and Bellouin, N. (2016). Constraining the aerosol influence on cloud fraction. *JGR Atmos.*, 121, 3566–3583. https://doi.org/10.1002/2015JD023744
3. Mülmenstädt, J., Gryspeerdt, E., Salzmann, M., Ma, P.-L., Dipu, S., and Quaas, J. (2019). Separating radiative forcing by aerosol–cloud interactions and rapid cloud adjustments in the ECHAM–HAMMOZ aerosol–climate model using the method of partial radiative perturbations. *ACP*, 19, 15415–15429. https://doi.org/10.5194/acp-19-15415-2019
4. Quaas, J., et al. (2020). Constraining the Twomey effect from satellite observations: issues and perspectives. *ACP*, 20, 15079–15099. https://doi.org/10.5194/acp-20-15079-2020
5. Jia, H., Ma, X., Yu, F., and Quaas, J. (2021). Significant underestimation of radiative forcing by aerosol–cloud interactions derived from satellite-based methods. *Nat. Commun.*, 12, 3649. https://doi.org/10.1038/s41467-021-23888-1
6. Dipu, S., Schwarz, M., Ekman, A. M. L., Gryspeerdt, E., Goren, T., Sourdeval, O., Mülmenstädt, J., and Quaas, J. (2022). Exploring satellite-derived relationships between cloud droplet number concentration and liquid water path using a large-domain large-eddy simulation. *Tellus B*, 74, 176–188. https://doi.org/10.16993/tellusb.27
7. Also: Costa-Surós et al. (2020, *ACP*, 20, 5657; https://doi.org/10.5194/acp-20-5657-2020) and Jia and Quaas (2023, *Nat. Clim. Change*, 13, 943; https://doi.org/10.1038/s41558-023-01775-5). Gryspeerdt et al. (2019), Bellouin et al. (2020), Mülmenstädt et al. (2020; 2024, GCM paper), Arola et al. (2022), Grosvenor et al. (2018) and Toll et al. (2019) are co-authored by Quaas and are already cited in the manuscript.

---

## 0. Editorial matter that precedes the scientific assessment

**Authorship and ACP's AI policy.** The manuscript lists an AI system as its sole author. The author-contribution statement says that the AI "designed and carried out the analysis and wrote the manuscript", and that "human review of the manuscript is pending".

The ACP AI policy (https://www.atmospheric-chemistry-and-physics.net/policies/ai_policy.html) states that "Generative AI must not be used for text or interpretations". It requires any generative use to be declared. COPE, whose guidance Copernicus follows, holds that AI tools cannot be authors because they cannot take responsibility for the work.

In its present form the manuscript is therefore not submittable to ACP, and an editor would return it without review. Before submission:

- the human investigators must take authorship and responsibility;
- they must rewrite or substantively own the text and the interpretation;
- the AI use must be declared as the policy requires.

**Code and data availability.** "Model output and the derived tables are available from the corresponding contact on request" is not adequate for ACP. The data policy expects persistent identifiers. A Zenodo archive is needed for:

- the model branch;
- the analysis scripts;
- the derived tables (`tables/*.csv` and the `fields/*.npz` reductions, which are small).

---

## 1. Summary

The authors ran a 288-member factorial set of doubly periodic EAMxx (SCREAM) simulations of the nocturnal, drizzling DYCOMS-II RF02 stratocumulus for 12 h. The factors are:

- eight horizontal grid spacings (40 km to 312 m);
- six target N_d (20–1000 cm⁻³);
- three cloud-droplet sedimentation factors (0.5, 1, 2);
- KK2000 autoconversion with or without its N_d dependence.

The main findings are as follows.

- At ≥10 km the configuration behaves like single-column physics, and the domain-mean LWP increases monotonically with N_d (S₁₀₀→₂₀₀ ≈ 0.24–0.27). This response disappears without the N_d dependence of autoconversion.
- As the grid is refined, entrainment strengthens, clouds thin and rise, and the precipitation sink collapses. The LWP maximum moves to about 100 cm⁻³ at 312 m, with a weak negative high-N_d branch (S ≈ −0.04 to −0.05) that steepens with faster sedimentation.
- The clean-branch susceptibility increases from 0.39 to 0.65–0.76.
- Nothing converges, and the turbulence scheme is grid-limited at 312 m.
- Within-scene LWP–N_d slopes with uniform aerosol range from −7.9 to +3.4, and their sign changes with grid spacing.

The revised manuscript is careful, honest about its limitations and much improved over the version seen by the first referee. The experiment is a useful addition to the literature. To my knowledge it is the first systematic factorial study of how the processes behind the LWP adjustment change across the turbulence grey zone within one model. That makes it relevant to the debate on whether kilometre-scale models will narrow the ERFaci uncertainty.

The paper still falls short of its stated motivation, which is to inform aerosol ERF and the interpretation of satellite constraints. It never translates its results into the quantity the ERF community uses: the radiative effect of the adjustment relative to the Twomey effect, separated into LWP and cloud-fraction (CF) margins. The headline also emphasises the part of the result that is least robust and least relevant to ERF: the sign of S at high N_d and at 312 m, and the location of the LWP maximum. The part that is both robust and ERF-relevant gets little attention: the large increase of the clean-branch response at fine grid spacing, which is dominated by a cloud-fraction adjustment that the coarse configuration cannot produce by construction.

All of my requests can be met with the existing output.

## 2. Recommendation and justification

**Major revision.** The simulations and the attribution design are sound enough for ACP, given the caveats the authors now state. The revision needs reframing and additional analysis, not new runs. In order of importance, the authors should:

1. express the response in radiative terms, separating the Twomey, LWP and CF contributions (M1, M3);
2. move the emphasis to the N_d range that matters for anthropogenic forcing (M2);
3. test whether the "resolution dependence" is a mean-state (regime) dependence (M4);
4. use the spatial dimension and the factorial structure to say which signs are robust (M5);
5. turn the satellite section into a test of how well a satellite-style analysis of these simulations would recover the causal response (M6).

Without these, the paper is a careful process study whose stated relevance to ERF and to satellite constraints is asserted rather than shown.

---

## 3. Major comments

### M1. The paper never translates the LWP susceptibility into an ERF-relevant quantity, and "the sign of the LWP adjustment" is not "the sign of the adjustment forcing"

**Problem.** Every conclusion is phrased in terms of S = d ln LWP / d ln N_d of the domain-mean LWP. The abstract ends with "the sign and magnitude of the simulated LWP adjustment depend on grid spacing". The ERF community, however, defines an adjustment by its radiative effect relative to the instantaneous (Twomey) forcing (Bellouin et al., 2020; Mülmenstädt et al., 2019). Three consequences follow.

- For adiabatic clouds, d ln τ = (1/3) d ln N_d + (5/6) d ln LWP_ic. The LWP adjustment therefore changes the sign of the albedo response only if S_ic < −0.4. No configuration here comes anywhere near that.
- Cloud albedo susceptibility scales roughly with A(1−A) (Platnick and Twomey, 1994). The thin 312 m clouds (LWP 70–80 g m⁻²) are radiatively far more susceptible than the 300 g m⁻² clouds at 40 km. The same S therefore has a different radiative weight at different grid spacings.
- At sub-kilometre spacing, a large part of the response is in cloud fraction. CF acts on the albedo linearly, not through τ^(5/6).

**Reviewer calculation (illustrative only).** I used the hour 10–12 means for s = 1 with suppression on from `runs.csv` and `cloudcover_3d.csv`. The method:

- in-cloud LWP = LWP / cc_max;
- τ = 0.07 LWP_ic^(5/6) N_d^(1/3), with N_d the diagnosed in-cloud value;
- cloud albedo A = τ / (τ + 13.3), a two-stream form with g = 0.85;
- scene albedo = cc_max · A, with the clear sky neglected;
- each finite N_d step is split sequentially into a Twomey term (N_d changed at fixed LWP_ic and CF), an LWP term and a CF term.

The ratio of the adjustment to the Twomey term is:

| Δx | 20→50 | 50→100 | 100→200 | 200→1000 |
|---|---|---|---|---|
| 40 km | 0.95 (LWP 0.95, CF 0) | 0.89 | 0.61 | 0.18 |
| 5 km | 2.05 | 1.04 | 0.46 | 0.03 |
| 2.5 km | 2.97 | 1.24 | 0.28 | −0.06 |
| 625 m | 3.08 | 0.88 | 0.10 | −0.06 |
| 312 m | 3.24 (LWP 1.07, CF 2.12) | 0.39 | −0.13 | −0.07 |

The total albedo change per branch is positive (brightening) in every configuration. On the moderate branch the increase is 0.070 at 40 km and 0.045 at 312 m: a factor of 1.6, not a change of sign.

The calculation is crude. It is plane-parallel, ignores the solar zenith angle and uses layer rather than cloud-top N_d. But it changes the message. In radiative terms the result is not "the adjustment changes sign at fine resolution". It is:

- the adjustment goes from amplifying the Twomey effect by about 60 % to offsetting it by about 10 % on the 100→200 branch;
- it amplifies the Twomey effect three-fold instead of one-fold on the clean branch.

**Why it matters.** The paper is motivated by ERF. An ERF reader who sees "the sign … of the simulated LWP adjustment depend[s] on grid spacing" will conclude that GSRMs might simulate a positive ERFaci from this mechanism. That is not what these runs show. Expressed relative to Twomey, the effect is a modest offset at high N_d and a strong amplification at low N_d.

**Fix.**

- Compute an offline shortwave albedo, or cloud radiative effect, decomposition at column level from the existing 15 min column LWP, cloud-top r_e or N_d, and cloud-fraction output. Use either:
  - a two-stream calculation at a fixed solar zenith angle (for example 60°) and at the diurnal-mean insolation for the RF02 date and latitude; or
  - a partial-radiative-perturbation decomposition in the sense of Mülmenstädt et al. (2019), applied to pairs of N_d levels.
- Report, for each branch and grid spacing, the Twomey term, the in-cloud LWP adjustment and the CF adjustment, and the ratio of the adjustments to the Twomey term.
- Rewrite the last sentence of the abstract and conclusion 1 in these terms, and reserve "sign" for S itself.
- State explicitly that the runs are nocturnal, so the radiative numbers are a potential albedo response of the simulated cloud state, not a forcing.

### M2. The emphasis is on the N_d range least relevant to anthropogenic ERF; the ERF-relevant branch shows the opposite resolution trend

**Problem.** The abstract and conclusion 1 lead with S₁₀₀→₂₀₀ and the location of the LWP maximum. But the observed RF02 N_d is about 55 cm⁻³, and the anthropogenic perturbation of remote marine stratocumulus is a change in ln N_d of order 0.3–0.7 around a clean baseline. On the interval 20→50 cm⁻³ the susceptibility increases with refinement, from 0.39 at ≥10 km to 0.63–0.76 at ≤5 km (Table 5). On the interval 50→100 cm⁻³ (my estimate from Table 4 using target N_d, not a manuscript result) the trend is non-monotonic: about 0.39 at 40 km, about 0.29–0.43 at 5–625 m, and dropping only at 312 m.

The high-N_d branches (200→1000 cm⁻³) matter for ship tracks and marine cloud brightening. They are a weak guide to ERF, which is dominated by clean regimes because of the concave dependence of the Twomey effect on N_d (Carslaw et al., 2013). Jia and Quaas (2023) further show that the N_d–aerosol relationship is sigmoidal, so the ERF-relevant susceptibility depends strongly on the baseline state.

The "LWP maximum" diagnostic is also ill-conditioned where the curve is flat. At 312 m, LWP at targets 100 and 200 is 76.2 and 73.7 g m⁻²; at 625 m it is 119.8 and 122.1 g m⁻². A 2–3 % change moves the maximum by a factor of two in N_d.

**Why it matters.** As written, the paper suggests that grey-zone models would weaken or reverse the LWP adjustment. In the N_d range that matters for ERF, these runs suggest the opposite: a stronger positive total adjustment at fine spacing, carried by cloud fraction (M3).

**Fix.**

- Fit a smooth function to the six N_d levels of each configuration, for example ln LWP quadratic or piecewise-linear in ln N_d, or a sigmoid form as in Jia and Quaas (2023). Report:
  - the local susceptibility S(N_d) with fit uncertainty;
  - S evaluated at the observed RF02 N_d (about 55 cm⁻³);
  - S averaged over a plausible pre-industrial-to-present-day interval, for example ln N_d from ln 30 to ln 55, with sensitivity to that choice.
- Restructure the abstract around:
  - the clean-branch result (robust, ERF-relevant, CF-dominated);
  - the flattening of the moderate branch;
  - the weak, sedimentation-sensitive negative polluted branch.
- Replace "the LWP maximum moved to about 100 cm⁻³" with a statement on the N_d above which |S| < 0.1.

### M3. Separate the cloud-fraction and in-cloud LWP adjustments; the CF adjustment is the most ERF-relevant resolution dependence and is structurally absent at coarse resolution

**Problem.** The manuscript mentions the cloud-cover part of S₂₀→₅₀ only in passing (0.33 at 312 m with the maximum-overlap definition). The data in `susceptibility.csv` (S_cc and S_ic, s = 1, suppression on) show a clearer picture.

- **Clean branch:** the CF part grows from 0 at ≥10 km to 0.16 (5 km), 0.31–0.41 (2.5 km to 625 m) and 0.53 (312 m). The in-cloud part falls from 0.39 to 0.21.
  - Note that these S_cc values use the LWP > 10 g m⁻² cloud cover. The maximum-overlap value at 312 m is 0.33, so the two definitions must be reconciled in the table I request.
- **Coarse spacing:** CF is exactly 1.00 both by the LWP threshold and by SHOC's subgrid cloud fraction (`cloudcover_3d.csv`). SHOC's assumed PDF cannot represent precipitation-driven mesoscale break-up, so a CF adjustment is impossible in that configuration by construction.
- **Suppression off at ≤2.5 km:** the clean-branch CF term is still positive (0.16–0.25) and the in-cloud term is negative. In other words, cloud cover increases with N_d even without the N_d dependence of autoconversion. The paper does not discuss this. The mechanism might be sedimentation of 12–14 µm droplets, the radiative effect of r_e on thin broken cloud, or entrainment. That deserves at least a diagnosis with the s-dependence already in hand.

**Why it matters.** Satellite-based and GCM-based ERF estimates treat the LWP and CF adjustments as separate terms of comparable importance:

- in ECHAM–HAMMOZ, the CF adjustment is about 23 % of ERFaci and the LWP adjustment about 39 % (Mülmenstädt et al., 2019);
- satellite estimates of the CF effect are of order −0.5 W m⁻² (Gryspeerdt et al., 2016);
- break-up and its suppression by aerosol are central to Goren et al. (2019).

That a grid of a few kilometres or finer begins to produce a CF adjustment at all is arguably the most important ERF-relevant result in the paper. It is also the one most directly relevant to GCMs, whose CF adjustments rest on parameterised macrophysics. Conversely, satellite analyses that discard broken scenes (Jia et al., 2021) would miss exactly this component.

**Fix.**

- Add S_ic and S_cc (with the maximum-overlap and the threshold definitions) to Table 5 for all branches and both suppression settings.
- Add a short subsection on the CF adjustment. It should cover:
  - its emergence with resolution;
  - its dependence on s and on the suppression switch;
  - the open-cell-like state at target 20 cm⁻³ and 312 m.
- Compare with the satellite CF–N_d literature.
- Use in-cloud LWP wherever the comparison is with satellite slopes. For example, the claim in Sect. 3.3 that the negative slopes are "an order of magnitude smaller than the observed ones" should use S_ic, because Gryspeerdt et al. (2019) use in-cloud LWP.

### M4. Resolution dependence or mean-state dependence? The ERF-relevant question is whether coarse models get the susceptibility wrong at a given cloud state

**Problem.** Refining the grid changes the mean state drastically: LWP falls from about 300 to about 75 g m⁻², cloud base rises from about 200 to about 720 m, and surface rain drops by orders of magnitude. The paper attributes the change in S to grid spacing.

Satellite studies show that S itself depends strongly on cloud state: precipitation, LWP, cloud depth and free-tropospheric humidity (Chen et al., 2014; Gryspeerdt et al., 2019; Possner et al., 2020). Precipitation susceptibility likewise decreases with cloud thickness (Terai et al., 2012).

Two cases need to be distinguished.

- If S across all grid spacings, sedimentation factors and suppression settings collapses onto a function of the base-state cloud regime, then resolution acts through the mean state. The lesson for GCMs is then about mean-state and warm-rain biases. That is the argument of Michibata et al. (2016) and Mülmenstädt et al. (2020), which link overly positive GCM LWP adjustments to "too frequent, too light" drizzle. The coarse runs here rain over 100 % of the domain at targets of 20–50 cm⁻³ (`rain_frac` = 1.0), against 0.03–0.34 at ≤1.25 km.
- If S does not collapse, the resolved dynamics change the susceptibility at a given state. That is a stronger and more novel claim.

**Why it matters.** The two interpretations lead to different recommendations for the GCM and GSRM communities. The present Discussion (Sect. 4.1) implicitly assumes the second without testing it.

**Fix.** Plot S, and its CF and in-cloud parts, against base-state predictors evaluated at the lower N_d of each branch. All the predictors are already in `runs.csv`:

- LWP_ic;
- cloud thickness;
- z_b;
- P_sfc;
- the precipitation-to-entrainment-drying ratio of Fig. 6c;
- η.

Pool all 288 runs. Report how much of the variance in S is explained by the state alone, and how much log Δx adds. In addition:

- Compute the precipitation susceptibility S_R = −d ln P / d ln N_d. It is the observable process metric used for warm-rain constraints. From `runs.csv` I estimate about 0.9 at 40 km and about 2.5 at 312 m on the 100→200 branch. Show it against LWP or h, and compare with aircraft and satellite ranges (Terai et al., 2012).
- Compare the raining fraction with RF02 drizzle statistics.

This would give the GCM community the process-level target the Discussion promises.

### M5. Use the spatial domain and the factorial structure to quantify which signs are robust

**Problem.** The only uncertainty measure is the standard deviation over eight autocorrelated 15 min intervals, which the authors correctly say is not an uncertainty. The conclusion is then that the sign of the sub-kilometre susceptibilities "is not established". That is fair but under-uses the data. Two features of the design allow more.

**(a) Spatial sampling.** The 240 km doubly periodic domain contains 11–19 mesoscale cells at sub-kilometre spacing.

*Reviewer calculation:* I split the hour-12 column LWP (`lwp12` in `fields/*.npz`, s = 1, suppression on) into 4 × 4 tiles of 60 km. The standard error of the domain mean estimated from the tile means is about 1.1 % at 312 m (target 200), 0.8 % at 312 m (target 1000), 0.7 % at 625 m and 1.6 % at 2.5 km. At 312 m the LWP difference between targets 200 and 1000 at hour 12 is 5.6 %, which is about four standard errors. The difference between 100 and 200 (3.4 % over hours 10–12) is marginal.

This is a lower bound on the true internal variability. The tiles share the domain-wide evolution and are spatially correlated, and an ensemble would also sample the common drift. It is still an informative, cheap first estimate.

**(b) Pseudo-replication across factors.** The signs of S₂₀₀→₁₀₀₀ in `susceptibility.csv`:

- at ≤2.5 km, negative in 23 of 24 configurations (3 sedimentation factors × 2 suppression settings × 4 grid spacings);
- at 312 m, negative in all six (−0.016 to −0.074).

The sign of S₁₀₀→₂₀₀ with suppression on, by contrast, is positive in all three sedimentation factors at 625 m (+0.03 to +0.04) and negative in all three at 312 m. The configurations are not independent, because they share initial conditions and forcing. But this pattern indicates that the polluted-branch sign is reasonably robust, whereas the moderate-branch sign at 312 m is the fragile result. The abstract currently leads with the fragile one.

**Fix.**

1. Compute block-bootstrap (spatial tile) confidence intervals for the domain-mean LWP and for S. Use the 15 min column output over hours 10–12, which is already processed into `fields/`. Report them alongside the temporal standard deviation.
2. Exploit the factorial design statistically. Fit ln LWP as a function of ln N_d × log Δx × s × suppression, with the relevant interactions, for example as a linear model or ANOVA over all 288 runs. The residual variance of terms that physically should be smooth gives a noise floor. The fitted interaction coefficients give S(Δx, s) with confidence intervals.
3. Check whether the paired runs are decorrelated by hour 10. Compute the spatial correlation of the LWP fields between runs at adjacent N_d (identical initial conditions) as a function of time. If the fields are still correlated, the differences benefit from common random numbers and their noise is smaller than an ensemble would show. If they are decorrelated, the tile estimate in (a) is the relevant noise.
4. Reframe the robust results as:
   - the large positive clean-branch S at ≤5 km, and its CF part;
   - the negative S₂₀₀→₁₀₀₀ at ≤2.5 km, and its steepening with s.

   Present the sign of S₁₀₀→₂₀₀ at 312 m and the location of the LWP maximum as unresolved.

### M6. The satellite section should test what a satellite-style analysis of these runs would infer, not only show that within-scene covariation is non-causal

**Problem.** Section 3.10 regresses column ln LWP on column cloud-top ln N_d within a single scene of uniform aerosol. It concludes that within-scene slopes are unrelated to the causal S. That is correct, but it is not how satellite constraints are built.

Satellite LWP adjustment estimates composite many scenes with different aerosol, aggregated at 1° or regime scales (Gryspeerdt et al., 2019; Quaas et al., 2020). They use N_d retrieved from τ and r_e under adiabatic assumptions, which builds a dependence on LWP into the retrieved N_d (Grosvenor et al., 2018; Arola et al., 2022). The slope depends on the aggregation scale (McComiskey and Feingold, 2012) and on which scenes are retained: overcast-only sampling biases the forcing estimate (Jia et al., 2021). Dipu et al. (2022) did essentially this exercise for a large-domain LES. That paper should be cited and compared with.

Conclusion 6 also adds little. The cloud-top versus layer agreement is a model-internal consequence of a near-constant ratio, as the authors say.

**Why it matters.** The paper has an unusual asset: a causal "truth" for S at every grid spacing, together with a column-resolved cloud field. Testing how a satellite-type estimator performs against that truth, and how that performance depends on grid spacing, would be a genuine contribution to the satellite-constraint literature.

**Fix.** All of the following are feasible with output already reduced to `fields/*.npz`: the LWP × cloud-top N_d and LWP × r_e joint histograms (`jh`, `jh_re`) and the column fields.

1. **Synthetic composite.** For each grid spacing, pool the columns of the six N_d runs, as if a satellite saw six aerosol regimes. Compute the binned mean LWP (in-cloud) against cloud-top N_d and its slope, and compare with the causal S curve. Assess whether the composite reproduces an inverted V, and where it peaks.
2. **Pseudo-retrieval.** Compute an adiabatic N_d from cloud-top r_e and τ, with τ derived from column LWP and r_e. Repeat (1) to show how the shared dependence on LWP changes the slope.
3. **Aggregation scale.** Coarse-grain the 312 m and 625 m columns to 1, 5 and 20 km before regressing. Report how the within-scene and composite slopes change.
4. **Sampling.** Repeat (1) with only overcast columns or tiles retained, which mimics common N_d-retrieval filters. Quantify how much of the clean-branch CF adjustment (M3) such sampling would remove.
5. Report OLS slopes of ln LWP on ln N_d together with reverse or orthogonal regressions. N_d is itself partly a response here (scavenging in thick drizzling columns, evaporation at edges), and the OLS slope is not symmetric.

### M7. The N_d denominator is partly endogenous; use cloud-top N_d for Twomey-relevant and cross-resolution comparisons

**Problem.** The diagnosed in-cloud layer N_d at a given target depends on cloud height, because the activation floor follows the prescribed CCN profile (Appendix B). Cloud height in turn responds to N_d and to Δx.

At target 200 cm⁻³, the layer N_d ranges from 166 cm⁻³ (312 m) to 266 cm⁻³ (40 km). The cloud-top N_d varies only from 152 to 162 cm⁻³ (`runs.csv`). The "matched N_d" comparisons (Sect. 3.2, conclusion 2, Fig. 10) interpolate in layer N_d. They therefore compare coarse runs at a lower target than fine runs, while the albedo-relevant (cloud-top) N_d is almost identical at fixed target.

Within a grid spacing, the denominator also includes a cloud-controlled part: higher N_d gives a thinner, higher cloud, a lower floor and a lower diagnosed N_d. The bias is small for the branch slopes (the authors show S changes by ≤0.10 with cloud-top N_d), but it matters for statements at fixed N_d.

**Fix.**

- Use cloud-top N_d, the quantity relevant to the Twomey effect and to satellites, as the primary variable for matched-N_d comparisons and for the radiative decomposition of M1.
- Alternatively, show both and explain the difference.
- Report S also with the prescribed CCN (target) in the denominator. That is the exogenous "treatment" in the causal sense and the analogue of an aerosol-based ACI index.

### M8. Transience, the nocturnal case and what "adjustment" means for ERF

This complements the first referee's M6 and does not repeat it.

**Problem.** ERF is evaluated over a population of clouds of all ages. For satellite and LES inference, the time dependence of the adjustment is now recognised as essential (Glassmeier et al., 2021; Gryspeerdt et al., 2022; Fons et al., 2023). Fons et al. find an LWP adjustment that is first positive and then negative.

The manuscript reports S at hours 10–12 of a run that is still drifting, in a nocturnal case. Daytime shortwave absorption thins stratocumulus and weakens entrainment, so the nocturnal adjustment is likely an upper bound on entrainment-driven thinning (Sandu et al., 2008).

**Fix.**

- Report a time-integrated S over hours 2–12, and the radiative decomposition of M1 averaged over that period, alongside the hour 10–12 values.
- Avoid "adjustment" in the ERF sense in the title, abstract and conclusions. Use "LWP susceptibility after 10–12 h", or define the term explicitly.
- Add the time-dependent satellite and causal-inference studies to the discussion of transience.

---

## 4. Minor comments

1. **Abstract.** Add one sentence with the radiatively weighted result (M1). Distinguish domain-mean, in-cloud and CF susceptibilities. The abstract currently has many numbers and none of them radiative.
2. **L46.** "Aerosol–cloud interactions remain the largest source of uncertainty in the effective radiative forcing". Be precise: in Forster et al. (2021) the aerosol ERF is the largest contributor to the uncertainty of the total anthropogenic ERF.
3. **L50.** Quaas et al. (2009) concerned LWP–AOD relationships in GCMs compared with satellites; it is a correlational, not causal, comparison. Pair it with Mülmenstädt et al. (2024, GCM paper) to make the point that GCM correlations and causal responses differ. Add Jia et al. (2021) to the list of reasons why present-day relationships underestimate the forcing.
4. **Sect. 2.3 / Table 1.** Justify the N_d range in relation to the observed RF02 N_d and a plausible pre-industrial value. Say explicitly which branch is relevant to ERF and which to ship tracks and cloud brightening.
5. **Sect. 2.4.** Define how S_ic and S_cc are computed (product rule for domain-mean LWP = CF × LWP_ic), and give both cloud-cover definitions for the split.
6. **Sect. 3.2.** "the maximum-overlap cloud cover decreases from 1.00 at Δx ≥ 2.5 km to 0.92 at 312 m". At target 20 cm⁻³ it reaches 0.68 at 312 m. Emphasise that the clean-branch CF signal is the large one.
7. **Sect. 3.3, L202.** Compare with Gryspeerdt et al. (2019) using in-cloud LWP and cloud-top N_d. Note that their observed negative slopes are upper bounds partly because of retrieval and sampling effects, which M6 would let the authors examine directly.
8. **Sect. 3.6.** Add S_R (M4). The rain fraction of 1.0 at ≥10 km for targets of 20–50 cm⁻³ is the "drizzle everywhere" behaviour discussed for GCMs by Michibata et al. (2016) and Mülmenstädt et al. (2020). Say so, cautiously.
9. **Sect. 3.10, Fig. 11b.** The y-axis (N_d relative to the scene mean) spans only ±15 %. Within-scene slopes of up to ±8 therefore come from small N_d variance and may suffer from leverage by a few columns. Report the N_d standard deviation per scene and show the scatter for one case.
10. **Sect. 3.10.** State how the AeroCom cloud-top operator weights partially cloudy columns. A satellite retrieval would not see a column with a cloud-top fraction of 0.1 as cloudy, so define a pixel-like cloud mask, for example cloud-top fraction > 0.9.
11. **Sect. 4.3.** Cite Dipu et al. (2022). Their large-domain LES of continental clouds also failed to reproduce the entrainment-driven negative branch at high N_d, a useful parallel to the weak negative branch here. Also cite Costa-Surós et al. (2020), where kilometre-to-LES-scale ICON simulations gave an ERFaci dominated by the Twomey effect with small adjustments.
12. **Sect. 4.2.** The argument that the coarse runs "are not representative of GCM columns" is sound, but the paper can still say something useful. The coarse configuration lacks any CF adjustment, its precipitation is spatially homogeneous, and it has the positive, autoconversion-driven S typical of GCMs. This is exactly the GCM behaviour that satellite-based warm-rain constraints target.
13. **LW radiation.** In a nocturnal case the longwave cloud radiative effect is the only radiative effect present. At 312 m and target 20 cm⁻³ (CF 0.50–0.68) it is not saturated. Report the top-of-atmosphere longwave change between N_d levels from the RRTMGP output, for completeness.
14. **Table 5.** Add columns for S at the observed RF02 N_d (M2) and the radiative adjustment-to-Twomey ratio (M1).
15. **Fig. 3.** Add a horizontal zero line and shade the range of S implied by the tile-bootstrap uncertainty (M5).
16. **Fig. 10.** Repeat panel (a) at matched cloud-top N_d (M7).
17. **Conclusion 6.** Replace it with the results of M6, or drop it.
18. **Terminology.** "LWP adjustment", "susceptibility" and "response" are used interchangeably. Define them once. In the ERF literature "adjustment" refers to the radiative effect of the cloud response after the instantaneous forcing.

---

## 5. Additional analyses feasible with existing output

All of these use files already present under `dp_screamxx_sedps_12h/manuscript/tables/` and `fields/`, or the 15 min column and cloud-top output from which they were derived. They require no new simulations.

| # | Analysis | Inputs | Addresses |
|---|---|---|---|
| A1 | Offline two-stream or PRP albedo decomposition (Twomey / LWP_ic / CF) per branch and Δx, at a fixed solar zenith angle and at diurnal-mean insolation | column LWP, cloud-top r_e and N_d, cloud fraction (15 min) | M1, M3 |
| A2 | Smooth fit of ln LWP(ln N_d) per configuration; local S at the observed N_d of 55 cm⁻³; S averaged over a pre-industrial-to-present-day interval | `runs.csv` | M2 |
| A3 | Table of S_ic and S_cc (both cloud-cover definitions) for all branches; diagnosis of the CF adjustment in the suppression-off runs | `susceptibility.csv`, `cloudcover_3d.csv` | M3 |
| A4 | S against base-state LWP, h, z_b, P_sfc, P/entrainment-drying ratio and η, pooled over all runs; variance explained by state versus log Δx | `runs.csv`, `ml_budget.csv` | M4 |
| A5 | Precipitation susceptibility S_R against LWP or h; raining fraction against observations | `runs.csv` | M4 |
| A6 | Spatial block-bootstrap CIs for LWP and S | `fields/*.npz` (column LWP), 15 min column output | M5 |
| A7 | Factorial linear model or ANOVA of ln LWP over all 288 runs | `runs.csv` | M5 |
| A8 | Time series of the spatial correlation of LWP between paired N_d runs | column output | M5 |
| A9 | Synthetic satellite composite, pseudo-retrieved N_d, aggregation-scale and overcast-sampling tests | `fields/*.npz` (`jh`, `jh_re`, column fields) | M6 |
| A10 | Matched comparisons and S with cloud-top N_d and with target CCN as denominators | `runs.csv`, `matched_nd.csv` | M7 |
| A11 | Time-integrated S (2–12 h) and its radiative weighting | `s_time.csv`, A1 | M8 |
| A12 | Top-of-atmosphere longwave flux change between N_d levels | RRTMGP output | minor 13 |

---

## 6. Literature the authors should engage with (verified; DOIs given)

Already in the bibliography, but under-used for the arguments above:

- Bellouin, N., et al. (2020), *Rev. Geophys.*, 58, e2019RG000660, https://doi.org/10.1029/2019RG000660. The adjustment-relative-to-Twomey framework (M1).
- Gryspeerdt, E., et al. (2019), *ACP*, 19, 5331, https://doi.org/10.5194/acp-19-5331-2019. In-cloud LWP and regime dependence (M3, M4).
- Mülmenstädt, J., et al. (2020), *Sci. Adv.*, 6, eaaz6433, https://doi.org/10.1126/sciadv.aaz6433. Warm-rain constraints (M4).
- Michibata, T., et al. (2016), *ACP*, 16, 15413, https://doi.org/10.5194/acp-16-15413-2016. GCM drizzle frequency (M4).
- Arola, A., et al. (2022), *Nat. Commun.*, 13, 7357, https://doi.org/10.1038/s41467-022-34948-5. Retrieval co-dependence (M6).

To add:

- Mülmenstädt, J., Gryspeerdt, E., Salzmann, M., Ma, P.-L., Dipu, S., and Quaas, J. (2019). *ACP*, 19, 15415–15429. https://doi.org/10.5194/acp-19-15415-2019. PRP decomposition into Twomey, LWP and CF terms (M1, M3).
- Gryspeerdt, E., Quaas, J., and Bellouin, N. (2016). Constraining the aerosol influence on cloud fraction. *JGR Atmos.*, 121, 3566–3583. https://doi.org/10.1002/2015JD023744 (M3).
- Quaas, J., et al. (2020). Constraining the Twomey effect from satellite observations: issues and perspectives. *ACP*, 20, 15079–15099. https://doi.org/10.5194/acp-20-15079-2020 (M6, M7).
- Jia, H., Ma, X., Yu, F., and Quaas, J. (2021). Significant underestimation of radiative forcing by aerosol–cloud interactions derived from satellite-based methods. *Nat. Commun.*, 12, 3649. https://doi.org/10.1038/s41467-021-23888-1. Sampling of broken scenes (M3, M6).
- Jia, H., and Quaas, J. (2023). Nonlinearity of the cloud response postpones climate penalty of mitigating air pollution in polluted regions. *Nat. Clim. Change*, 13, 943–950. https://doi.org/10.1038/s41558-023-01775-5. Baseline dependence of the susceptibility (M2).
- Dipu, S., et al. (2022). Exploring satellite-derived relationships between cloud droplet number concentration and liquid water path using a large-domain large-eddy simulation. *Tellus B*, 74, 176–188. https://doi.org/10.16993/tellusb.27. The closest methodological analogue to M6.
- Costa-Surós, M., et al. (2020). Detection and attribution of aerosol–cloud interactions in large-domain large-eddy simulations with the ICOsahedral Non-hydrostatic model. *ACP*, 20, 5657–5678. https://doi.org/10.5194/acp-20-5657-2020. ERFaci at LES-like resolution dominated by the Twomey effect (minor 11).
- McComiskey, A., and Feingold, G. (2012). The scale problem in quantifying aerosol indirect effects. *ACP*, 12, 1031–1049. https://doi.org/10.5194/acp-12-1031-2012 (M6).
- Terai, C. R., Wood, R., Leon, D. C., and Zuidema, P. (2012). Does precipitation susceptibility vary with increasing cloud thickness in marine stratocumulus? *ACP*, 12, 4567–4583. https://doi.org/10.5194/acp-12-4567-2012 (M4).
- Platnick, S., and Twomey, S. (1994). Determining the susceptibility of cloud albedo to changes in droplet concentration with the Advanced Very High Resolution Radiometer. *J. Appl. Meteorol.*, 33, 334–347. https://doi.org/10.1175/1520-0450(1994)033<0334:DTSOCA>2.0.CO;2 (M1).
- Gryspeerdt, E., Glassmeier, F., Feingold, G., Hoffmann, F., and Murray-Watson, R. J. (2022). Observing short-timescale cloud development to constrain aerosol–cloud interactions. *ACP*, 22, 11727–11738. https://doi.org/10.5194/acp-22-11727-2022 (M8).
- Fons, E., Runge, J., Neubauer, D., and Lohmann, U. (2023). Stratocumulus adjustments to aerosol perturbations disentangled with a causal approach. *npj Clim. Atmos. Sci.*, 6, 130. https://doi.org/10.1038/s41612-023-00452-w. Time-dependent sign of the LWP adjustment, causal inference (M5, M8).

- Carslaw, K. S., et al. (2013). Large contribution of natural aerosols to uncertainty in indirect forcing. *Nature*, 503, 67–71. https://doi.org/10.1038/nature12674. Dominance of clean, pre-industrial states in the uncertainty of ERFaci (M2).
