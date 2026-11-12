> **Disclaimer: this is an AI-simulated review written by Claude, not by any real person.** The perspective is modelled on themes in the published work of Hailing Jia. It does not represent that researcher's actual views, and they have neither seen nor endorsed it.

# Referee report: Reviewer D (perspective informed by the published work of H. Jia)

**Manuscript:** "Horizontal resolution dependence of the liquid water path response to droplet number in doubly periodic EAMxx simulations of drizzling stratocumulus", submitted to *Atmospheric Chemistry and Physics*

**Version reviewed:** LaTeX source `sedps_acp_manuscript.tex` (431 lines) and the compiled PDF dated 11 Nov 2026. Supporting tables were in `manuscript/tables/`, run summaries in `analysis_report5/summary_h10-12.csv`, and column-level output in `manuscript/fields/*.npz`.

**How the persona was set up.** A web search confirmed that Hailing Jia (Leipzig Institute for Meteorology, Leipzig University; working with J. Quaas) publishes satellite-based studies of aerosol–cloud interactions. Their topics include: the Nd–aerosol sensitivity and how updraft, precipitation, retrieval error and vertical co-location confound it; satellite sampling biases in RFaci; retrieval artefacts in r_e–AOD relationships; and the non-linearity of the cloud response. I found no first-authored Jia paper that deals specifically with the LWP adjustment. The LWP–Nd parts of this review therefore draw on the wider satellite-ACI literature that Jia's work belongs to and cites. Those papers are listed separately in Sect. 7.

---

## 1. Summary

The authors ran 288 doubly periodic EAMxx (DP-SCREAM) simulations of DYCOMS-II RF02. The design crosses eight horizontal grid spacings (40 km to 312 m), six prescribed-CCN targets (Nd 20–1000 cm⁻³), three cloud-droplet sedimentation factors, and the KK2000 Nd dependence of autoconversion switched on or off. The main findings are:

- At 10–40 km, LWP rises monotonically with Nd (S₁₀₀→₂₀₀ ≈ 0.24–0.27). This response disappears when autoconversion is made Nd-independent.
- As the grid is refined, the cloud thins and lifts, and rain production collapses. The LWP maximum moves to about 100 cm⁻³ at 312 m, with a weak negative branch (S ≈ −0.04 to −0.05).
- A mixed-layer budget links the general thinning to entrainment, but it cannot explain the Nd dependence at sub-kilometre spacing.
- Neither LWP nor S converges.
- Sect. 3.10 and 4.3 compare the result with satellite practice. Model-diagnosed cloud-top Nd gives nearly the same S as layer Nd. Within-scene regressions of column ln LWP on column ln Nd_top, with uniform CCN, give slopes from −7.9 to +3.4 that change sign with grid spacing. The authors present this as a model illustration that spatial co-variability is not the adjustment.

The experiment is carefully designed, the caveats are stated honestly, and the paper is a useful contribution to understanding grey-zone behaviour of ACI in a GSRM. My comments focus on the link to observations, which is where my expertise lies. The paper currently claims relevance to satellite-based LWP–Nd estimates in its introduction, in Sect. 3.10, 4.3 and conclusion 6. In my view that link is underdeveloped, and in one respect it is drawn in the wrong direction. The existing output already supports a much stronger satellite-relevant analysis at little cost, and I give concrete numbers below.

## 2. Recommendation

**Major revision.** The modelling core (Sect. 3.1–3.9) is sound and appropriately hedged. My major concerns are:

1. The satellite-relevant section (Sect. 3.10, 4.3, conclusion 6) needs to be either substantially strengthened with a retrieval-like analysis or reduced to a short, clearly bounded remark.
2. The LWP–Nd responses should be reported in the variables that satellite studies actually use: cloud-top Nd, in-cloud LWP, and cloud fraction separately.
3. The statistical treatment of the within-scene regressions should be revised.

None of this needs new simulations.

---

## 3. Major comments

### D1. The satellite-relevant section, as framed, does not support its own conclusion

Sect. 4.3 concludes that the within-scene results "caution against evaluating the LWP adjustments of kilometre-scale models with satellite statistics that do not account for cloud-controlled Nd variability". I agree with the general concern, which is well established (Gryspeerdt et al., 2019; Arola et al., 2022; Mülmenstädt et al., 2024). These simulations, however, do not show that it matters. To a large extent they show the opposite.

**(a) Within-scene Nd variance is tiny compared with the imposed Nd range.** CCN are prescribed and horizontally uniform, and P3 resets in-cloud Nd to at least the scaled CCN at every step. Cloud-top Nd therefore varies very little within a scene. I computed it from the joint histograms the authors already store (`fields_*.npz`, key `jh`: columns with cf_top > 0.5 and LWP > 10 g m⁻², hours 10–12). For suppression on and s = 1, at Δx ≤ 5 km, the within-scene standard deviation of ln Nd_top is only 0.05–0.13. That is at or below the 0.115 ln-unit bin width, so the true spread may be smaller still. The corresponding standard deviation of ln LWP is 0.5–0.9. An OLS slope equals r·σ_lnLWP/σ_lnNd, so moderate correlations become slopes of ±2 to ±8. The large magnitudes (−7.9, +3.4) mainly reflect the near-zero denominator, not strong co-variability. The correlations (−0.86 to +0.56) are the more meaningful statistic, together with σ_lnNd.

**(b) A satellite-like pooled composite recovers the causal slope.** I pooled the columns of the six Nd runs at each Δx (equal sampling per run, suppression on, s = 1) into one joint distribution. This mimics a composite built from many scenes that differ in aerosol but not in meteorology. I then computed the pooled OLS slope of ln LWP on ln Nd_top and a binned E[ln LWP | ln Nd_top] slope.

| Δx | pooled OLS slope | r | binned slope | between-run slope (geometric-mean LWP of selected columns vs Nd_top) |
|---|---|---|---|---|
| 5 km | 0.23 | 0.40 | 0.22 | 0.24 |
| 2.5 km | 0.18 | 0.30 | 0.17 | 0.19 |
| 1.25 km | 0.14 | 0.25 | 0.14 | 0.15 |
| 625 m | 0.11 | 0.19 | 0.11 | 0.12 |
| 312 m | 0.03 | 0.04 | 0.03 | 0.04 |

(Reviewer's own computation from the authors' stored histograms. The between-run slope is an OLS fit through the six run means. A linear fit across the full 20–1000 cm⁻³ range masks the turnover, which is a separate point; see D4.)

Within-scene co-variability with slopes of ±2 to ±8 thus has almost no leverage in a composite once Nd spans a factor of 50 across scenes. In this experiment, a "satellite" that observed true cloud-top Nd would recover the causal slope (in in-cloud terms). The real observational problem is different, and it is the one this paper could actually address:

- Natural within-scene and between-scene Nd variability that is not aerosol-driven is large. Updraft-dependent activation produces it, as do precipitation scavenging and in-cloud processing.
- Retrieval errors are large: about 78 % per pixel and 54 % for 1° averages (Grosvenor et al., 2018).
- Those errors are correlated with LWP through r_e and τ (Arola et al., 2022; Kokkola et al., 2025).

The authors should either (i) make the variance partition explicit, in the form "cloud-controlled Nd variability matters only when its variance is a non-negligible fraction of total ln Nd variance; here it is X %", or (ii) remove the cautionary sentence. Option (i) is more informative.

**(c) The within-scene Nd variability in this model is not representative of nature.** Activation here does not depend on updraft. The Nd floor is a function of prescribed CCN and SHOC cloud fraction only. In observations, cloud-base updraft (often proxied by cloud-base height or geometric thickness; Jia et al., 2022) raises both Nd and LWP, which produces positive within-scene covariation. That source is missing here. The remaining Nd variability comes from sinks (coalescence, sedimentation, mixing with cloud-free air) and from vertical advection of higher-Nd air from lower levels, where the CCN profile is larger. The statement that "the sign of this covariation changes with grid spacing" (Sect. 3.10, conclusion 6) is therefore a statement about the sink processes of this particular configuration. It should not be generalised to observed within-scene relationships.

**(d) Possible time-step artefact in the within-scene Nd.** In the E3SM master version of P3 I looked at (`p3_main_impl_part1.hpp`), the SPA floor `nc = max(nc, factor·nccn·cld_frac_l)` is applied at the start of P3. Autoconversion, self-collection, accretion and cloud sedimentation then deplete Nd within the same step. If the AeroCom cloud-top fields are sampled after P3, values below the floor reflect single-step depletion, which scales with Δt_phys. Δt_phys falls from 100 s at ≥ 5 km to 15 s at 312 m. The summary file supports this. At 40 km, cloud-top Nd relative to target falls from 0.85 to 0.75 (target 200) and from 0.96 to 0.89 (target 1000) as s goes from 0.5 to 2. At 312 m the same ratio does not depend on s (0.759–0.762). That pattern fits sedimentation removing number from the uppermost layer within a step, an effect that grows with s·v·Δt/Δz. The "drizzle-depletion" negative within-scene slopes at 2.5–5 km (Δt 75–100 s) could therefore partly be a time-step effect. Please state where in the time step the cloud-top fields are sampled, and discuss this possibility. The co-variation of Δt with Δx is already acknowledged for the bulk results; it applies here too.

**Requested:** Reframe Sect. 3.10/4.3 around the variance-partition result (D1a, b). Report σ_lnNd and r alongside slopes. Add the activation and time-step caveats (D1c, d). Revise conclusion 6 and the last sentence of Sect. 4.3 accordingly.

### D2. Report the response in satellite-comparable variables: cloud-top Nd, in-cloud LWP and cloud fraction

Satellite LWP-adjustment studies, and the forcing frameworks that use them (e.g., Bellouin et al., 2020), separate an in-cloud (intensive) LWP adjustment from a cloud-fraction (extensive) adjustment. They regress against retrieved cloud-top Nd. The manuscript uses domain-mean (all-sky) LWP and the layer-median in-cloud Nd, and it partitions out cloud cover only for the clean branch. Recomputing from `summary_h10-12.csv` (suppression on, s = 1; in-cloud LWP = domain-mean LWP divided by the LWP > 10 g m⁻² cover) changes the picture considerably at fine spacing:

| Δx | S_lo all-sky, layer Nd (paper) | S_lo all-sky, Nd_top | S_lo in-cloud, Nd_top | S_hi in-cloud, Nd_top | S_vhi in-cloud, Nd_top |
|---|---|---|---|---|---|
| 40 km | 0.39 | 0.37 | 0.37 | 0.26 | 0.08 |
| 5 km | 0.63 | 0.62 | 0.46 | 0.20 | 0.01 |
| 2.5 km | 0.74 | 0.72 | 0.36 | 0.08 | −0.03 |
| 1.25 km | 0.65 | 0.63 | 0.34 | 0.04 | −0.04 |
| 625 m | 0.76 | 0.75 | 0.35 | 0.01 | −0.04 |
| 312 m | 0.73 | 0.71 | 0.19 | −0.06 | −0.04 |

With suppression off, the in-cloud clean-branch slope at Δx ≤ 2.5 km is negative (−0.04 to −0.17).

Consequences:

- **Clean branch.** At 312 m, about three quarters of the all-sky clean-branch S is a cloud-fraction adjustment (d ln CF/d ln Nd_top ≈ 0.52). The in-cloud LWP adjustment that a MODIS-type analysis would measure is only about 0.19. The headline that "S_lo increases from 0.39 to 0.65–0.76 with refinement" (Sect. 3.3) is largely a cloud-cover result. It should be reported as two terms.
- **High-Nd branches.** Here the cloud-fraction contribution is small (< 0.03, as the authors note), and in-cloud S is slightly *more* negative than all-sky S at ≤ 2.5 km.
- **Cross-resolution comparisons.** Comparisons "at fixed diagnosed Nd" (Sect. 3.2, Fig. 10) use layer Nd, which at coarse spacing is inflated 1.4–1.9× relative to cloud top by cloud-base cloud-fraction effects and the CCN profile. Cloud-top Nd at a given target, by contrast, is nearly independent of Δx (e.g., 151–162 cm⁻³ for target 200 at all spacings). For a satellite reader, comparing at fixed cloud-top Nd, which is effectively fixed target, is the natural choice. It changes the numbers quoted in Sect. 3.2 (for example, "LWP 273 g m⁻² at 40 km vs 73 g m⁻² at 312 m at Nd = 200") and the location of the LWP maximum: 84 cm⁻³ layer Nd ≈ 76 cm⁻³ cloud-top Nd at 312 m.
- **Averaging.** S uses the log of domain means. Pixel-level studies use the mean of ln LWP (geometric mean) or bin-mean LWP. With σ_lnLWP ≈ 0.7–0.9 at fine spacing, these can differ. Please state the averaging used and check its sensitivity.

**Requested:** Add a table (or extend Table 5) with S in in-cloud LWP versus cloud-top Nd, plus d ln CF/d ln Nd_top, for all branches and Δx. Consider showing Fig. 2 against cloud-top Nd, or adding a panel that does.

### D3. "Cloud-top Nd" is not a retrieval, and a retrieval-like Nd behaves differently. This can be shown with existing output.

The authors rightly say that their AeroCom cloud-top Nd is not a retrieval (Sect. 3.10). But the reason satellite S estimates are uncertain is precisely the retrieval: Nd_ret ∝ τ^½ r_e^−5/2, or equivalently ∝ LWP^½ r_e^−3 under adiabatic assumptions. Its errors depend on sub-adiabaticity, vertical r_e weighting, heterogeneity and cloud fraction (Grosvenor et al., 2018; Jia et al., 2022, who found that retrieval biases tend to underestimate the Nd sensitivity, with cloud fraction playing a key role). The model outputs column LWP, cloud-top r_e and cloud-top fraction every 15 min. A column-level adiabatic inversion is therefore possible without new runs.

As a crude, domain-mean illustration, I applied the Grosvenor et al. (2018) adiabatic formula with c_w = 2×10⁻⁶ kg m⁻⁴, f_ad = 1, k = 0.8, Q_ext = 2 and τ = 9 LWP_ic/(5 ρ_w r_e). I used the in-cloud LWP and fraction-weighted cloud-top r_e from `summary_h10-12.csv`. This is *not* a substitute for a pixel-level analysis, but it shows the size of the issue:

- **Nd-dependent bias.** Nd_ret/Nd_top decreases with Nd: from 2.2 (target 20) to 0.8 (target 1000) at 40 km, and from 4–5.6 to 1.0–1.2 at Δx ≤ 5 km. The bias is Nd-dependent, much like the sub-adiabaticity bias that Kokkola et al. (2025) found in LES.
- **Effect on S.** Using Nd_ret instead of Nd_top changes in-cloud S by large amounts. S_hi at 5 km goes from 0.20 to 0.35, and S_lo at 40 km from 0.37 to 0.50. On the polluted branch at Δx ≤ 2.5 km the slope becomes about 1.5× more negative (e.g., −0.04 → −0.06 at 312 m). That is the direction expected from correlated retrieval errors (Arola et al., 2022).
- **Re filtering.** At target 20–50 cm⁻³ and Δx ≤ 5 km, 16–56 % of cloudy columns have cloud-top r_e > 15 µm. Many satellite studies exclude such retrievals or precipitating scenes; Jia et al. (2022) showed that including precipitating clouds inflates the Nd–aerosol sensitivity by about 21 %. Retrieval-like filtering would therefore remove much of the clean branch.

These numbers depend on assumptions I cannot check (the vertical weighting of r_e in the AeroCom operator, the subgrid structure of SHOC cloud near cloud top, and the representativeness of domain means of heterogeneous fields). A proper analysis by the authors could, however, quantify how far a retrieval-like Nd distorts the causal S in a setting where the truth is known. That would be a genuinely new contribution relative to Arola et al. (2022) and Kokkola et al. (2025), because it would add the grid-spacing dimension.

**Requested:** Either implement a column-level retrieval-like Nd (minimum: adiabatic inversion of column LWP and r_e_top with standard filters; better: a MODIS-simulator-type diagnostic if available in this EAMxx version) and report S_ret and within-scene and pooled slopes with it, or drop the "satellite-relevant" framing and keep only a short remark. Note also that the case is nocturnal with no shortwave radiation, so τ and r_e are not observable by passive sensors at all. Any satellite analogue is hypothetical and should be labelled as such.

### D4. How the results should, and should not, inform interpretation of observed negative LWP–Nd slopes

The paper compares the simulated negative branch with observed slopes in three places (Sect. 3.3: "an order of magnitude smaller than the observed ones"; Sect. 4.1; Sect. 4.3). Several asymmetries between the two quantities should be spelled out:

1. **The simulated clean branch is purely causal; the observed one is not.** In the simulations, Nd is prescribed between runs, so the positive branch at coarse spacing (S_lo ≈ 0.39) is causal precipitation suppression. In observations, the positive branch at low Nd is partly reverse causality: precipitation scavenges CCN and lowers Nd (Gryspeerdt et al., 2019). Removing precipitating scenes to address this is standard practice (Jia et al., 2022). The model's inverted-V and the observed inverted-V therefore differ in what makes up their left branch. Any resemblance (Sect. 3.3, "resembles the inverted-V shape in satellite composites") is a resemblance of shape only.
2. **The simulated S is at fixed meteorology.** The between-run S is a causal estimate under perfect meteorological control. That is the quantity satellite studies try to approximate by stratifying on EIS, free-tropospheric humidity, cloud-base height and so on (e.g., Chen et al., 2014; Zhang et al., 2022). Observed slopes also contain meteorological co-variability and retrieval artefacts. They are not "an upper bound" in a strict sense; both biases can have either sign (Arola et al., 2022, argue that retrieval errors push slopes negative). Comparing a fixed-meteorology domain-mean S with composite slopes is not like-for-like. Natural-experiment estimates (ship tracks: Toll et al., 2019; Gryspeerdt et al., 2021) and LES ensembles (Glassmeier et al., 2021) are the more appropriate comparison and should be the primary reference in Sect. 3.3 and 4.1.
3. **Timescales.** The runs are 12 h, and S is still evolving at sub-kilometre spacing. Ship-track analyses show that LWP adjustments continue to develop beyond 10 h (Gryspeerdt et al., 2021), and composites mix scenes at all stages. A 12 h snapshot S is closer to an early-time natural-experiment estimate than to a climatological composite.
4. **A single fit hides the turnover.** A single linear fit of ln LWP on ln Nd across 20–1000 cm⁻³ gives a positive slope at every grid spacing: 0.22 at 40 km, 0.21 at 2.5 km, 0.10 at 312 m (pooled over the six run means, s = 1, on). This is so even at 312 m, where the curve has a maximum at about 100 cm⁻³. Satellite slopes are similarly sensitive to whether they are reported as a single regression or as binned, regime-dependent slopes (Gryspeerdt et al., 2019; Possner et al., 2020). Please be explicit that S here is branch-wise and that branch boundaries are a choice.
5. **State dependence.** Perhaps the most satellite-relevant result is implicit. Across Δx and s, the sign and size of S co-vary with cloud state: LWP, thickness, cloud-base height, the precipitation-to-entrainment-drying ratio (Fig. 6c). Observed susceptibilities are also strongly state-dependent (Chen et al., 2014; Zhang et al., 2022, who identify precipitating, thin non-precipitating and thick non-precipitating regimes). If S collapsed onto a function of a cloud-state variable when pooled across Δx and s, the grid-spacing dependence would be mediated by the mean state. Such a result would be directly comparable with satellite stratifications by LWP or precipitation state. If it did not collapse, the dependence would be a structural model effect that satellites cannot diagnose. Either outcome is informative and can be tested with existing output (see Sect. 5, item 5).

**Requested:** Rewrite the comparison with observations in Sect. 3.3, 4.1 and 4.3 along these lines. Make natural experiments and LES the main reference, and present composite slopes as a qualitatively different statistic.

### D5. Statistical methods for the within-scene and branch slopes

**(a) Regression direction and dilution.** Within-scene slopes are OLS of ln LWP on ln Nd_top, but Fig. 11b shows E[Nd_top | LWP], which is the reverse conditioning. Satellite composites usually show E[LWP | Nd] in Nd bins. With σ_lnNd ≪ σ_lnLWP the two regressions differ by large factors. In my pooled calculation the slope implied by the reverse regression (1/b_{lnNd|lnLWP}) was 1.5–13, against 0.03–0.23 for the forward OLS slope. Please either show E[ln LWP | ln Nd_top] in Fig. 11b or make the conditioning explicit, and report r and the ln Nd range for each regression. Measurement noise in Nd attenuates OLS slopes towards zero (regression dilution), while correlated retrieval errors bias them negative (Arola et al., 2022). The model, where the truth is known, is a natural place to show the size of both effects. Adding synthetic multiplicative errors with the Grosvenor et al. (2018) structure to τ and r_e before inversion would do this.

**(b) Selection and truncation.** The regression uses only columns with cf_top > 0.5 and LWP > 10 g m⁻² (`extract_fields.py`). This is not stated in the paper. Selecting on the dependent variable (LWP) truncates its distribution and biases OLS slopes. Selecting on cf_top removes exactly the edge columns that the text invokes to explain the positive slopes at 625/312 m. Please state the criteria and test sensitivity to them, for example with LWP > 0 or > 20 g m⁻² and cf_top > 0.9. The cf_top > 0.9 test is similar to the "overcast pixels only" filter common in MODIS L2 work.

**(c) Uncertainty.** The standard errors (≤ 0.8) are computed as the SD over eight autocorrelated 15 min instants divided by √8, with the columns treated as independent. Both the instants and the spatially autocorrelated columns (cells are 13–48 km across, i.e., many physics columns) make the effective sample size much smaller. Please use a block bootstrap over cells or instants, or report the SD rather than the SE.

**(d) Scale.** Physics columns are 469 m apart at 312 m and 3.75–7.5 km apart at 2.5–5 km, compared with 1 km MODIS pixels. Aggregation changes slopes (McComiskey and Feingold, 2012). Aggregating the 312/625 m columns to about 1 km and about 5 km and repeating the within-scene regression would show whether the sign change with Δx is partly a pixel-scale effect. Comparing all Δx at a common aggregation scale (for example 5 km) would separate "how much is resolved" from "what scale is sampled".

**(e) Branch S and diagnosed Nd.** The between-run S uses controlled Nd, so there is no regression dilution in x. The diagnosed layer Nd, however, comes from two snapshots, while LWP comes from a 2 h mean. The 15-min cloud-top Nd is available continuously and is nearly constant in time. It would be a more consistent and more satellite-like abscissa.

### D6. Scope of conclusion 6 and the abstract

Conclusion 6 states that within-scene slopes "ranged from −7.9 to +3.4 and changed sign with grid spacing". Given D1 (small Nd variance, absence of updraft-driven activation, possible Δt effect) and D5 (selection, dependence on regression direction), this is not robust enough to be a numbered conclusion. I suggest replacing it with the in-cloud/cloud-fraction partition (D2) and, if implemented, the retrieval-like result (D3). Otherwise reword it as: "with horizontally uniform aerosol, the residual within-scene Nd variability is small (σ_lnNd ≤ 0.13) and has negligible influence on composite slopes in this design."

---

## 4. Minor comments

1. **Sect. 2.4, AeroCom operator.** State explicitly that column cloud-top Nd and r_e are obtained by dividing the fraction-weighted sums by cf_top_liq, which the scripts do. Readers familiar with the AeroCom convention will otherwise wonder whether the product is normalised. Also state the vertical extent of the "uppermost liquid layer" (one model level? a τ threshold?). A satellite r_e retrieval weights roughly the top few optical depths, and the depth matters for r_e and hence for any retrieval-like Nd.
2. **Sect. 2.3.** The activation floor depends on cloud-top height through the CCN profile, so cloud-top Nd at fixed target is close to 0.76–0.85 × target at all Δx. Say so. It means cloud-top Nd is effectively the aerosol control variable, which is useful for satellite comparisons.
3. **Sect. 2.4, cloud cover.** Two cloud-cover definitions are used (LWP > 10 g m⁻² and maximum overlap). For comparison with passive satellite cloud masks, an optical-depth threshold (e.g., τ > 1–2) is closer to practice. It can be approximated from column LWP and r_e.
4. **Sect. 3.3, L202.** "the negative slopes are an order of magnitude smaller than the observed ones". Please give the observed values and their source (which product, scale, filters). Note that observed composite slopes and causal S are different quantities (D4).
5. **Sect. 3.3, L211.** The cloud-cover part of S_lo is given only at 312 m. Give it for all Δx and branches (D2).
6. **Sect. 3.10, L308.** "Satellite estimates of LWP adjustments use Nd retrieved from cloud-top effective radius and optical depth under adiabatic assumptions". Add that they also typically use in-cloud LWP derived from the same τ and r_e (LWP ∝ τ r_e). This shared dependence is the source of correlated errors.
7. **Sect. 3.10, L310.** "because cloud-top Nd is reduced in thin, evaporating cloud edges". As far as I can tell, SHOC's saturation adjustment does not remove number when cloud water partially evaporates, and the floor is reapplied every step. Please give the mechanism by which Nd_top falls at edges: dilution by mixing with cloud-free air during advection? cf normalisation? within-step processes?
8. **Fig. 11b.** The 2.5 km, target 200 curve sits at about 0.94 of the scene mean for LWP < 150 g m⁻², rising steeply above that. Please state the number of columns per LWP bin. The rise may rest on few columns.
9. **Fig. 11c.** Add r (e.g., as marker size or a second panel) and σ_lnNd. The x-axis is layer in-cloud Nd while the y-axis uses Nd_top. Use Nd_top on both for consistency.
10. **Sect. 4.3.** "satellite analyses also use in-cloud LWP at pixel scale rather than domain means". Now quantify this (D2).
11. **Sect. 4.1/4.3.** The RF02 inversion jump (Δq_t ≈ 5.8–6.5 g kg⁻¹) and the nocturnal, constant forcing place this case in a specific part of the observed meteorological space (Chen et al., 2014). One sentence placing RF02 within the satellite-observed distribution of free-tropospheric humidity and EIS would help readers judge representativeness.
12. **Abstract.** The abstract does not mention the satellite comparison. That is acceptable if the section is reduced. If it is strengthened per D3, add one sentence.
13. **Wording.** "within-scene covariability" (Sect. 3.10 title) versus "spatial co-variability" (Sect. 4.3). Use one term. "Co-variability" with a hyphen is the more common spelling in this literature.
14. **Fig. 2 and 10.** If the abscissa stays as layer Nd, add a secondary axis or note giving the corresponding cloud-top Nd, which differs by a Δx-dependent factor.
15. **Sect. 3.4 and Fig. 4.** The temporal evolution of S is presented per 2 h window. A satellite sees a single instant. Report the range of single-instant S, which the 15-min output allows, as an indication of snapshot sampling variability.
16. **Sect. 4.2, L333.** "process-level targets ... could help to reduce equifinality". If this sentence stays, say which observable could constrain the precipitation-suppression term (e.g., the precipitation-susceptibility metric of Wood and colleagues, or the dependence of S on precipitation state in satellite composites).

---

## 5. Feasible additional analyses with existing output (no new simulations)

In rough order of value-to-effort. Items 1–2 use only `summary_h10-12.csv`. Items 3–7 use the 15-min `aci2d.INSTANT` and `aerocom.INSTANT` streams already read by `extract_fields.py`.

1. **In-cloud versus cloud-fraction partition** (D2). Compute S(in-cloud LWP, Nd_top) and d ln CF/d ln Nd_top for all Δx, s, suppression settings and branches. Preliminary numbers are in D2. Effort: minutes.
2. **Cloud-top Nd as abscissa.** Redo Fig. 2/10 and the "fixed Nd" comparisons against Nd_top, which is nearly Δx-invariant at fixed target. Effort: minutes.
3. **Column-level retrieval-like Nd** (D3). Compute Nd_ret = f(column LWP, r_e_top) with the adiabatic formula. Apply standard filters (cf_top > 0.9 or overcast; r_e < 15 µm or excluding raining columns if surface rain or RWP is in the stream; τ > 3–5). Report (i) between-run S_ret, (ii) within-scene slopes and correlations with Nd_ret, and (iii) pooled composites. Compare all three with the causal S. This is the analysis that would make the "satellite-relevant" section meaningful.
4. **Synthetic retrieval errors** (D5a). Perturb τ and r_e with multiplicative errors consistent with Grosvenor et al. (2018) before inversion, and show how regression dilution and correlated-error bias move S_ret away from S at each Δx.
5. **State-dependence test** (D4.5). Plot all branch S values (Δx × s × suppression) against mean cloud state: LWP, h, z_b, rain production, P_sfc/(entrainment drying). Test whether they collapse. This connects directly to satellite regime stratification (Zhang et al., 2022; Chen et al., 2014).
6. **Pooled composites and variance partition** (D1b). Pool columns across the six Nd runs, and optionally across s, to build Gryspeerdt-style binned E[LWP | Nd] composites. Report the fraction of ln Nd variance that is within-scene versus between-scene. The stored `jh` histograms are too coarse (0.05 dex in Nd) for clean binned composites; recompute from raw columns.
7. **Aggregation scale** (D5d). Coarse-grain the 312/625 m columns to about 1 km and about 5 km and repeat the within-scene and pooled regressions. Also compare all Δx at a common 5 km aggregation.
8. **Selection sensitivity and robust uncertainty** (D5b, c). Vary the LWP and cf_top thresholds, and use block-bootstrap uncertainties.
9. **Timing of the cloud-top sample** (D1d). Check where in the time step the AeroCom fields are written. Quantify the s- and Δt-dependence of Nd_top relative to the floor; the summary file already shows a 10–13 % s-dependence at 40 km and none at 312 m.

---

## 6. Overall evaluation of the satellite-relevant section

Prescribed uniform CCN plus an activation floor make Sect. 3.10 meaningful only in a narrow sense. It can show what cloud-controlled Nd variability looks like *when aerosol is perfectly uniform and activation is updraft-independent*, and how much leverage that variability has on a composite. The answer to the second question in this design is "very little" (D1b). That is itself a useful, quantitative, and somewhat counter-intuitive result, and it should be stated as such. The section cannot currently speak to retrieval bias, to meteorological co-variability, or to the observed negative slopes. The design has one real strength for satellite questions: the causal S at fixed meteorology is known exactly. Adding a retrieval-like Nd (D3) would use that strength.

---

## 7. Literature

All entries were checked by web search during this review (title, journal, year, DOI).

### 7.1 Papers by H. Jia and co-authors that informed this perspective

1. **Jia, H., Ma, X., Yu, F., and Quaas, J. (2021).** Significant underestimation of radiative forcing by aerosol–cloud interactions derived from satellite-based methods. *Nature Communications*, 12, 3649. https://doi.org/10.1038/s41467-021-23888-1. Shows that satellite sampling, including which cloud-fraction conditions yield retrievals, and the choice of aerosol proxy bias satellite-based ACI estimates. Relevant to D2, D3 and D5b.
2. **Jia, H., Quaas, J., Gryspeerdt, E., Böhm, C., and Sourdeval, O. (2022).** Addressing the difficulties in quantifying droplet number response to aerosol from satellite observations. *Atmos. Chem. Phys.*, 22, 7353–7372. https://doi.org/10.5194/acp-22-7353-2022. Covers updraft (cloud-base height, thickness), precipitation (about +21 % inflation), retrieval errors (underestimation, with cloud fraction playing a key role) and vertical co-location. Relevant to D1c, D3 and D4.1.
3. **Jia, H., Ma, X., Quaas, J., Yin, Y., and Qiu, T. (2019).** Is positive correlation between cloud droplet effective radius and aerosol optical depth over land due to retrieval artifacts or real physical processes? *Atmos. Chem. Phys.*, 19, 8879–8896. https://doi.org/10.5194/acp-19-8879-2019. Retrieval artefacts from partially cloudy and 3-D clouds can greatly overestimate slopes. Relevant to D3 and D5.
4. **Jia, H. and Quaas, J. (2023).** Nonlinearity of the cloud response postpones climate penalty of mitigating air pollution in polluted regions. *Nature Climate Change*, 13, 943–950. https://doi.org/10.1038/s41558-023-01775-5. Non-linear (sigmoidal) cloud responses mean that single log-linear fits mislead. Relevant to D4.4.

### 7.2 Further references cited in this report (verified)

- Arola, A., Lipponen, A., Kolmonen, P., et al. (2022). Aerosol effects on clouds are concealed by natural cloud heterogeneity and satellite retrieval errors. *Nature Communications*, 13, 7357. https://doi.org/10.1038/s41467-022-34948-5 (already cited in the manuscript).
- Kokkola, H., et al. (2025). Model analysis of biases in the satellite-diagnosed aerosol effect on the cloud liquid water path. *Atmos. Chem. Phys.*, 25, 1533. https://doi.org/10.5194/acp-25-1533-2025. LES with UCLALES-SALSA; sub-adiabaticity biases satellite-diagnosed LWP–CCN relationships, and satellite Nd is biased high by 18–40 %. **Not cited; strongly recommended** for D3.
- Grosvenor, D. P., et al. (2018). Remote sensing of droplet number concentration in warm clouds: A review of the current state of knowledge and perspectives. *Rev. Geophys.*, 56, 409–453. https://doi.org/10.1029/2017RG000593. Gives 78 % pixel-level and 54 % 1°-mean Nd uncertainty (already cited).
- Gryspeerdt, E., et al. (2019). Constraining the aerosol influence on cloud liquid water path. *Atmos. Chem. Phys.*, 19, 5331–5347. https://doi.org/10.5194/acp-19-5331-2019 (already cited).
- Gryspeerdt, E., Goren, T., and Smith, T. W. P. (2021). Observing the timescales of aerosol–cloud interactions in snapshot satellite images. *Atmos. Chem. Phys.*, 21, 6093–6109. https://doi.org/10.5194/acp-21-6093-2021. LWP adjustments keep developing beyond 10 h, relevant to the 12 h transience (D4.3). **Not cited; recommended.**
- Gryspeerdt, E., McCoy, D. T., Crosbie, E., et al. (2022). The impact of sampling strategy on the cloud droplet number concentration estimated from satellite data. *Atmos. Meas. Tech.*, 15, 3875–3892. https://doi.org/10.5194/amt-15-3875-2022. On sampling filters for MODIS Nd, relevant to D3 and D5b. **Not cited; recommended.**
- Zhang, J., Zhou, X., Goren, T., and Feingold, G. (2022). Albedo susceptibility of northeastern Pacific stratocumulus: the role of covarying meteorological conditions. *Atmos. Chem. Phys.*, 22, 861–880. https://doi.org/10.5194/acp-22-861-2022. Cloud state (LWP, Nd) dominates susceptibility, with distinct regimes; relevant to D4.5. **Not cited; recommended.**
- McComiskey, A. and Feingold, G. (2012). The scale problem in quantifying aerosol indirect effects. *Atmos. Chem. Phys.*, 12, 1031–1049. https://doi.org/10.5194/acp-12-1031-2012. Aggregation scale changes ACI statistics; relevant to D5d. **Not cited; recommended.**
- Chen, Y.-C., et al. (2014). Satellite-based estimate of global aerosol–cloud radiative forcing by marine warm clouds. *Nature Geosci.*, 7, 643–646. https://doi.org/10.1038/ngeo2214 (already cited).
- Possner, A., Eastman, R., Bender, F., and Glassmeier, F. (2020). Deconvolution of boundary layer depth and aerosol constraints on cloud water path in subtropical stratocumulus decks. *Atmos. Chem. Phys.*, 20, 3609. https://doi.org/10.5194/acp-20-3609-2020 (already cited; DOI as in the manuscript's bibliography).
- Glassmeier, F., et al. (2021). Aerosol-cloud-climate cooling overestimated by ship-track data. *Science*, 371, 485. https://doi.org/10.1126/science.abd3980 (already cited).

---

## 8. Note on the previous referee report and response

I read the earlier report and the authors' response. The response to M8 (dropping the "retrieval proxy" label, restricting to Δx ≤ 5 km, adding SEs, adding a mechanism) was appropriate as far as it went. My comments D1–D3 and D5 are not covered by it:

- the variance-partition and pooled-composite result;
- the in-cloud versus cloud-fraction partition;
- the absence of updraft-dependent activation;
- the possible Δt artefact in Nd_top;
- the regression-direction, selection and effective-sample-size issues;
- a retrieval-like Nd computable from existing output.

I reached these points independently.
