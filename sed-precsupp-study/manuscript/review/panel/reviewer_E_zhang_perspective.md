> **Disclaimer:** This is an AI-simulated review written for an internal review panel. It is not a review written by, endorsed by, or expressing the actual opinions of any real person.

# Referee report: Reviewer E (perspective informed by the published work of J. Zhang)

**Manuscript:** "Horizontal resolution dependence of the liquid water path response to droplet number in doubly periodic EAMxx simulations of drizzling stratocumulus", submitted to *Atmospheric Chemistry and Physics*

**Version reviewed:** `scmlib/sed-precsupp-study/manuscript/sedps_acp_manuscript.tex` (431 lines, 11 Nov 2026) and the matching PDF. Line numbers below are LaTeX source lines.

**Recommendation:** Major revision

---

## About this persona and how it was built

**Persona check.** A web search confirmed that Jianhao Zhang is a research scientist at NOAA CSL with a CIRES (CU Boulder) affiliation. His listed topics are marine boundary-layer clouds, aerosol–cloud–meteorology interactions, LES modelling, satellite remote sensing and marine cloud brightening. His published work fits most of the requested focus areas: diurnal LES ensembles of stratocumulus aerosol–cloud interactions, decoupling and its effect on the LWP diurnal cycle, satellite-derived albedo susceptibility, and the timing of LWP adjustments. I found less first-author work by him specifically on cloud-droplet sedimentation and entrainment feedbacks. For those topics I drew mainly on the LES literature his work builds on (Bretherton et al. 2007; Hill et al. 2009; Hoffmann et al. 2025). The persona was therefore kept, with that caveat.

**Papers I drew on** (each verified on the publisher's page or by a DOI search):

1. Zhang, J., Chen, Y.-S., Yamaguchi, T., and Feingold, G. (2024): Cloud water adjustments to aerosol perturbations are buffered by solar heating in non-precipitating marine stratocumuli. *ACP*, 24, 10425–10440. doi:10.5194/acp-24-10425-2024
2. Chen, Y.-S., Zhang, J., Hoffmann, F., Yamaguchi, T., Glassmeier, F., Zhou, X., and Feingold, G. (2024): Diurnal evolution of non-precipitating marine stratocumuli in a large-eddy simulation ensemble. *ACP*, 24, 12661–12685. doi:10.5194/acp-24-12661-2024
3. Zhang, J. and Zuidema, P. (2019): The diurnal cycle of the smoky marine boundary layer observed during August in the remote southeast Atlantic. *ACP*, 19, 14493–14516. doi:10.5194/acp-19-14493-2019
4. Zhang, J., Zhou, X., Goren, T., and Feingold, G. (2022): Albedo susceptibility of northeastern Pacific stratocumulus: the role of covarying meteorological conditions. *ACP*, 22, 861–880. doi:10.5194/acp-22-861-2022
5. Zhang, J. and Feingold, G. (2023): Distinct regional meteorological influences on low-cloud albedo susceptibility over global marine stratocumulus regions. *ACP*, 23, 1073–1090. doi:10.5194/acp-23-1073-2023

**What I checked against the data.** I read the previous referee report and the authors' response, but I formed my own judgement. Several numbers below are my own quick calculations from the files listed here. The authors should reproduce them before using them.

- `analysis_report5/explore_scalars.csv`
- `manuscript/tables/ml_budget.csv` and `ml_timeseries.csv`
- the per-run domain-mean profiles in `explore/npz/explore_<case>.npz`, which hold θl, qt, cloud fraction, qc, Nc, SGS and resolved buoyancy fluxes, and w variance

---

## 1. Summary

The authors ran 288 doubly periodic EAMxx (SCREAM) simulations of the nocturnal, drizzling DYCOMS-II RF02 case. Each run lasts 12 h under constant forcing, with prescribed surface fluxes and no shortwave radiation. The factors are:

- eight horizontal grid spacings (40 km to 312 m);
- six target Nd levels (20 to 1000 cm⁻³);
- three cloud-droplet sedimentation factors (0.5, 1, 2);
- the Nd dependence of KK2000 autoconversion switched on or off, with "off" matched at 63 cm⁻³.

The main findings are as follows.

- **Coarse grids (≥10 km).** LWP increases monotonically with Nd, with S₁₀₀→₂₀₀ ≈ 0.25. This positive response disappears when autoconversion does not depend on Nd.
- **Finer grids.** Entrainment increases, the cloud thins and lifts, and rain production collapses. The LWP maximum moves to about 100 cm⁻³ at 312 m, where a weak negative branch (S ≈ −0.04 to −0.05) appears. This branch steepens with faster sedimentation.
- **Budget.** A mixed-layer budget ties the general thinning to entrainment warming and drying that exceed the radiative and surface forcing. It cannot resolve the Nd dependence at sub-km spacing.
- **Convergence.** Nothing converges, and SHOC's mixing length is capped by the grid spacing at 312 m.

The manuscript is careful, unusually transparent and much improved by the previous revision. The caveats about single realisations, transience and pivot dependence are now stated plainly.

My concerns are about **physical interpretation** rather than bookkeeping. The paper explains its resolution dependence with an adjustment framework built on LES theory and evidence: precipitation suppression versus sedimentation/evaporation–entrainment, and mixed-layer budgets. Several properties of EAMxx and of this setup do not sit comfortably within that framework:

- SHOC performs all condensation, so Nd cannot act on evaporation rates.
- The inversion is grid-locked at coarse spacing.
- Entrainment at 312 m is unusually efficient relative to the turbulence that should drive it.
- The decoupling metric gives the opposite ranking to buoyancy-flux and cloud-base diagnostics.
- A nocturnal-only design omits the period in which LES shows that adjustments are buffered.

None of these invalidates the experiment. Each changes what the results can be said to show.

## 2. Recommendation

**Major revision.** The simulations are valuable and the main empirical result is robust: in EAMxx, the LWP–Nd relationship changes shape across the grey zone. The mechanistic narrative, however, especially the sentences that attribute behaviour to "the sedimentation–entrainment feedback" and to "entrainment efficiency where part of the circulation is resolved", needs to be rebuilt on diagnostics that test the mechanism. Most of what I ask for can be done with output that already exists (Section 5).

---

## 3. Major comments

### M1. What can make entrainment depend on Nd in this model, and which pathway the data actually show

The paper states (L62, L327, L347) that SHOC's saturation adjustment computes condensation and evaporation independently of droplet size, and that P3 only evaporates rain. That is a good and important check. Its consequences for interpreting the entrainment response, however, are not followed through.

**(a) The model is always in the fast-evaporation limit.** In EAMxx, Nd can influence cloud-top entrainment through only three routes:

- **Drizzle.** P3 rain removes liquid from the cloud layer and evaporates below cloud, which stabilises the subcloud layer and reduces in-cloud buoyancy production.
- **Sedimentation.** Droplet sedimentation removes liquid water from the entrainment zone (Bretherton et al. 2007).
- **Radiation.** Effective radius affects radiation, which matters only for thin or broken cloud.

The evaporation–entrainment feedback in the sense of Wang et al. (2003) and Hill et al. (2009) needs a size-dependent evaporation (phase-relaxation) time scale, so it is absent. Its bulk-LES analogue, the amount of cloud liquid available for evaporative cooling in the entrainment zone, is present, but only through the drizzle and sedimentation routes. The introduction (L48) and discussion (L327) should therefore not present "evaporation–entrainment" as a candidate pathway in this model. They should say explicitly that any Nd dependence of w_e in EAMxx must pass through rain or sedimentation.

**(b) The data say the dominant Nd dependence of w_e at fine spacing comes from drizzle, not sedimentation.** At 312 m (suppression on, s = 1), w_e rises steeply from 4.5 to 8.1 mm s⁻¹ between targets 20 and 100 cm⁻³. Above 100 cm⁻³ it rises only from 8.1 to 8.6 mm s⁻¹ (`explore_scalars.csv`). The steep part coincides with the collapse of surface precipitation, and it occurs equally with suppression off, where the rain sink is still substantial at low Nd.

More directly, the w_e difference between suppression on and off (hours 10–12, from `ml_budget.csv`) at targets ≥200 cm⁻³ is:

| Grid spacing | w_e(on) − w_e(off) (mm s⁻¹) |
|---|---|
| 40 km | 0.05–0.11 |
| 5 km | 0.6–0.8 |
| 2.5 km | 1.1 |
| 312 m | 0.3–0.45 |

The "off" runs still drizzle at high Nd (0.4 mm d⁻¹ at 2.5 km). So at grey-zone spacings, drizzle reduces entrainment by up to about 15 %, which is the classic drizzle–entrainment coupling (Stevens et al. 1998; Ackerman et al. 2009). At 40 km it does essentially nothing.

**(c) This coupling is booked as "precipitation suppression" in Eq. (3).** Switching the Nd dependence of autoconversion changes both the precipitation sink (positive for LWP) and the drizzle-mediated entrainment (negative for LWP). The small precipitation-suppression term at fine spacing (0.04–0.10 on the moderate branch, L244) is therefore partly a cancellation between two opposing processes. It does not mean that rain processes stop mattering. At 2.5 km and targets ≥200 cm⁻³, the budget gives on-minus-off changes of:

- **entrainment term:** −8 to −11 g m⁻² h⁻¹;
- **precipitation term:** about +5.5 g m⁻² h⁻¹.

The entrainment response is larger than the direct sink. I ask the authors to:

- rename the first term of Eq. (3) as the effect of the autoconversion Nd dependence, not "precipitation suppression";
- use the budget to split the on–off difference into rain-sink and entrainment parts at each Δx (Section 5, item 4);
- reword the framing (abstract, L104 in Sect. 4.1, conclusion 2) of "precipitation suppression vs entrainment". In this experiment the knob that controls precipitation also controls part of the entrainment.

**(d) The sedimentation effect on w_e at high Nd is small, but sedimentation velocities are not.** At 312 m, changing s from 0.5 to 2 reduces w_e by only 0.3–0.5 mm s⁻¹ (4–6 %) at targets ≥200 cm⁻³. At low Nd the reduction is 1.1–2.4 mm s⁻¹ (Fig. 7a), but there the droplets are 12–17 μm and sedimentation acts like drizzle, as the authors themselves note on the clean branch (L246).

A rough Stokes estimate is informative. I used the domain-mean qc/cf and Nc/cf at the highest level where qc exceeds half its maximum, with a mass-weighted gamma factor of about 1.5. The mass-weighted fall speed at cloud top is then about 15–20 mm s⁻¹ at targets 200 cm⁻³ and about 5–7 mm s⁻¹ at 1000 cm⁻³, at every grid spacing. That is comparable to or larger than w_e (4–8.6 mm s⁻¹). By the Bretherton et al. (2007) argument, sedimentation should then exert strong control on entrainment.

That entrainment responds weakly, and not at all at ≥10 km, suggests that SHOC's cloud-top mixing hardly sees the sedimentation-induced reduction of liquid in the uppermost layer. A 50 m layer and the time-split order of SHOC and P3 are plausible reasons. The P3 sedimentation diagnostic is broken, but the flux can be computed offline from the state (Section 5, item 3). This would turn the claim that results are "consistent with a sedimentation–entrainment feedback" (abstract; conclusion 3) into a test: does Δw_e between s = 0.5 and s = 2 scale with the cloud-top sedimentation-flux difference, and with what efficiency compared with the parameterisation of Bretherton et al. (2007)?

**(e) Put the magnitude of the negative branch in the right context.** L327 compares S ≈ −0.04 with steady-state LES adjustments (Glassmeier et al. 2021) and calls it an order of magnitude smaller. Two more relevant comparisons exist.

- Hill et al. (2009) used bin-microphysics LES of nocturnal, non-drizzling stratocumulus. Raising aerosol from 100 to 1000 cm⁻³, with both the evaporation and sedimentation pathways active, reduced LWP by about 10 %. By my conversion, that is S ≈ ln(0.9)/ln(10) ≈ −0.05 over a few hours of simulation, very close to the 312 m polluted branch.
- Hoffmann et al. (2025) used a mixed-layer model for weakly precipitating stratocumulus and found a slope that falls from positive values to about −0.03 at N = 1000 cm⁻³.

In contrast, the diurnal LES ensemble of Zhang et al. (2024) gives a relationship that becomes increasingly negative through the night and is still about −0.2 in the late afternoon.

So the small magnitude at 312 m is consistent with short, single-case LES and with mixed-layer theory, but much weaker than ensemble-based nocturnal LES estimates. The discussion should separate these comparisons rather than citing a single "order of magnitude".

### M2. Cloud-top processes and the inversion are represented differently at every grid spacing

The paper treats w_e as a physical response that "generally increases" with refinement. The data suggest three distinct numerical regimes.

**(a) Coarse spacing (≥10 km): a grid-locked inversion.** At 40 km, z_i rises from 821 to 865 m over 12 h and asymptotes towards a model level interface. Levels near the inversion are at 828 and 878 m, with Δz ≈ 50 m (`ml_timeseries.csv`; npz `z`). The diagnosed w_e of 3.7–4.0 mm s⁻¹ is therefore close to −w_s(z_i) ≈ 3.2 mm s⁻¹ plus a small residual. It is the same within 0.1 mm s⁻¹ across Nd 100–1000, s = 0.5–2, and suppression on or off, even though surface precipitation varies from 0.01 to 0.83 mm d⁻¹ (Fig. 2c).

A cloud top locked to a level, with entrainment set by subsidence, is a familiar single-column problem with sharp inversions on coarse vertical grids. It is why several boundary-layer schemes use explicit entrainment closures. The conclusion that "entrainment in EAMxx is nearly insensitive to droplet sedimentation" at coarse spacing (L242, L323, L333) may describe this numerical locking rather than SHOC's physics. Please show z_i(t) and the θl profile around the inversion at each Δx, and discuss locking explicitly. The comparison with Mülmenstädt et al. (2024) in Sect. 4.2 depends on this.

**(b) The 10 → 5 km "transition" is a time-dependent unlocking.** The 5 km run at target 200 cm⁻³ follows the 40 km z_i almost exactly for 8 h (821, 827, 838, …, 862 m). Between hours 8 and 12 it breaks away (872, 893, 909, 918 m). The budget-window w_e jumps from 4.3 to 7.3 mm s⁻¹ at the same time (`ml_budget.csv`).

The hour 10–12 analysis window at 5 km therefore captures the run in the middle of a regime change. This likely explains several features:

- the "unexplained" abrupt change between 10 and 5 km (L284, L325);
- the anomalously large w_e at 5 km (Fig. 2c);
- the largest budget errors (mean −4.1 g m⁻² h⁻¹ in the last window, compared with less than 1 elsewhere);
- the stripe-like circulations.

Please show and discuss this. Fig. 4 should mark it, and the 5 km results should be described as transient.

**(c) Sub-km spacing: entrainment that is too efficient for the turbulence present.** I computed:

- w* from the domain-mean boundary-layer-integrated buoyancy flux (SGS plus resolved, from the npz profiles);
- an entrainment efficiency A = w_e z_i Δb / w*³, with Δb approximated from Δθl.

A rises about fourfold across the grid spacings:

| Grid spacing | A | BL-integrated buoyancy flux (K m² s⁻¹) | Total BL w variance (m² s⁻²) |
|---|---|---|---|
| ≥10 km | 0.7–0.9 | 18–23 | 0.33–0.40 |
| 2.5–1.25 km | 1.4–1.6 | | |
| 625 m | 1.9–2.0 | | |
| 312 m | 2.9–3.0 | about 13 | about 0.09 |

So at 312 m, entrainment doubles while the turbulence that should drive it weakens.

In LES, entrainment in nocturnal stratocumulus is controlled by how well the inversion is resolved, and it converges *from above* as the grid is refined. Under-resolved inversions entrain too much and break the deck (Stevens et al. 2005; Pressel et al. 2017; Mellado et al. 2018). Here the vertical spacing at the inversion is fixed at about 50 m (L80), while horizontal refinement lets resolved updrafts overshoot into a two- to four-level domain-mean inversion. The 312 m entrainment rate is 7.4–8.6 mm s⁻¹, compared with 4.5 mm s⁻¹ for DHARMA and 6.0–7.6 mm s⁻¹ observed, and the cloud cover is 0.84 (LWP > 10 g m⁻²) even at high Nd.

This is what a grey-zone model with substantial implicit (numerical) entrainment would produce. The trend from 5 km to 312 m thus runs opposite to how LES approach convergence. The 312 m solution is probably in the most over-entraining part of the grey zone, not on a path towards LES. Because the LWP maximum, and the sign of S, are set by the balance between entrainment and precipitation (Sect. 4.1), the shift of the turning point to about 100 cm⁻³ may be partly a numerical-entrainment effect.

I ask the authors to:

- report an entrainment efficiency normalised by the turbulence or by the radiative driving;
- report the domain-mean inversion thickness and, from the 3D snapshots, the standard deviation of local cloud-top height, against Δx;
- state the above in the abstract and conclusions;
- if at all possible, run one 312 m pair (targets 200 and 1000 cm⁻³) with Δz ≈ 10–15 m near the inversion. This is the single most informative extra experiment.

**(d) η is not "entrainment efficiency".** η = ρ c_p w_e Δθl / F_rad (L266) is the ratio of entrainment warming to radiative cooling. In a steady mixed layer it should equal 1 − (SHF + P)/F_rad, which is about 0.8 at 312 m. Values of 1.2–1.3 therefore mean the layer is warming, and nothing more. The sentence at L264, "the change in w_e mostly reflects a change in entrainment efficiency", needs a definition of efficiency that does not already contain w_e. A buoyancy-flux-based A, as above, or the Nicholls–Turton-type form normalised by the radiative flux jump, would serve.

### M3. The decoupling diagnostic gives the wrong ranking across grid spacings

Decoupling is measured as Δq_t between the lowest and highest quarters of the boundary layer (L125, Fig. 9c). Several problems follow.

**(a) The coarse runs are labelled decoupled but are well mixed by every other measure.** At ≥10 km, Δq_t is 1.2–1.7 g kg⁻¹ at all Nd, the largest values in the study. By other diagnostics these runs are the best coupled:

- the domain-mean buoyancy flux is positive throughout the boundary layer, with its minimum at 75–110 % of the surface value;
- cloud base lies within about 25 m of the LCL of mixed-layer air;
- θl is uniform or decreases slightly upward, so θl(top quarter) − θl(bottom quarter) is −0.9 to +0.2 K in `explore_scalars.csv`.

The Δq_t comes from SHOC carrying the 93 W m⁻² latent heat flux down-gradient through a deep cloud layer, and from the top quarter reaching into the inversion (point c). Jones et al. (2011) required both Δq_t > 0.5 g kg⁻¹ *and* Δθl > 0.5 K. By that two-part criterion, the coarse runs are coupled.

**(b) The sub-km runs at high Nd are more decoupled than Fig. 9c implies.** At 312 m and targets ≥100 cm⁻³, Δq_t is only about 0.3 g kg⁻¹. However:

- the total buoyancy flux has a pronounced minimum of only 8–10 % of its surface value at about 0.55 z_i, just below cloud base;
- cloud base lies 60–80 m above the LCL of 0.1–0.8 z_i air (from `ml_budget.csv`; on average +83 m at 312 m, compared with −25 m at 40 km);
- the w variance profile has separate subcloud and cloud-layer maxima (npz `w2_res`, `w2_sgs`).

By buoyancy flux and cloud base, refinement increases decoupling. By Δq_t, it decreases. Chen et al. (2024) show that the degree of decoupling organises how LWP evolves, both at night and after sunrise. Getting it right therefore matters for the mechanism.

**(c) The top quarter is contaminated by inversion air.** z_i is defined at the midpoint of the θl jump (L125). The domain-mean inversion is one level thick at 40 km but two to four levels thick at fine spacing and low Nd. The 0.75–1.0 z_i layer therefore includes the lower half of the inversion:

- at 5 km and target 20 cm⁻³, θl rises from 289 to 293 K within the "top quarter";
- even at 312 m and target 200 cm⁻³, the level at 980 m has θl = 292.8 K and q_t = 7.3 g kg⁻¹.

Please define the boundary-layer top for this metric as the inversion *base*, or use cloud-layer averages bounded by z_b and the inversion base. Report several metrics side by side:

- Δq_t and Δθl with the Jones thresholds;
- z_b minus the surface-air LCL;
- the minimum, or negative area, of the buoyancy-flux profile below cloud base (Turton and Nicholls 1987; Bretherton and Wyant 1997);
- the w-variance profile.

**(d) "Drizzle decouples the boundary layer at low Nd" (L286) needs a stability signature.** In the domain means I inspected, the subcloud buoyancy flux never becomes significantly negative: the negative area is at most 5 % of the positive area. The positive skewness and the q_t gradient at low Nd are consistent with cumulus-under-stratocumulus. Please show buoyancy-flux profiles (Section 5, item 1) before calling these layers "drizzle-decoupled".

### M4. The mixed-layer budget's validity for decoupled and broken layers

The authors already acknowledge (L157) that the budget is a diagnostic decomposition and loses skill at sub-km spacing. Its construction, however, explains why, and the explanation should be stated and acted on.

- **Cloud base is computed for the wrong air.** z_b is taken as the LCL of the 0.1–0.8 z_i mean. In a decoupled layer, cloud base is set by the cloud-layer air or the updrafts feeding it, not the subcloud-weighted mean. The offset z_b − LCL_ml grows systematically with refinement, from −25 m at ≥10 km to +55, +64, +75 and +83 m at 2.5 km, 1.25 km, 625 m and 312 m (hour 12 windows, `ml_budget.csv`). The predicted dz_b/dt thus responds to changes in subcloud air that the cloud does not see.
- **LWP ∝ h² assumes overcast cloud with a fixed adiabatic fraction.** At 312 m, cloud cover (LWP > 10 g m⁻²) is 0.50–0.85, and on the clean branch half the susceptibility comes from cloud cover (L230).
- **The "entrainment" term mixes deepening and warming/drying.** Entrainment both raises z_i (thickening) and raises z_b (thinning). Showing the two parts separately would help readers judge the net "−27 to −32 % h⁻¹" at 312 m (L275).

I suggest:

- formulate the budget for in-cloud LWP, with a separate cloud-fraction tendency;
- compute the cloud-base sensitivity from cloud-layer thermodynamics, for example the 0.6–0.9 z_i mean or the value at z_b;
- restrict the process attribution to runs and windows classified as coupled by an objective criterion (M3), and report the attribution only where the budget closes;
- alternatively, use a two-layer (decoupled) budget.

In any case, Sect. 3.6 should not attribute the general thinning at 625 m and 312 m to entrainment where the budget sum and the simulated trend differ by a factor of two (625 m, L275).

### M5. The nocturnal-only, constant-forcing design limits generality more than the text admits

The limitations section (L341) mentions the diurnal cycle in one sentence. From the perspective of recent LES work, this is a central limitation, for four reasons.

1. **The analysis window lies in a period that does not occur in nature.** Hours 10–12 come after 10 h of uninterrupted longwave-driven turbulence. At about 30° N in July, the night lasts only about 10 h. The analysis window therefore represents conditions that, without shortwave radiation, would never occur.
2. **The buffering phase is missing.** Zhang et al. (2024) find that in non-precipitating stratocumulus the LWP–Nd relationship becomes more negative through the night and is then buffered after sunrise by cloud-layer shortwave absorption, which depends strongly on LWP. The time evolution at 312 m (S₂₀₀→₁₀₀₀ becoming more negative with time, Fig. 4) agrees qualitatively with the nocturnal phase of that behaviour, which is worth stating. The buffering phase, however, is absent by design.
3. **The daytime response would differ by grid spacing.** Hour-12 LWP differs about fourfold between 40 km and 312 m, and coupling differs too (M3). The daytime thinning would therefore differ strongly between grid spacings (Chen et al. 2024: sunrise LWP, inversion height and decoupling control morning thinning; also Sandu et al. 2008). The resolution dependence of a diurnally integrated S cannot be inferred from these runs.
4. **Both pathways peak at night.** Drizzle in RF02-like clouds peaks at night and entrainment driven by cloud-top cooling is strongest then, so the night-time balance between them need not represent the daytime or daily-mean balance.

Please:

- state in the abstract and conclusions that the results apply to nocturnal conditions;
- expand Sect. 4.4 along these lines;
- consider a minimal diurnal set, for example 5 km, 625 m and 312 m × targets 50, 200 and 1000 cm⁻³, suppression on, s = 1, 36 h with shortwave radiation, which would show whether the resolution dependence persists through one day.

The final sentence of the abstract ("the sign and magnitude … depend on grid spacing across the turbulence grey zone") is fine for this setup, but it should be qualified as nocturnal.

### M6. Comparing the resolution dependence with LES knowledge, and what the 312 m solution is

The manuscript presents the sequence from 40 km to 312 m as progressively resolving the boundary layer. Several 312 m diagnostics, however, are unlike LES of nocturnal stratocumulus:

- the resolved w skewness is positive at all Nd (0.09–0.24 at targets ≥100 cm⁻³), whereas LES and observations of radiatively driven, well-mixed decks show negative skewness in the cloud layer;
- the total boundary-layer w variance (resolved plus subgrid, about 0.09 m² s⁻²) is a factor of 3–4 below the coarse runs;
- a third of the variance is still subgrid, and the mixing length is capped everywhere (L284);
- entrainment efficiency is about 3 (M2c);
- the deck is broken at high Nd.

The authors note some of this, but the discussion still reads as though finer means closer to LES. For example, L268 says "its larger magnitude at fine spacing indicates that the coupling between sedimentation and entrainment is stronger where part of the boundary-layer circulation is resolved".

I recommend:

- add a short paragraph (Sect. 3.8 or 4.1) that states where LES-based expectations place each regime: SCM-like locking (≥10 km); a transitional regime (5–1.25 km); and over-entraining, near-grid-scale convection (625–312 m);
- state that a converged answer for this physics lies beyond a regime in which entrainment must decrease again;
- remove or support the inference at L268;
- for the low-Nd broken cells at sub-km spacing, mention that pockets of open cells were observed during RF02 (Stevens et al. 2005, BAMS), so these features are not unphysical in themselves, whereas the breakup at high Nd is.

---

## 4. Minor comments

1. **Abstract.** "Consistent with a sedimentation–entrainment feedback": add the size of the w_e response to s at high Nd (0.2–0.8 mm s⁻¹), so readers can judge it (M1d).
2. **L62.** Describe the order of the SHOC and P3 calls within a physics step, and whether P3 sedimentation acts on cloud water after SHOC's adjustment. Discuss whether the Δt that co-varies with Δx (100 to 15 s) changes how much cloud-top liquid is sedimented before SHOC re-adjusts.
3. **L64.** Rain fraction = 1 spreads rain over the whole cell and maximises subcloud evaporation where cloud is broken. The agreement of f_evap with observations at 625 m (0.73) may depend on this choice; say so.
4. **L125, z_i definition.** In decoupled runs, the "boundary-layer value below 400 m" is subcloud air (cloud base is 680–730 m at 312 m), so the midpoint is shifted. Test the sensitivity of w_e to an inversion-base or maximum-gradient definition.
5. **L125, decoupling.** State the sign convention of Δq_t (and Δθl, if added).
6. **Fig. 9c.** The 40 km curve is hidden behind 20 km. Add Δθl in a separate panel, or as a second marker, and draw the Jones et al. (2011) thresholds.
7. **Fig. 9b.** Add a profile panel of resolved and SGS buoyancy flux and of w variance at 40 km, 2.5 km and 312 m for targets 20 and 200 cm⁻³. These would support or refute every decoupling statement in the paper.
8. **L264.** Report F_rad by Δx and Nd. At 312 m it is lower (75–81 W m⁻² at targets ≥50) because of reduced cloud cover, and the radiative term in the budget follows from this.
9. **L266–268.** Give the steady-state reference value of η (≈ 1 − (SHF + P)/F_rad) so readers see that η > 1 means warming. Avoid calling η an efficiency (M2d).
10. **L268.** Separate the low-Nd Δw_e(s) (12–17 μm droplets falling at several cm s⁻¹, effectively drizzle) from the high-Nd Δw_e(s) (Bretherton-type). Only the latter is the sedimentation–entrainment mechanism.
11. **L270 / Fig. 8.** Show the entrainment term split into its z_i and z_b parts. State in the caption that the subsidence term is not independent of the entrainment term, because they balance in dz_i/dt.
12. **L229.** "Initial-condition spread … is typically of a few per cent" needs a reference or a number from an existing ensemble.
13. **Sect. 3.10, L308.** "Cloud-top Nd is reduced in thin, evaporating cloud edges". In a model where condensation is size-independent and activation imposes a floor, explain the mechanism. Is it P3's number adjustment when SHOC evaporates cloud water, the fraction weighting of the AeroCom operator, or partial SHOC cloud fraction? This matters for the within-scene slopes.
14. **Fig. 4.** Mark the onset of z_i growth at 5 km (about hour 8) and comment on how it affects S(t) (M2b).
15. **L341.** Add Zhang et al. (2024), Chen et al. (2024) and Hoffmann et al. (2025) to the discussion of diurnal and entrainment-mediated adjustments. They are directly relevant and currently not cited.
16. **Conclusion 4.** "Entrainment drying exceeded the prescribed surface moisture supply" holds with fixed fluxes. Add "with prescribed surface fluxes" here as well as in Sect. 4.4.
17. **Conclusion 1.** "The LWP maximum moved to about 100 cm⁻³": add "in nocturnal, constant-forcing conditions".
18. **Terminology.** Use "sedimentation–entrainment coupling" consistently, rather than alternating with "feedback", unless a closed feedback loop is shown.

---

## 5. Feasible additional analyses with existing output

All of these use files that already exist: the npz profiles, the 15-minute domain means and time series, `ml_budget.csv`, and the 2-hourly 3D snapshots.

1. **Multi-metric decoupling** (npz profiles, `ml_budget.csv`). For every run, report:
   - Δq_t and Δθl with the BL top at the inversion base, against the Jones et al. thresholds;
   - z_b minus the surface-air LCL;
   - the minimum and the negative area of the total buoyancy flux below cloud base, normalised by the surface value;
   - the ratio of cloud-layer to subcloud w variance.

   My rough numbers are in M3. They reverse the ranking in Fig. 9c.

2. **Entrainment efficiency and inversion structure.**
   - A = w_e z_i Δb / w*³ from the integrated buoyancy flux (Δb including the q_t jump).
   - The domain-mean inversion thickness (for example, the 10–90 % θl transition depth) and its number of levels.
   - From the 3D snapshots at ≤1.25 km, the standard deviation of local cloud-top height and the fraction of columns with cloud water in the 50 m layer above the domain-mean z_i.
   - z_i(t) for all Δx, to document locking at ≥10 km and unlocking at 5 km.

3. **Offline cloud-top sedimentation flux.** Compute the P3 mass-weighted fall speed from the state (cloud-top qc, Nc and the P3 shape parameter) and the resulting flux F_sed, using the 3D snapshots or the domain-mean profiles. Test whether Δw_e between s = 0.5 and s = 2 at fixed Nd scales with ΔF_sed, and compare the implied efficiency with Bretherton et al. (2007), at each Δx. This substitutes for the broken P3 diagnostic.

4. **Separate the two roles of the autoconversion knob** (`ml_budget.csv`). For each Δx and Nd, split the on–off LWP-tendency difference into the precipitation-sink term and the entrainment term, including the change in w_e. My numbers at 2.5 km (M1c) suggest the entrainment part dominates at targets ≥200 cm⁻³.

5. **Phase-space view of the transience.** For each Δx, plot dLWP/dt against LWP for the six Nd levels over the 2 h windows, in the style of Glassmeier et al. (2021) and Hoffmann et al. (2020). Estimate where the tendency would vanish and the relaxation time scale. Report S evaluated at these extrapolated "steady" LWPs alongside the hour 10–12 S. This would show whether the sign at 312 m is likely to persist.

6. **In-cloud versus cloud-cover decomposition on all branches** (3D snapshots and 15-minute columns). S = S_cf + S_LWPin at every Δx, with in-cloud LWP and cloud fraction defined at the column scale. Feed the in-cloud LWP into the revised budget (M4).

7. **Budget restricted to coupled windows.** Recompute Table A1 skill and Fig. 8 using only windows classified as coupled by item 1. If skill recovers there, the loss of skill at sub-km spacing is a decoupling issue, not a turbulence-partition issue.

8. **Time evolution against the nocturnal LES picture.** Using Fig. 4 data, compare the rate at which S₂₀₀→₁₀₀₀ becomes more negative through the night at each Δx with the nocturnal phase in Zhang et al. (2024). This can be presented as a model-independent way to show where EAMxx agrees with LES and where it does not.

## 6. Literature

**Verified for this report** (DOIs confirmed on the publisher's page or by DOI search):

- Zhang, J., Chen, Y.-S., Yamaguchi, T., and Feingold, G. (2024), *ACP*, 24, 10425–10440. doi:10.5194/acp-24-10425-2024. Not cited in the manuscript; **recommended**.
- Chen, Y.-S., Zhang, J., Hoffmann, F., Yamaguchi, T., Glassmeier, F., Zhou, X., and Feingold, G. (2024), *ACP*, 24, 12661–12685. doi:10.5194/acp-24-12661-2024. Not cited; **recommended**.
- Hoffmann, F., Chen, Y.-S., and Feingold, G. (2025): On the processes determining the slope of cloud water adjustments in weakly and non-precipitating stratocumulus. *ACP*, 25, 8657–8670. doi:10.5194/acp-25-8657-2025. Not cited; **recommended**.
- Zhang, J. and Zuidema, P. (2019), *ACP*, 19, 14493–14516. doi:10.5194/acp-19-14493-2019. Optional, for the diurnal cycle and decoupling.
- Zhang, J., Zhou, X., Goren, T., and Feingold, G. (2022), *ACP*, 22, 861–880. doi:10.5194/acp-22-861-2022. Optional, for Sect. 4.3.
- Zhang, J. and Feingold, G. (2023), *ACP*, 23, 1073–1090. doi:10.5194/acp-23-1073-2023. Optional, for Sect. 4.3.
- Bretherton, C. S., Blossey, P. N., and Uchida, J. (2007), *GRL*, 34. doi:10.1029/2006GL027648. Already cited.
- Hill, A. A., Feingold, G., and Jiang, H. (2009), *J. Atmos. Sci.* doi:10.1175/2008JAS2909.1. Already cited; use it for the magnitude comparison in M1e.
- Sandu, I., Brenguier, J.-L., Geoffroy, O., Thouron, O., and Masson, V. (2008), *J. Atmos. Sci.*, 65, 2705–2718. doi:10.1175/2008JAS2451.1. Already cited.
- Glassmeier, F., et al. (2021), *Science*, 371, 485–489. doi:10.1126/science.abd3980. Already cited.
- Stevens, B., et al. (2005), *Mon. Wea. Rev.*, 133, 1443–1462. doi:10.1175/MWR2930.1. Already cited.
- Ackerman, A. S., et al. (2009), *Mon. Wea. Rev.*, 137, 1083–1110. doi:10.1175/2008MWR2582.1. Already cited.

**Standard references suggested but not verified here** (the authors should check the details before citing):

- Stevens, B., et al. (2005): Pockets of open cells and drizzle in marine stratocumulus. *BAMS*, 86, 51–57. Supports the point that POCs were observed during RF02.
- Turton, J. D. and Nicholls, S. (1987), *QJRMS*, on the decoupling of stratocumulus.
- Grenier, H. and Bretherton, C. S. (2001), *Mon. Wea. Rev.*, on the representation of inversions and explicit entrainment closure in single-column models.
- Savic-Jovcic, V. and Stevens, B. (2008), *J. Atmos. Sci.*, on LES of RF02 with drizzle and mesoscale organisation.

*Sources consulted for the persona check:* [NOAA CSL staff page](https://csl.noaa.gov/staff/jianhao.zhang), [CIRES profile](https://cires.colorado.edu/people/jianhao-zhang), [ACP 24, 10425](https://acp.copernicus.org/articles/24/10425/2024/), [ACP 24, 12661](https://acp.copernicus.org/articles/24/12661/2024/), [ACP 19, 14493](https://acp.copernicus.org/articles/19/14493/2019/), [ACP 22, 861](https://acp.copernicus.org/articles/22/861/2022/), [ACP 23, 1073](https://acp.copernicus.org/articles/23/1073/2023/), [ACP 25, 8657](https://acp.copernicus.org/articles/25/8657/2025/).
