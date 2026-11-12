# Response to the referee

We thank the referee for a careful, constructive and unusually detailed review. The manuscript has been substantially revised. No new simulations could be run during the revision, because the GPU system was unavailable. Where the referee asked for new runs, we did three things instead:

- reframed the claims so that they follow from the existing runs;
- added every analysis that the existing output allows (CPU nodes only);
- listed the required experiments explicitly in Sect. 4.4 and in the conclusions.

The authorship has changed. The manuscript is now authored by an AI system (Claude, Anthropic). It designed and carried out the analysis and wrote the text at the direction of N. Mahfouz and J. Mülmenstädt, who designed the experiments and are acknowledged; N. Mahfouz is the contact for correspondence.

New scripts are `manuscript/scripts/revision_analysis.py`, `cloudcover_3d.py` with `cloudcover_job.sh`, `make_figures_rev.py` and `finalize_bib.py`. New tables are in `dp_screamxx_sedps_12h/manuscript/tables/`:

- `obs_comparison.csv`
- `budget_skill.csv`
- `matched_nd.csv`
- `shocmix.csv`
- `dwe_sed.csv`
- `nd_stability.csv`
- `sfcflux_feedback.csv`
- `deposition.csv`
- `scene_se.csv`
- `interaction.csv`
- `cloudcover_3d.csv`

## Summary of main changes

- **New title:** "Horizontal resolution dependence of the liquid water path response to droplet number in doubly periodic EAMxx simulations of drizzling stratocumulus". This follows the referee's first suggestion: it names the model, and it drops "decides" and "microphysical pathway".
- **Abstract:** rewritten (249 words). It restricts the claims to EAMxx, presents the 312 m negative branch as a weak tendency in single, transient runs, removes "reproduces … (correlation 0.88)", and states the mixing-length limit.
- **New comparison with RF02 observations and published simulations** (Sect. 3.1, Table 3). The comparison uses values verified from Wyant et al. (2007) and its sources (Faloona et al., 2005; vanZanten et al., 2005).
- **Factorial decomposition with an explicit interaction term** (Eq. 9, Fig. 5), with the pivot dependence stated in Methods, Results, Discussion and Conclusions.
- **Mixed-layer budget reframed as a diagnostic decomposition.** It now has per-resolution skill and skill for Nd anomalies (Appendix A, Table A1, Fig. A1), and Fig. 8 shows six grid spacings with RMSE shading.
- **New diagnostics** for the SHOC mixing-length cap and for the height dependence of the activation floor (Appendix B, Fig. A4). Subgrid-inclusive cloud cover and comparisons at matched diagnosed Nd were also added (Figs. 1, 10; text).
- **GCM/GSRM implications removed or softened.** Literature mischaracterisations were corrected, missing references added (all verified against Crossref) and uncited .bib entries removed.
- **Prose rewritten in conventional ACP style.** There are no bullet lists outside the numbered conclusions and no bold run-in headings, and the referee's suggested rewrites were adopted.

## Major comments

**M1. Factorial decomposition.**
- (a) *Pivot dependence.* Accepted. Sect. 2.1 now gives the off/on autoconversion ratio, (Nd/63)^1.79: 0.13 at 20 cm⁻³ and about 140 at 1000 cm⁻³. Sect. 2.5 states that the off runs at 40 km and target 1000 precipitate 0.83 versus 0.01 mm d⁻¹ (on), while at 312 m they precipitate 0.01–0.17 mm d⁻¹. The attribution at coarse spacing is now described as specific to this design and not pivot-independent (Sects. 2.5, 3.5, conclusion 2).
- (b) *Interaction term.* Accepted. Eq. (9) now decomposes S_on(1) into four terms:
  - precipitation suppression at s → 0 (a_on − a_off);
  - sedimentation with suppression off (b_off);
  - interaction (b_on − b_off);
  - residual (a_off).

  Fig. 5 shows all four. The interaction is −0.07 to −0.08 on the moderate branch at ≥10 km. dS_on/ds is −0.10 at 40 km versus −0.04 at 312 m, and this is stated. We checked two candidate mechanisms for the coarse-resolution sensitivity:
  - w_e changes by less than 0.6 mm s⁻¹ with s at ≥10 km (new Fig. 7a).
  - Estimated droplet deposition at the lowest level is negligible except in one corner of the matrix: ≥10 km, Nd 20, s = 2, suppression off, where it is up to 0.25 mm d⁻¹, about 20 % of surface precipitation (`deposition.csv`).

  We therefore state that the coarse-resolution sensitivity depends on the autoconversion formulation, and that its mechanism was not isolated. The statements at old L303, L407 and L417 were removed.
- (c) *Sign at 2.5–1.25 km.* Accepted. The text now states that S₁₀₀→₂₀₀ increases with s at 2.5 and 1.25 km (0.09 → 0.23, 0.06 → 0.20). The "steepens with sedimentation" statement is restricted to S₂₀₀→₁₀₀₀ at ≤2.5 km and to S₁₀₀→₂₀₀ at 312 m.
- (d) *Extrapolation to s = 0.* The extrapolation and its single residual degree of freedom are stated as a caveat in Sect. 2.5, and the convex clean-branch S_off is noted in Sect. 3.5. The RMS-based linearity claim was removed. Running s = 0 directly is listed as a required experiment.
- (e) *Different denominators.* Stated in Sect. 2.5.
- *Requested runs* (s = 0, second pivot, 2 × 2 design): not possible. They are listed in Sect. 4.4 and the conclusions.

**M2. Mixed-layer budget.**
- (a) *Circularity.* Sect. 2.6 now states that d z_i/dt equals the simulated value by construction, that only the cloud-base tendency and the LWP–h relation are predicted, and that the budget is a diagnostic decomposition.
- (b) *Skill.* We reproduced the referee's per-resolution statistics and tabulate them in Table A1, raw and for Nd anomalies, over all windows and for hours 10–12. Fig. A1 now shows Nd anomalies by resolution. Fig. 8 shows 40 km, 5 km, 2.5 km, 1.25 km, 625 m and 312 m with ±RMSE shading. The abstract no longer quotes r = 0.88.
- (c) *Nd dependence within the noise.* Accepted. Sect. 3.7 now states that at ≤2.5 km the net Nd dependence of the budget sum is no larger than the budget error. It also notes that the entrainment term is non-monotonic in Nd, and that the budget does not establish which process sets the small negative S at sub-km spacing. The 625 m mismatch (−5.4 to −5.7 versus −1.9 to −2.9 % h⁻¹) is reported.
- (d) *Mixed-layer assumptions.* Stated in Sect. 2.6.
- *Separate in-cloud/cloud-cover budgets and an independent w_e (flux-jump):* not done. The needed resolved fluxes at z_i are output only as 2-hourly snapshots. We note this as a limitation; the budget is framed as diagnostic only.

**M3. Model-specific grid dependence.**
- (a) *SHOC length-scale cap.* Accepted and quantified. From the EAMxx source, SHOC receives `dx_short` from HOMME. For the planar element this is the element length divided by 3, i.e. the nominal Δx, not the physics-column spacing. From the horiz_avg output (new Fig. A4a, `shocmix.csv`), the domain-mean mixing length is within 5 % of the cap at 90 % of boundary-layer levels at 312 m, at 25 % at 625 m, and at none at ≥1.25 km. This is stated in Sects. 2.1, 3.8, 4.1, 4.4, the abstract and the conclusions. A run with a relaxed cap is listed as required.
- (b) *Time step and radiation interval.* Now stated in Sect. 2.3 (radiation interval from 300 to 45 s) and as a limitation. The physics-to-dynamics ratio (12 versus 24) is explained.
- (c) *10 → 5 km transition.* Accepted. Sect. 3.2 notes the stripe-like structures at 5 km, with a wavelength of about six physics columns, which suggest partly numerical circulations. Sect. 3.8 shows that SHOC's mixing length at 5 km is about two thirds of that at 10 km although the cap is inactive, and states that the transition was not diagnosed further. The 10 km runs are no longer grouped with 20–40 km at high Nd: the column LWP SD reaches up to 27 g m⁻² at 10 km versus at most 5 g m⁻² at 20–40 km. The statement that the partly resolved circulation "entrains more efficiently" was removed. The w snapshots at 5 km were not analysed further.
- (d) *Mesoscale peak.* The text now states that the peaks at 5 and 2.5 km (6.4 and 8 physics-column spacings) are probably limited by the dycore's effective resolution, and that λ is quantised at 240/n km. The Fig. 9d annotation "domain-limited" was removed.

**M4. Prescribed surface fluxes, no Coriolis.** Interactive-flux runs were not possible. We added a quantitative bulk estimate (Sect. 4.4, `sfcflux_feedback.csv`). It scales LHF with q_s(SST = 292 K) − q_t and SHF with SST − T_air, calibrated to the prescribed fluxes and the initial mixed layer. The estimated fluxes are:
- 88–103 and 6–10 W m⁻² at 312 m;
- 77–79 and 17–20 W m⁻² at ≥10 km.

The feedback would therefore reduce warming at fine Δx, but the latent heat flux would remain below the 105–131 W m⁻² of entrainment drying at 312 m. The absence of Coriolis force and wind nudging, the decaying shear, and the choice of a 12 h duration are now described in Sect. 2.2.

**M5. Evaluation against observations.** Added as Sect. 3.1 and Table 3. Hours 4–6 at target Nd = 50 (diagnosed 42–67 cm⁻³) are compared with the observations and with the DHARMA LES and SCM ranges, all taken from Wyant et al. (2007, Table 2 and text, which we read in full):
- observations: LWP 100 ± 20 g m⁻², w_e 6.0–7.6 mm s⁻¹ (Faloona et al., 2005), surface precipitation 0.35 mm d⁻¹, evaporated fraction 0.73;
- DHARMA LES: LWP 144 g m⁻², w_e 4.5 mm s⁻¹;
- SCMs: LWP 30–162 g m⁻², w_e 1.5–6.8 mm s⁻¹.

We could not obtain the full text of Ackerman et al. (2009), because the publisher and repository blocked automated access. We therefore cite it only for its abstract-level conclusions: the ensemble LWP is consistent with the measurements, the entrainment rate lies at the low end of the measured range, and precipitation is underestimated. The ≥5 km runs resemble the LES in LWP and w_e, the 312 m runs entrain at the upper end of the observed range, and the 625 m runs are closest overall. No grid spacing matches all observed quantities. The LCL of the initial mixed layer (about 400 m) is given. An LES with the same physics is listed as missing.

**M6. Robustness at 312 m.** Accepted throughout. The LWP differences (2.6 and 4.1 g m⁻², 3.4 %) are now quoted and compared with the hourly drift (4–6 % h⁻¹) and with typical ensemble spread. The temporal-sampling SD is described explicitly as not an uncertainty estimate. The non-levelling of S(t) is stated, including the increase of S₁₀₀→₂₀₀ at 1.25 km and 625 m. The abstract and conclusions now describe the negative branch as weak, with a sign that is not established. Ensembles and 24 h runs are listed as required.

**M7. Definitions.**
- (a) *Cloud cover.* We computed maximum-overlap and random-overlap cloud cover from SHOC's cldfrac_liq in the 3D snapshots (`cloudcover_3d.csv`). The subgrid-inclusive cloud cover is also 1.00 at ≥10 km, so the coarse value is not an artefact of the LWP threshold. At 312 m it is 0.92 instead of 0.84 (0.68 instead of 0.50 at target 20). The cloud-cover part of S₂₀→₅₀ at 312 m becomes 0.33 instead of 0.53. Both definitions are reported, and Fig. 10b uses the maximum-overlap definition.
- (b) *Fixed target Nd.* Cross-resolution comparisons now use values interpolated in ln Nd to fixed diagnosed Nd (`matched_nd.csv`). This applies to:
  - LWP at 200 cm⁻³ (Sect. 3.2);
  - the precipitation-suppression gain at a diagnosed Nd of 500 cm⁻³ (110 → 6 g m⁻²);
  - the convergence percentages (10–23 % and 21–40 %);
  - Fig. 10.

  Table 4 (LWP at target Nd) keeps target values and says so in its caption.
- (c) *Nd above target.* Explained from the code and output. P3 sets the in-cloud Nd to max(Nd, factor × CCN), and the prescribed CCN decreases with height. For target 200 the floor falls from about 345 to about 150 cm⁻³ between 300 and 900 m (Fig. A4b). Low clouds at coarse Δx therefore have higher Nd, and small SHOC cloud fractions near cloud base inflate in-cloud values further. The temporal stability of diagnosed Nd is now reported (ratio 12 h/6 h of 0.83–1.08 at ≤5 km and 0.97–1.25 at ≥10 km).
- (d) *Entrainment rate.* The windows (8–12 h fits versus 2 h windows in the budget) and the quantisation of z_i (rises of about 70 m versus about 200 m over 12 h) are stated in Sect. 2.4 and in the caption of Fig. 8.
- (e) *Surface rain includes droplet sedimentation.* P3 does not output separate surface fluxes. We estimated droplet deposition at the lowest level, using the Stokes speed of the mean-volume radius as a lower bound. It is negligible except at ≥10 km, Nd 20, s = 2, suppression off (≤0.25 mm d⁻¹, about 20 %). This is reported in Sects. 3.5 and 4.4.
- (f) *Resolved versus SHOC variance.* The caveat that SHOC's w² is diagnosed from TKE is stated in Sect. 2.4.

**M8. Satellite section.**
- (a) The "retrieval proxy" framing was dropped: the quantity is called model-diagnosed cloud-top Nd, and the text states that the agreement follows largely from the near-constant ratio and says nothing about retrieval errors. The pixel-scale LWP point is mentioned in Sect. 4.3. A MODIS-like retrieval was not implemented.
- (b) The within-scene analysis is now restricted to Δx ≤ 5 km, with standard errors over instants (Fig. 11c). The reported range is now −7.9 to +3.4.
- (c) A short mechanistic explanation of the sign change was added: drizzle depletion in thick cloud versus evaporation at thin cloud edges, and their dependence on resolution.

**M9. GCM/GSRM implications.**
- (a) The GCM analogy was removed. Sect. 4.2 states explicitly that the coarse runs are not representative of GCM columns and draws no conclusions about GCM behaviour.
- (b) Mülmenstädt et al. (2024, ACP 24, 13633) is now described correctly. It found sedimentation-mediated entrainment active in E3SM SCM physics and concluded that GCM physics can represent the coupling. It is credited as the methodological precedent for the sedimentation-factor design (Introduction and Sect. 2.1) and discussed in Sect. 4.2.
- (c) All claims are restricted to EAMxx/SHOC. Other closures are mentioned (Boutle et al., 2014; Efstathiou and Beare, 2015).

## Minor comments

1. Abstract and Sect. 3.6 now give the rain-production decrease "at 200 cm⁻³" (twentyfold) and the smaller decrease at target 20 (2.0 → 1.2 mm d⁻¹).
2. Abstract: "entrainment generally increased". Sect. 3.3 gives the non-monotonic values (5 km > 2.5 km).
3. The abstract now says "288 doubly periodic simulations". The 71 completed 3D-turbulence runs are described in Methods and Appendix C.
4. The abstract has been reduced to 249 words with fewer numbers.
5. Reworded. bogenschutz2023 (JAMES, doubly periodic) and bogenschutz2023rrm (GMD, regionally refined) are now distinguished.
6. The verification is now stated: P3's vapour–liquid exchange equals its rain evaporation at every level (checked in horiz_avg output).
7. Checked in the source. The P3 autoconversion subgrid-variance scaling is disabled (`sgs_var_coef = 1`). This is stated in Sect. 2.1, with its resolution-dependent implication noted in Sect. 4.4.
8. Corrected. 63 cm⁻³ is no longer called the geometric centre; matching is at a diagnosed Nd; the observed 55 cm⁻³ is mentioned.
9. The off/on autoconversion ratio is now given, and the "leaves rain intact" statement was corrected.
10. One of the two runs (312 m, Nd 1000, s = 1, suppression off, 3D turbulence on) completed during the revision and is now included. The other (s = 2, suppression on) had completed only 1 of 12 segments and is excluded. The text says 71 of 72, and the "time of writing" phrasing was removed.
11. The Δt_dyn ratio of 12 versus 24 is confirmed from the run script and explained.
12. The temporal stability of diagnosed Nd is reported (Sect. 2.3).
13. Quantisation of z_b is stated in Sect. 2.4.
14. The sign convention for w_s is stated.
15. Explained in Sect. 2.4.
16. Unified to 13–22 km from runs.csv (12.6–18.5 km at 312 m and 15–21.8 km at 625 m).
17. Rephrased as "small cells of high LWP".
18. 10 km is no longer grouped with 20–40 km at high Nd (see M3c).
19. Changed to "appears only at Δx ≤ 5 km".
20. Corrected (see inconsistency 1).
21. Changed to "decreases monotonically as Δx decreases".
22. Made specific: Glassmeier et al. (2021) concerns non-precipitating Sc evolving over a day or more.
23. Nd ranges are now specified: sedimentation lowers LWP most at Nd 20 (clean branch) and increases LWP more at target 200 than at 1000 (polluted branch).
24. Now quoted for s = 1 with suppression on (12–14 μm). The proxy figure was replaced by the partial dependence on s at fixed Nd (Fig. 7a), which addresses comment 28.
25. Numbers given (67 → 128 W m⁻² at target 200).
26. Ackerman et al. (2004) is now credited for the precipitation-to-entrainment-drying diagnostic (Sect. 3.6 and Introduction).
27. The reference to Table 2 was removed. F_rad values (80–88 W m⁻²) are given in the text.
28. Fig. 7a now shows w_e(s = 2) − w_e(s = 0.5) at fixed Nd. The P3 mass-weighted fall speed at cloud top is not in the output; this is stated as a limitation.
29. See M3a and Fig. A4a.
30. Skewness is computed on the physics grid over the boundary layer (stated). The positive value at 312 m is now discussed as possibly reflecting near-grid-scale updrafts, given the capped mixing length.
31. Skewness is plotted only for Δx ≤ 5 km, and this is stated.
32. The aspect-ratio discussion was revised. Sub-km cells are on the narrow side of observations; the 2.5 km value agrees better but is probably resolution-limited.
33. Rephrased. The weakness of the test is stated (SHOC horizontal diffusion is small relative to dycore dissipation). Hyperviscosity tests are not possible without new runs.
34. Citations added (Honnert et al., 2020; Boutle et al., 2014).
35. Terai et al. (2020) is now correctly characterised (UPCAM, 250 m versus 4 km; weaker positive LWP increase; smaller raining fraction) and compared explicitly in Sect. 4.2.
36. The unsupported "moist free troposphere" claim was removed. The q_t jump (5.8–6.5 g kg⁻¹) is given, and humidity control is cited (Ackerman et al., 2004; Chen et al., 2014).
37. Added: the RF02 LES used Δz ≈ 5 m near the inversion; vertically enhanced physics (Bogenschutz et al., 2023b) is cited; vertical refinement is listed as required.
38. wood2006 was replaced by Kazil et al. (2011, ACP 11, 7491, verified) for aerosol processing.
39. Wang, Wang and Feingold (2003), Bretherton et al. (2007) and Hoffmann and Feingold (2019) were added (verified). Xue and Feingold (2006) and Wang and Feingold (2009) were dropped from that statement.
40. All requested items were added to Sect. 4.4.
41. The appendix on the P3 diagnostic bug was removed and reduced to one sentence in Sect. 2.1. We cannot cite an issue or PR number, because none has been filed to our knowledge.
42. Persistent identifiers are not yet available. The section gives the code branches and states that model output and derived tables are available from the contact on request, as instructed by the study leads.
43. All placeholders and draft notes were removed. The AI-use statement is now factual (author contributions and acknowledgements).

## Technical corrections

- Title and section headings changed as suggested ("Temporal evolution of the susceptibility", "Resolution dependence of the precipitation sink", "Resolution dependence of the dominant adjustment pathway").
- L51 rewritten as suggested.
- SCREAM expansion is "Simple Cloud-Resolving E3SM Atmosphere Model", as in Donahue et al. (2024) and Bogenschutz et al. (2025).
- "Rain fraction set to one" is explained.
- The \gmm macro is used consistently.
- Fig. 1 now uses the perceptually uniform cividis colormap with a 0–300 g m⁻² range. The caption no longer mixes the hour-12 maps with 10–12 h means.
- Fig. 2: distinct markers for 40/20/10 km; the legend is moved outside; panel (d) extends to 10⁻⁴ with clipping stated.
- Fig. 3: the log axis is stated; the error bars are described as temporal sampling only.
- Table 4 (now Table 5): two decimals, "<0.01" where appropriate, header "target Nd at max LWP".
- Fig. 5: interaction term added.
- Fig. 7: redrawn; legend outside; label collisions fixed.
- Fig. 8: six grid spacings, RMSE shading, window difference stated in the caption.
- Fig. 9: caption corrected; "domain-limited" removed.
- Fig. 11c: Δx ≤ 5 km only, with standard errors.
- Fig. A1: redrawn by resolution with Nd anomalies; labels fixed.
- Fig. A3: legends in all panels.
- "inverted-V" is used only as a compound adjective. Target versus diagnosed Nd is defined once in a notation paragraph (Sect. 2.4). Sc/Cu abbreviations were removed. AeroCom, SPA, pg2, IOP and RF02 are defined at first use.

## Verified inconsistencies (Sect. 6 of the report)

All 25 items were checked against the tables and corrected:

1. Off-run LWP description rewritten with the correct values (Sect. 3.3).
2. S(t): 1.25 km and 625 m increase; only 312 m drifts negative on the moderate branch; S₂₀₀→₁₀₀₀ drifts negative (Sect. 3.4). The 2.5 km starting value (+0.04) is also given.
3. Sub-km values corrected to 0.56–0.63; 1.25 km is 0.51.
4. Ratio decrease now given as factors of about 4 (target 20) and about 300 (targets 200–1000).
5. Now 0.011 mm d⁻¹ at target 100 and ≤0.002 mm d⁻¹ above.
6. Now "below 0.2 %".
7. Now 0.28–0.41 m² s⁻².
8. Now "about 40–75 %".
9. Recomputed at matched diagnosed Nd: 10–23 % and 21–40 %.
10. Corrected.
11. Unified to 13–22 km.
12. Rewritten as resolution-limited.
13. Corrected: at 2.5 and 1.25 km the negative S₂₀₀→₁₀₀₀ comes from the interaction and the residual.
14. Corrected with the interaction term.
15. Restricted (see M1c).
16. η and w_e at 5 km reported; the non-monotonic behaviour stated.
17. Removed from the abstract; per-resolution skill tabulated.
18. Radiative +21 to +24 % h⁻¹ for Nd ≥ 50; entrainment values listed and described as non-monotonic.
19. Restricted to ≤5 km; the new range is −7.9 to +3.4.
20. Now 0.12 → 0.24–0.27.
21. Now 0.21–0.64 g kg⁻¹.
22. Table reference removed.
23. Caption corrected.
24. Corrected.
25. Confirmed and explained.

## Literature

- **Corrected characterisations:** Ackerman et al. (2004), Mülmenstädt et al. (2024, ACP 24, 13633), Terai et al. (2020), Sato et al. (2018), Toll et al. (2019; "about a quarter of the Twomey cooling"), Gryspeerdt et al. (2019; upper bound), Glassmeier et al. (2021), and the Bogenschutz et al. (2023) DP versus RRM papers.
- **Added and verified against Crossref:**
  - Wyant et al. (2007)
  - Boutle et al. (2014)
  - Wang, Wang and Feingold (2003)
  - Beare (2014)
  - Efstathiou and Beare (2015)
  - Hoffmann and Feingold (2019)
  - Kazil et al. (2011)
  - Wang, M. et al. (2011)
  - Faloona et al. (2005)
  - vanZanten and Stevens (2005)
  - Mahfouz et al. (2024, ACP 24, 7253)
  - Mahfouz et al. (2025, ACP 25, 15105)
  - Bogenschutz et al. (2025, JAMES, DP-SCREAMv1)
  - Stanford et al. (2026, EGUsphere)
- **Now cited:** Chen et al. (2014) and Ghan et al. (2016).
- **Removed from the .bib:** entries that are not cited (the .bib now contains exactly the 90 cited entries). This includes bryan2003, christensen2022, feingold2010, lu2005, matheou2011, mulmenstadt2021, seifert2015, stevens2003entr, xue2006 and wang2009. Faloona et al. (2005) is used for the observed entrainment rate instead of Stevens et al. (2003, QJRMS), which concerns RF01.
- **Not added:** we did not add the Beare-type references beyond the two verified ones.

## Requested experiments not performed (listed in Sect. 4.4)

- s = 0
- a second matching Nd for the suppression-off configuration, or a 2 × 2 Nd_auto × Nd_sed/rad design
- initial-condition ensembles at 2.5 km and 312 m
- 24 h runs
- interactive surface fluxes
- common-time-step runs at 40, 5 and 2.5 km
- a relaxed SHOC mixing-length cap at 625 and 312 m
- refined vertical spacing near the inversion
- hyperviscosity/sponge tests
- an LES reference with the same microphysics
- a MODIS-like Nd retrieval
