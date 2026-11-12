> *Disclaimer: this is an AI-simulated review. Its perspective is modelled on the published research of Bjorn Stevens. It was not written by him and does not represent his actual opinions.*

# Referee report: Reviewer B (perspective informed by the published work of B. Stevens)

**Manuscript:** "Horizontal resolution dependence of the liquid water path response to droplet number in doubly periodic EAMxx simulations of drizzling stratocumulus", submitted to *Atmospheric Chemistry and Physics*

**Version reviewed:** LaTeX source `scmlib/sed-precsupp-study/manuscript/sedps_acp_manuscript.tex`, as of 11 Nov 2026. Line numbers below refer to this file.

**Numbers I checked:** I checked some numbers against `dp_screamxx_sedps_12h/manuscript/tables/*.csv`, mainly `runs.csv`, `susceptibility.csv` and `obs_comparison.csv`. I did not read any model output.

**Previous review:** I read the earlier referee report and the authors' response. I agree with most of that report. I do not repeat its points, except where I disagree or think it missed the more basic physical issue.

### Published work this perspective draws on (DOIs verified via Crossref)

- Stevens, B., and Bretherton, C. S. (1999): Effects of resolution on the simulation of stratocumulus entrainment. *QJRMS*, 125, 425–439. https://doi.org/10.1002/qj.49712555403
- Stevens, B., Moeng, C.-H., and Sullivan, P. P. (1999): Large-eddy simulations of radiatively driven convection: sensitivities to the representation of small scales. *J. Atmos. Sci.*, 56, 3963–3984. https://doi.org/10.1175/1520-0469(1999)056<3963:LESORD>2.0.CO;2
- Stevens, B. (2002): Entrainment in stratocumulus-topped mixed layers. *QJRMS*, 128, 2663–2690. https://doi.org/10.1256/qj.01.202
- Stevens, B., et al. (2003): Dynamics and chemistry of marine stratocumulus – DYCOMS-II. *BAMS*, 84, 579–593. https://doi.org/10.1175/BAMS-84-5-579
- Stevens, B., et al. (2005): Evaluation of large-eddy simulations via observations of nocturnal marine stratocumulus. *Mon. Weather Rev.*, 133, 1443–1462. https://doi.org/10.1175/MWR2930.1
- Ackerman, A. S., et al. (2009): Large-eddy simulations of a drizzling, stratocumulus-topped marine boundary layer. *Mon. Weather Rev.*, 137, 1083–1110. https://doi.org/10.1175/2008MWR2582.1
- Stevens, B., and Feingold, G. (2009): Untangling aerosol effects on clouds and precipitation in a buffered system. *Nature*, 461, 607–613. https://doi.org/10.1038/nature08281
- Stevens, B., et al. (2019): DYAMOND: the DYnamics of the Atmospheric general circulation Modeled On Non-hydrostatic Domains. *Prog. Earth Planet. Sci.*, 6, 61. https://doi.org/10.1186/s40645-019-0304-z
- Stevens, B., et al. (2020): The added value of large-eddy and storm-resolving models for simulating clouds and precipitation. *J. Meteor. Soc. Japan*, 98, 395–435. https://doi.org/10.2151/jmsj.2020-021

---

## 1. Summary

The authors ran a factorial set of 288 doubly periodic EAMxx (SCREAM: SHOC turbulence + P3 microphysics) simulations of the DYCOMS-II RF02 nocturnal drizzling stratocumulus. The factors are:

- eight horizontal grid spacings, from 40 km to 312 m;
- six prescribed droplet-number targets;
- three cloud-droplet fall-speed multipliers;
- the KK2000 autoconversion either with or without its N_d dependence.

The main findings are as follows.

- At 10–40 km, where the runs are effectively single-column, LWP rises monotonically with N_d, with S₁₀₀→₂₀₀ ≈ 0.25.
- As the grid is refined, the diagnosed inversion deepening rate roughly doubles, cloud base rises, clouds thin and rain production collapses. The LWP maximum moves to N_d ≈ 100 cm⁻³ at 312 m, where a very weak negative branch appears (S ≈ −0.05).
- Nothing converges.
- A mixed-layer budget associates the thinning with entrainment warming and drying that exceed the radiative and surface forcing.

The revision is much more careful than the earlier version: claims are hedged, the budget is presented as diagnostic, and limitations are listed. As a record of how one GSRM-class model behaves across the grey zone for a well-studied case, the paper has value. My concerns are about physical interpretation, which is where I think the paper can contribute much more than it now does. Three questions are not adequately answered:

- What, physically, is the "entrainment" that increases with resolution?
- Is the change in the N_d response a change in the response, or a change in the state on which the response is evaluated?
- What do transient 12 h susceptibilities say about a buffered system?

## 2. Recommendation

**Major revision.**

The data set is valuable, and most of what I ask for can be done with existing output. However, the central physical narrative is not yet supported. That narrative is: finer grids → stronger entrainment → thinner, non-raining clouds → loss of precipitation suppression → inverted V. Each link is either undiagnosed or partly an artefact of how it is measured.

- **Entrainment link.** The increase in entrainment with horizontal refinement happens at a fixed 50 m vertical spacing across the inversion. The most parsimonious explanation for it is numerical: an under-resolved interface mixing more vigorously as more resolved vertical velocity reaches it. That is precisely the failure mode documented in the stratocumulus LES literature. The paper never tests this.
- **The η > 1 argument.** It rests on an inversion-jump definition that roughly doubles the jump relative to the RF02 specification. Under the authors' own definition, the observed RF02 entrainment rate implies η ≈ 1.
- **The susceptibility contrast.** A quick check of the authors' own tables suggests that most of the resolution dependence of S can be explained by the base state, i.e. the ratio of surface precipitation to entrainment drying. On that reading, resolution matters because it changes the mean state, not because it changes the response function.
- **The comparison across grid spacings.** It sets a quasi-equilibrium state (coarse runs) against strongly transient states (sub-km runs), which are still far from their mixed-layer equilibrium inversion height.

None of these issues is fatal. Each needs to be addressed before the paper can claim to teach us something about grey-zone aerosol–cloud adjustments, rather than about one configuration's drift.

---

## 3. Major comments

### M1. The "entrainment" that increases with resolution is not physically identified. Under-resolution of the inversion is the leading hypothesis and must be tested.

**Problem.** The entrainment rate is diagnosed as w_e = dz_i/dt − w_s(z_i), with z_i taken as the θ_l midpoint crossing (L125). It rises from about 3.7 mm s⁻¹ at 40 km to 7.7 mm s⁻¹ at 5 km and 8.1 mm s⁻¹ at 312 m (L264). Throughout, the vertical spacing at the inversion stays at about 50 m (L66, L299).

In LES of nocturnal stratocumulus, the dominant sensitivity of entrainment is to how the cloud-top interface is represented: vertical resolution, numerical diffusion of the advection scheme, and the behaviour of the subgrid model in the stably stratified interface layer. The relevant studies are:

- Stevens and Bretherton (1999);
- Stevens, Moeng and Sullivan (1999);
- Bretherton et al. (1999);
- Stevens et al. (2005), where native configurations "greatly overestimated mixing at cloud top" unless the vertical grid was refined to about 5 m or the subgrid model was limited at the interface;
- Pressel et al. (2017);
- Mellado et al. (2018);
- Matheou and Teixeira (2019).

Here the horizontal grid is refined by a factor of 128 while the vertical grid stays an order of magnitude coarser than in the RF02 LES. As resolved vertical velocity grows (resolved share 3 % → 67 %, L284), more of the transport across a 50 m-thick numerical interface is carried by the dynamical core's vertical advection and remap, together with SHOC's diffusivity. The diagnosed w_e therefore conflates three things:

- physical engulfment;
- parameterised mixing;
- implicit numerical mixing.

The latter is expected to grow precisely as the resolved eddies become energetic but remain under-resolved near the interface. The positive boundary-layer skewness at 312 m at all N_d (L286) is consistent with this. A radiatively driven, well-mixed stratocumulus layer should have negative skewness. Positive skewness with near-grid-scale updrafts is a symptom of an under-resolved flow, not of an approach to LES.

The authors' own data contain a further clue. At hours 4–6 the 5 km runs are indistinguishable from 40 km:

| Δx | w_e (mm s⁻¹) | LWP (g m⁻²) |
|---|---|---|
| 40 km | 4.16 | 158.8 |
| 5 km | 4.07 | 155.9 |

(`obs_comparison.csv`)

By hours 8–12, however, w_e at 5 km has nearly doubled (7.7 versus 3.7 mm s⁻¹, target 200; `runs.csv`). The "10 → 5 km transition" is thus a spin-up of something that takes about 6 h to develop. That is more suggestive of a slowly growing grid-scale circulation (cf. the stripes in Fig. 1, L183) than of resolved boundary-layer turbulence.

**Why it matters.** The abstract's first causal statement is "with decreasing grid spacing, entrainment generally increased". Every downstream result depends on it: η > 1, the warming and drying, the thinning, the loss of rain, and the shift of the LWP maximum. If a large part of the increase is implicit numerical mixing at an under-resolved inversion, the paper describes a vertical-resolution artefact that is unmasked by horizontal refinement. That is not grey-zone physics. It is still a useful result for GSRM developers, but it is a different paper.

**Fix (feasible with existing output).**

1. **Close a flux budget at the inversion.** Use the 2-hourly 3D snapshots and the 15-min horizontally averaged profiles. At z_i, compute:
   - the resolved flux ⟨w′θ_l′⟩ and ⟨w′q_t′⟩ on the physics grid;
   - SHOC's flux.

   Compare their sum with the entrainment flux implied by the θ_l and q_t tendencies of the boundary layer (or with −w_e Δθ_l). The residual is implicit (numerical) mixing. Show the three components against Δx. Even two snapshots per run (10 and 12 h) for s = 1 at targets 50, 200 and 1000 would be decisive. If the residual grows with refinement, say so plainly.
2. **Diagnose the sharpness of the inversion.** Report it against Δx and time, for example as the depth over which domain-mean θ_l rises from 10 % to 90 % of its jump. Also report the number of model levels within the entrainment zone. With z_i rising through about 200 m at 312 m but only about 70 m at 40 km (L125), the effective vertical resolution of the interface also changes with time and with Δx.
3. **Show the time series of w_e, resolved variance and SHOC TKE at 10, 5 and 2.5 km.** This would identify when and how the 5 km departure develops. A w spectrum at 5 km would show whether the variance sits at 2–6 grid lengths, a signature of numerically controlled circulations.
4. **Reword the text.** Until (1) is done, call the quantity what it is: the diagnosed inversion deepening rate corrected for subsidence. State in the abstract that the vertical spacing at the inversion (about 50 m, ten times the RF02 LES) was held fixed while the horizontal grid was refined. Sect. 4.4 mentions this only as a limitation; it is in fact a competing explanation of the main result.

### M2. The η > 1 diagnostic depends on an inversion-jump definition that roughly doubles the jump, and under that definition the observed RF02 entrainment also gives η ≈ 1.

**Problem.** In the budget (L150) and in η (L266), Δθ_l is the difference between θ_l at 100 m above z_i and the mixed-layer mean. In RF02 the free-tropospheric θ_l above the inversion increases as the cube root of the height above z_i, so the profile rises by about 4.6 K in the first 100 m. In `runs.csv` the resulting Δθ_l is 11.0–12.0 K at all grid spacings (e.g. 11.2 K at 312 m and 12.0 K at 40 km, target 200). The specified jump at the interface is about 6.7 K (288.3 K to 295 K, Ackerman et al. 2009).

η therefore scales with an arbitrary offset, and so do the entrainment warming and drying terms in the budget. A more physical choice is the jump across the entrainment zone, as in Stevens (2002) and Lilly (1968), or a flux-jump estimate. With such a jump, η at 312 m would fall from about 1.25 to about 0.8.

Second, using the authors' definition with the observed RF02 values gives:

- w_e = 6.0–7.6 mm s⁻¹ (Faloona et al. 2005);
- Δθ_l ≈ 11.5 K;
- F_rad ≈ 85 W m⁻²;
- hence η_obs ≈ 0.9–1.1.

So "η exceeds one at fine spacing" (L268, conclusion 4) does not mark anomalous behaviour. At hours 4–6 it may simply mean that the fine runs entrain about as much as was observed, and that the coarse runs (η ≈ 0.55) entrain too little. This reverses the implied reading of Sect. 3.7.

**Fix.**

- Report η and the budget terms for offsets of 50, 100 and 150 m and for an interface jump (e.g. extrapolated from below and above the entrainment zone, or a flux-jump estimate).
- Compute η_obs with the same definition and put it on Fig. 7b.
- Reframe Sect. 3.7: the issue is which grid spacing gives the right entrainment efficiency for the right reason, not that η > 1.

### M3. Fidelity of the case setup to the RF02 specification: radiation, free-tropospheric drift, winds, droplet profile and duration

The paper benchmarks against the RF02 LES and SCM intercomparisons (Sect. 3.1). That benchmarking is meaningful only if the forcing is the same, or the differences are shown to be small. The following points are not covered by the previous referee.

**(a) Radiation and the free troposphere.** The GCSS DYCOMS-II specification (Stevens et al. 2005; Ackerman et al. 2009) uses a parametric long-wave flux. It includes an above-inversion term designed to offset subsidence warming, so that the cube-root free-tropospheric profile remains approximately steady. Here RRTMGP is used, and the free troposphere is nudged only above 650 hPa (L77). Between the inversion and 650 hPa, therefore, subsidence acts on a strongly stratified profile without the balancing term. Near the inversion dθ/dz is large, so subsidence warming is several K per day, much larger than clear-sky radiative cooling. The jump and the entrained-air properties thus drift in time. Because the sub-km runs deepen by about 200 m into a different part of the profile while the coarse runs barely move, the drift is resolution-dependent.

The boundary-layer radiative cooling of 80–88 W m⁻² (L264) also needs comparison with the cloud-top flux divergence that the specification produces for a comparable LWP.

*Fix:*
- Show Hovmöller plots or time-sliced profiles of θ_l and q_t from z_i to 3 km, for 40 km and 312 m.
- Quantify the subsidence and radiative tendencies above z_i.
- Compare F_rad with the specified forcing.

**(b) Prescribed surface fluxes are the protocol, not a departure.** L79 lists the prescribed fluxes as one of three departures from the intercomparison protocol. In the RF02 LES case, the specified surface sensible and latent heat fluxes are 16 and 93 W m⁻², the values used here; the SCM case adopted them as well. The sentence should be corrected. The previous referee's request for interactive fluxes (their M4) would move the setup away from the benchmark, not towards it. The bulk feedback estimate in Sect. 4.4 is fine as a sensitivity statement, but it should not be presented as fixing a protocol deviation.

**(c) No geostrophic forcing and no Coriolis.** The specified RF02 case is forced by a sheared geostrophic wind with Coriolis. Here the initial winds simply decay (L79). In SHOC, shear production and surface stress feed TKE, and in the resolved flow, shear at the inversion contributes to entrainment. Removing both changes the TKE budget in a way that depends on how much of it is resolved. Is the decay of the domain-mean wind the same at all Δx? Show the wind profiles at hours 6 and 12, and say whether the inversion shear differs between 40 km and 312 m. This is a cheap check.

**(d) Droplet number varies within the cloud and with cloud height.** P3 sets in-cloud N_d to at least a scaled SPA CCN profile that decreases with height (L87, Fig. A4b). The specification used a constant N_d = 55 cm⁻³. Within a single cloud, N_d therefore varies by about a factor of two from base to top (about 345 → 150 cm⁻³ for target 200). The N_d at cloud top, where sedimentation acts on entrainment, falls as the cloud rises.

As a result, two physical effects are coupled in a resolution-dependent way: the cloud-top N_d that governs the sedimentation–entrainment coupling, and the inversion height. The interpolation to fixed diagnosed N_d (a layer median) does not remove this. At minimum, report the susceptibilities using cloud-top N_d as the abscissa in the main text (the data exist: `S_*_top` in `susceptibility.csv`). State clearly that the treatment of N_d is a departure from the benchmark.

**(e) Evaluation window versus analysis window.** The evaluation (Table 3) is at hours 4–6, but every result is at hours 10–12, after a further 4–6 h of drift under steady forcing that is no longer tied to any observed state. The table should also give the hour 10–12 state for the same runs. Add the observed cloud-base height and cloud-base drizzle rate (vanZanten et al. 2005), so that the drift is visible in the same units. As noted in M1, the 5 km run moves from "LES-like" to "high-entrainment" between these two windows.

### M4. A 312 m doubly periodic EAMxx/SHOC run should not be read as "approaching LES"; the paper should say how far from LES it is and place every run on a Δx/z_i axis.

**Problem.** The paper is careful not to call 312 m converged, but Sects. 3.8–3.9 and 4.1 still implicitly treat it as the end of a path towards LES. By the usual criteria it is squarely in Wyngaard's terra incognita.

- **Grid spacing relative to the boundary layer.** The nominal Δx/z_i is about 0.3. The physics columns are 469 m apart (Δ_phys/z_i ≈ 0.47). The effective resolution of the spectral-element core is a few grid lengths, i.e. of the order of z_i. The energy-containing eddies, with wavelengths of about 1–1.5 z_i, are therefore at or beyond the effective resolution.
- **Subgrid length scale.** SHOC caps its mixing length at Δx (L62). An LES subgrid model at the same Δ would use a length of order 0.1–0.2 Δ. At 312 m, SHOC is thus still acting as a boundary-layer (RANS-type) closure with a grid-limited length scale. It is not acting as an LES subgrid model.
- **Moments.** One-third of the w variance is subgrid (L284), and the resolved skewness has the wrong sign for a radiatively driven layer (L286).
- **Vertical resolution.** The vertical grid is about ten times coarser than the RF02 LES at the interface.

**Why it matters.** The direction of the trend from 625 m to 312 m (LWP falling 21–40 %, L299) is often read as "towards the LES answer". Nothing in the paper supports that reading, and in the LES literature under-resolution typically produces over-entrainment and too-thin clouds (Stevens et al. 2005). A reader could equally conclude that the sub-km trend moves away from the physical solution because resolved eddies are increasingly energetic at an unresolved interface.

**Fix.**

- Plot the main diagnostics against Δx/z_i, using physics-column spacing and an estimated effective resolution.
- Compare the resolved share (Fig. 9a) with a grey-zone partition function such as that of Honnert et al. (2011), to show where SHOC's repartition departs from the expected behaviour. Part of that departure is imposed by the length-scale cap.
- Estimate the effective resolution from kinetic-energy or w spectra in the 3D snapshots.
- State explicitly in Sect. 4 and in the conclusions that the finest run is not an approximation to LES. Present the results as the behaviour of a grey-zone model whose sub-km trend may or may not point towards the physical answer.

### M5. Is the dependence on resolution a dependence on the base state? The authors' own numbers suggest it largely is, and this should become the organising result.

**Problem.** The paper frames the result as "the LWP adjustment depends on grid spacing". The physical argument it invokes (Sect. 3.6, Discussion) is the classical one of Ackerman et al. (2004), Wood (2007) and Hoffmann et al. (2020): the sign of the response is set by the relative strength of the precipitation sink and entrainment drying. If that argument is right, S should depend on that ratio, whatever the grid spacing that produced the state.

I checked this with the authors' tables. I paired S₁₀₀→₂₀₀ (suppression on, from `susceptibility.csv`) with the ratio of surface precipitation to entrainment drying, P_sfc/F_ent,moist, of the target-100 run (`runs.csv`). Over all 24 combinations of grid spacing and sedimentation factor, S correlates with ln(P_sfc/F_ent,moist) at r ≈ 0.91, with cloud thickness at r ≈ 0.83, and with base-state LWP at r ≈ 0.86. Examples:

| Δx | s | P_sfc/F_ent,moist | S₁₀₀→₂₀₀ |
|---|---|---|---|
| 40 km | 1 | 0.27 | 0.27 |
| 5 km | 2 | 0.27 | 0.27 |
| 2.5 km | 2 | 0.24 | 0.23 |
| 1.25 km | 2 | 0.16 | 0.20 |
| 312 m | 1 | 0.003 | −0.05 |

The puzzling result that S₁₀₀→₂₀₀ *increases* with s at 2.5 and 1.25 km (L213, L244) also fits this picture. At those grid spacings, faster sedimentation roughly triples surface precipitation in the base state (0.21 → 0.70 mm d⁻¹ at 2.5 km). It thereby moves the run towards the precipitation-controlled regime.

The same reading applies to the coarse-resolution "interaction" term in the decomposition. Much of what the factorial decomposition labels interaction or residual may simply be the movement of the base state along a common response curve.

**Why it matters.** This changes the message. Under this reading, resolution does not principally change *how* the cloud responds to N_d. It changes the cloud: the depth, the cloud base and the precipitation efficiency. The response then follows the state, which is the more useful and more general statement.

It also redirects attention to the right question for GSRMs: does the model get the mean state, in particular cloud thickness and precipitation efficiency, right? It also explains why the decomposition is design-dependent. The off configuration moves the base state (heavy drizzle at high N_d), so it samples a different part of the same curve.

**Fix.**

- Make a figure of S (all branches, both autoconversion settings, all s) against a base-state measure. Candidates are P_sfc/F_ent,moist (Ackerman et al. 2004), cloud-base rain rate, cloud thickness, or the ratio of precipitation to entrainment time scales.
- Colour the points by Δx.
- Quantify how much of the variance in S is explained by the state alone, and how much remains attributable to Δx at fixed state. The latter, if any, is the genuine "resolution dependence of the response".
- Rewrite Sects. 3.5–3.6 and 4.1 around this.

A closely related, cheaper point concerns the precipitation sink itself. At hours 4–6 the 2.5 km runs produce five times more surface precipitation than the 40 km runs (0.68 versus 0.14 mm d⁻¹), despite lower LWP (132 versus 159 g m⁻²; `obs_comparison.csv`). KK2000 is applied without a subgrid variance enhancement, so the coarse runs never engage the nonlinearity of q_c^2.47, whereas resolved variability at km scales does. Compute the enhancement factor ⟨q_c^2.47⟩/⟨q_c⟩^2.47 from the 3D snapshots. Show how much of the resolution dependence of the precipitation efficiency per unit LWP it explains. This is a resolution-dependent bias in the very sink whose suppression the paper attributes.

### M6. Transience, equilibrium and buffering: the coarse and fine runs are at different stages of adjustment, and the paper's susceptibilities are not buffered responses.

**Problem.** In a stratocumulus-topped mixed layer with constant divergence D, the inversion relaxes towards z_i,eq = w_e/D on the time scale 1/D. Here 1/D ≈ 74 h. Using the diagnosed w_e (8–12 h fit, target 200, s = 1):

| Δx | z_i,eq (m) | z_i at hours 10–12 (m) |
|---|---|---|
| 40 km | ≈ 990 | ≈ 863 |
| 2.5 km | ≈ 1810 | ≈ 942 |
| 312 m | ≈ 2170 | ≈ 1016 |

The 40 km runs are thus near their equilibrium depth. The sub-km runs are not even halfway, and their LWP is falling by 4–6 % h⁻¹ (L233). The fast LWP adjustment to the current z_i takes hours. The slow adjustment of z_i takes days (Bretherton et al. 2010; Jones et al. 2014).

The paper's S at hours 10–12 is therefore a fast-manifold response, conditioned on a z_i that is still drifting and that differs between N_d levels at 312 m (by about 17 m between targets 100 and 1000, and by about 50 m between targets 50 and 1000). Comparing S across Δx compares a quasi-steady system with a transient one. It is not a comparison of two estimates of the same buffered quantity.

This matters for interpretation in the sense of Stevens and Feingold (2009). Buffering refers to the tendency of the cloud system, once it has adjusted, to compensate for a perturbation through other processes. Seifert et al. (2015) showed for precipitating shallow convection that the sensitivity to aerosol is largest in the transient phase and diminishes towards equilibrium. Two distinct situations are also conflated in the paper:

- **Coarse spacing: compensation.** A large precipitation-suppression term is partly offset by an interaction term (L242). That is buffering by compensation.
- **312 m: no sink.** All terms are small because there is no rain to suppress (P_sfc ≤ 0.01 mm d⁻¹ for N_d ≥ 100). That is insensitivity owing to an absent sink, not buffering.

A near-zero S means different things in the two cases, and the paper should say so.

**Fix.**

- Report z_i,eq = w_e/D and the time scale 1/D for each run, and state explicitly that the sub-km runs are far from equilibrium.
- Use the existing mixed-layer budget as a prognostic model to estimate where each configuration would equilibrate. Close w_e with a constant entrainment efficiency diagnosed per run, e.g. a fixed η or the A of Stevens (2002). Show whether the sign of S at sub-km spacing is robust in that equilibrium, in the spirit of Uchida et al. (2010). This needs no new simulations and directly addresses whether the weak negative branch is a transient.
- Distinguish compensation from absent-sink insensitivity in Sect. 4.1.
- Translate S into the quantity that matters for forcing. For an adiabatic cloud, d ln τ/d ln N_d = 1/3 + (5/6) S. This gives about 0.56 at 40 km and about 0.29 at 312 m on the moderate branch, before cloud-fraction changes. So the resolution dependence amounts to a factor of about two in the combined Twomey-plus-LWP response. Stating this frames the result in radiative terms and makes clear what is at stake.

### M7. What the results mean for storm-resolving models is not drawn out, and the most relevant regime (2.5–5 km) is the least understood.

**Problem.** Global storm-resolving models run at 2.5–5 km (Stevens et al. 2019). Stevens et al. (2020) argue that it is at hectometre scales that clouds such as stratocumulus begin to be represented with a more direct connection between circulation and cloud, while km scales mainly improve precipitation and deep convection.

The paper's own results fit this: at 2.5–5 km the boundary layer is about 95 % parameterised (L284). Yet this is where the largest and least explained change occurs. That change is the 10 → 5 km jump in w_e, cloud base and LWP, which develops after hour 6 and coincides with stripe-like structures at about six physics-column wavelengths (L183, L284). For GSRM practice the key question is whether these circulations are physical, or a numerical response that leads to double counting with SHOC. The paper raises this but does not diagnose it, and the discussion (L333) instead reports that S at 2.5–5 km lies "between" 40 km and 312 m. That is true but uninformative.

**Fix.**

- Diagnose the 5 km circulations with the 3D snapshots: their spectrum, their orientation relative to the element grid, their vertical structure, and their onset time.
- If they are grid-scale circulations, state the implication directly: in EAMxx with SHOC, the grey zone for stratocumulus starts at about 5 km, not at 1 km. A closure that does not know this will double count mixing in the GSRM range.
- Recommend the specific remedies this implies: a scale-aware partition, and vertical resolution consistent with the horizontal resolution at the inversion. Avoid the generic "resolution-sensitivity tests".

### M8. Clarity and economy: the paper should be built around one physical argument, with fewer numbers per sentence.

**Problem.** In revision the paper has become more accurate but also longer and more defensive. It has 11 main figures, 4 appendix figures, 6 tables and an abstract carrying more than 15 numbers. Many paragraphs (e.g. L211–213, L242–246, L264–268) hold 10–20 quantitative values. The reader is left to assemble the argument. Several sections (3.4, 3.5 and 3.10) end in "we have not isolated / not established" statements without telling the reader what has been learned.

**Fix.**

- Organise the paper around the mixed-layer argument:
  1. how resolution changes the mean state (entrainment efficiency → z_i, z_b, h);
  2. how the mean state sets the precipitation sink;
  3. how the sink sets S (M5);
  4. which parts are model-specific (M1, M4, M7).
- Move Sect. 3.10 (cloud-top N_d and within-scene covariability) to an appendix or a separate note. It is competent but tangential, and its main message is already well established.
- Condense the decomposition caveats to one paragraph in Methods.
- Use tables for numbers, and use sentences for claims and their physical reason.
- Rewrite the abstract to state, in order: the question; the main physical result (resolution changes the mean state, and the response follows the state); the key quantitative contrast; and the principal caveat (vertical resolution fixed, sub-km runs transient and not LES-like).

---

## 4. Minor comments

1. **L19–23, L420, L425 (editorial).** The manuscript lists an AI system as sole author. My understanding is that Copernicus policy does not allow AI tools to be listed as authors, because they cannot take responsibility for the work. The editor should confirm. "Human review of the manuscript is pending" (L420) must be resolved before submission.
2. **L62.** "SHOC limits its turbulent mixing length to the host grid length." App. B reports a SHOC mixing length of about 1600 m in the upper boundary layer at Δx ≥ 10 km, almost twice z_i. Please comment on what a mixing length larger than the boundary-layer depth means for SHOC's diffusivity at and above the inversion, and whether the stability limiter controls cross-inversion mixing at coarse spacing.
3. **L73.** Calling the β = 0 configuration "precipitation suppression off" invites confusion, because it changes the rain amount strongly in both directions. "N_d-independent autoconversion" is more accurate.
4. **L77.** Give the vertical grid explicitly: a table or figure of level heights from 500 to 1200 m. "About 50 m" (L66) and "25–50 m" (L125) should be reconciled.
5. **L125, z_i definition.** The θ_l midpoint between the boundary layer (<400 m) and the 1400 m value depends on the θ_l at 1400 m. That value drifts under unbalanced subsidence (M3a), and in the sub-km runs it is only about 400 m above z_i by hour 12. Check z_i against a maximum-gradient or q_t-based definition.
6. **L125, w_e uncertainty.** At 40 km, z_i rises by about 25 m (half a level) over the 8–12 h fit window. Give an uncertainty for w_e from the level quantisation.
7. **L146–150.** F_rad is defined as the cooling below z_i + 150 m. For the entrainment closure, the relevant forcing is the long-wave flux divergence across the cloud-top region. Clear-sky cooling within 150 m above z_i, and cloud-base warming, should be shown separately.
8. **L165, Table 3.** Add the observed cloud-base height, the cloud-base drizzle rate and the observed N_d (about 55 cm⁻³). Note that the "LES" entry is a single model (DHARMA), not the ensemble.
9. **L183.** "The mixed layer becomes 1.8 K warmer": warmer than what? Say relative to the initial state or to 40 km, and over what period.
10. **L202.** "The resulting shape resembles the inverted-V shape…" With a negative branch of −0.05 whose sign is not established, I would not invoke the satellite inverted V at all. Say instead that the LWP maximum moves to lower N_d.
11. **L255.** The evaporated fraction of 0.93 at 312 m exceeds the observed 0.73 by a wide margin. Is rain fraction = 1 (L64) important in broken sub-km scenes, where rain falls into clear columns?
12. **L268.** "Larger magnitude at fine spacing indicates that the coupling between sedimentation and entrainment is stronger where part of the boundary-layer circulation is resolved." Given M1, it could equally indicate that sedimentation affects the liquid water in the interface grid cell, where implicit mixing is large. Soften the wording.
13. **L284.** The resolved share is computed on the physics grid from instantaneous snapshots, while SHOC's variance is diagnosed from TKE (stated). Also state whether the resolved variance is computed relative to the domain mean, and how many samples enter it.
14. **L299.** "Vertical resolution at the inversion is known to control entrainment in LES and in SCREAM." Cite Stevens and Bretherton (1999) and Stevens et al. (2005) explicitly for the LES part.
15. **L327.** The q_t jump of 5.8–6.5 g kg⁻¹ is again measured 100 m above z_i. Give the interface value too (M2).
16. **L341.** "Initial-condition spread … typically a few per cent" (also L213) needs a reference or should be removed.
17. **Fig. 2.** The eight grid-spacing colours are hard to separate (especially the 10/20/40 km and 1.25 km/625 m pairs), and the axis labels are very small at print size. Consider a sequential palette with direct line labels.
18. **Fig. 7b.** Add η_obs (M2) and the reference line η = 1 with an explanation of what it means for the mixed-layer θ_l tendency.
19. **Conclusions.** Six numbered items followed by a paragraph of required experiments is too much. Three conclusions, with their physical reasons, would be stronger.
20. **Terminology.** "Susceptibility" is used for d ln LWP/d ln N_d and "adjustment" for the process. Define both once and use them consistently. The abstract uses "LWP adjustment" for S.

---

## 5. Additional analyses feasible with existing output

None of these requires new simulations. Items 1–4 are the most important.

1. **Inversion flux budget** (M1). Use the 10 and 12 h snapshots and the horiz_avg profiles to compare resolved, SHOC and implied entrainment fluxes of θ_l and q_t at z_i. The residual estimates implicit numerical mixing. Do this for s = 1, targets 50, 200 and 1000, at all Δx ≤ 10 km.
2. **State-collapse figure** (M5). Plot S against P_sfc/F_ent,moist, cloud thickness or cloud-base rain rate for all runs, coloured by Δx. My quick check gives r ≈ 0.91 for S₁₀₀→₂₀₀ (on) against ln(P_sfc/F_ent,moist) across all (Δx, s). Quantify the residual dependence on Δx at fixed state.
3. **Jump-definition sensitivity** (M2). Report η and the budget terms for offsets of 50, 100 and 150 m and for an interface jump, plus η_obs from the RF02 observations.
4. **Equilibrium estimate** (M6). Compute z_i,eq = w_e/D for each run. Integrate the existing mixed-layer budget forward with a per-run entrainment efficiency to estimate equilibrium LWP and S.
5. **Free-tropospheric drift** (M3a). Plot θ_l and q_t profiles above z_i at 0, 6 and 12 h for 40 km and 312 m. Report the subsidence and RRTMGP tendencies there, and compare F_rad with the specified forcing.
6. **Spin-up of the 5 km transition** (M1, M7). Show time series of w_e, resolved w variance, SHOC TKE and LWP at 10, 5 and 2.5 km, together with w spectra from the snapshots.
7. **Effective resolution and grey-zone partition** (M4). Compute kinetic-energy or w spectra by Δx, and plot the resolved share against Δx/z_i with a Honnert et al. (2011)-type partition function.
8. **Autoconversion enhancement by resolved variance** (M5). Compute ⟨q_c^2.47⟩/⟨q_c⟩^2.47 by Δx and N_d, and the precipitation efficiency per unit LWP.
9. **Radiative translation** (M6). Report d ln τ/d ln N_d = 1/3 + (5/6) S, together with the cloud-fraction contribution, by Δx.
10. **Wind and shear** (M3c). Plot domain-mean wind profiles at 6 and 12 h by Δx.

---

## 6. Literature the authors should engage with (DOIs verified via Crossref)

- **Stevens, B., and Bretherton, C. S. (1999).** Effects of resolution on the simulation of stratocumulus entrainment. *QJRMS*, 125, 425–439. https://doi.org/10.1002/qj.49712555403
  Resolution and numerical controls on simulated Sc entrainment; central to M1.
- **Stevens, B., Moeng, C.-H., and Sullivan, P. P. (1999).** Large-eddy simulations of radiatively driven convection: sensitivities to the representation of small scales. *J. Atmos. Sci.*, 56, 3963–3984. https://doi.org/10.1175/1520-0469(1999)056<3963:LESORD>2.0.CO;2
  Subgrid and numerical sensitivities of radiatively driven entrainment.
- **Stevens, B., et al. (2005)** (already cited, but only in passing). https://doi.org/10.1175/MWR2930.1
  Native configurations overestimated mixing at cloud top unless the vertical grid was refined or subgrid mixing was limited at the interface. This should be engaged with directly in M1/M4.
- **Matheou, G., and Teixeira, J. (2019).** Sensitivity to physical and numerical aspects of large-eddy simulation of stratocumulus. *Mon. Weather Rev.*, 147, 2621–2639. https://doi.org/10.1175/MWR-D-18-0294.1
  Liquid–radiation–turbulence feedback slows grid convergence; surface fluxes and shear contribute substantially to TKE (relevant to M3c).
- **Zhu, P., Bretherton, C. S., Köhler, M., et al. (2005).** Intercomparison and interpretation of single-column model simulations of a nocturnal stratocumulus-topped marine boundary layer. *Mon. Weather Rev.*, 133, 2741–2758. https://doi.org/10.1175/MWR2997.1
  The DYCOMS-II RF01 SCM companion to Wyant et al. (2007); relevant to the single-column limit and to the vertical-resolution dependence of SCM entrainment.
- **Jones, C. R., Bretherton, C. S., and Blossey, P. N. (2014).** Fast stratocumulus time scale in mixed layer model and large eddy simulation. *JAMES*, 6, 206–222. https://doi.org/10.1002/2013MS000289
  Fast versus slow adjustment; central to M6.
- **Bretherton, C. S., Uchida, J., and Blossey, P. N. (2010)** (already in the .bib). https://doi.org/10.3894/JAMES.2010.2.14
  Slow manifolds and equilibria; should be used for the equilibrium argument (M6), not only cited for run length.
- **Seifert, A., Heus, T., Pincus, R., and Stevens, B. (2015).** Large-eddy simulation of the transient and near-equilibrium behavior of precipitating shallow convection. *JAMES*, 7, 1918–1937. https://doi.org/10.1002/2015MS000489
  Aerosol sensitivity in the transient versus near-equilibrium phases; buffering (M6).
- **Honnert, R., Masson, V., and Couvreux, F. (2011).** A diagnostic for evaluating the representation of turbulence in atmospheric models at the kilometric scale. *J. Atmos. Sci.*, 68, 3112–3131. https://doi.org/10.1175/JAS-D-11-061.1
  Grey-zone partition functions (M4).
- **Stevens, B., et al. (2020).** The added value of large-eddy and storm-resolving models for simulating clouds and precipitation. *J. Meteor. Soc. Japan*, 98, 395–435. https://doi.org/10.2151/jmsj.2020-021
  Km versus hm scales for clouds; frames M7.
- **Schneider, T., Teixeira, J., Bretherton, C. S., et al. (2017).** Climate goals and computing the future of clouds. *Nature Climate Change*, 7, 3–5. https://doi.org/10.1038/nclimate3190
  Resolution requirements for low clouds in global models.
- **Stevens, B., and Feingold, G. (2009)** (already cited, only in the introduction). https://doi.org/10.1038/nature08281
  Should be engaged with in the discussion of what a near-zero S at fine spacing means (M6).

---

*Reviewer B (AI-simulated; perspective informed by the published work of B. Stevens)*
