# Editor's decision letter (AI-simulated panel)

*AI-simulated review for internal use. The five reports were written by AI agents. Each one's perspective was informed by the published work of the named scientist; they are not those scientists' views.*

**Manuscript:** "Horizontal resolution dependence of the liquid water path response to droplet number in doubly periodic EAMxx simulations of drizzling stratocumulus"
**Decision:** Major revision. All five reviewers (A–E) recommend major revision.

The panel agrees that the 288-run matrix is valuable, carefully documented and worth publishing. The panel also agrees that the paper's explanation of why the LWP response changes with grid spacing does not yet rest on diagnostics that test the proposed mechanisms. Below I group the reviewers' requests by priority. Unless a request says otherwise, it can be met with the existing output; new simulations are to be listed as future work, not promised.

## Priority 1: what the paper reports and how it is framed

1. **Base-state regime as the organising variable (B M5, A, D, E).** Across all 24 combinations of grid spacing and sedimentation factor, S₁₀₀→₂₀₀ correlates at r ≈ 0.91 with ln(surface precipitation / entrainment drying) of the Nd-100 run (B). Grid spacing appears to act mainly by changing the base-state cloud: thickness, rain and the rain-to-entrainment-drying ratio. Make S against regime, pooled over all runs, a central figure, and recast "resolution dependence" as "dependence on the simulated cloud regime, which grid spacing controls in EAMxx".
2. **Time evolution and transience (C, B M6, E).** Present S(t) as a main result. At 2–4 h, S₁₀₀→₂₀₀ is about 0.11 at every spacing from 40 km to 2.5 km; the trend with grid spacing builds over the run (C). Show where the LWP maximum sits over time, the dLWP/dt–LWP phase plane and steady-state extrapolations with uncertainty (C). Contrast the quasi-steady coarse runs with the transient fine runs, whose relaxation time is about 74 h (B). Compare with LES ensembles at the same time after perturbation (C). Describe every result as nocturnal and as a snapshot of an adjustment still under way at 11 h.
3. **In-cloud versus cloud-fraction terms; cloud-top Nd; forcing relevance (A, D, B).**
   - Split S into an in-cloud LWP term and a cloud-fraction term on every branch. At 312 m the clean-branch S is 0.71 all-sky but 0.19 in-cloud (D); the cloud-fraction share of the clean-branch response grows from 0 to 0.53 (A).
   - Use cloud-top Nd, which varies little across grid spacing, as the denominator for comparisons across resolutions.
   - Translate S into d ln τ/d ln Nd = 1/3 + (5/6)S (B), and add an offline albedo split into Twomey, LWP and cloud-fraction terms (A).
   - Report the clean-branch response near the observed RF02 Nd (~55 cm⁻³) prominently (A).
   - Reword the abstract: a sign change in the LWP response is not a sign change in the adjustment forcing (A).

## Priority 2: mechanism and numerics

4. **Is the entrainment change physical? (B M1–M2, E 2).**
   - Inversion vertical spacing stays at ~50 m while Δx shrinks 128×, so numerical mixing at the inversion has to be addressed.
   - Using the 3D snapshots, give an inversion flux budget split into resolved, SHOC and leftover implicit mixing, plus inversion-thickness diagnostics.
   - Resolve the dependence of η on how the jump is defined: Δθ_l taken 100 m above z_i, against the interface jump (B).
   - Report the w*-based efficiency A (E).
   - Describe the three regimes: ≥10 km, where the inversion is pinned to a model level; 5 km, where a circulation develops late and appears stripe-like; and ≤2.5 km.
   - State plainly that 312 m is unlikely to lie on a path to LES.
5. **Drizzle versus sedimentation (E 1, D 5).**
   - The "precipitation-suppression" factor also contains a drizzle–entrainment effect of the opposite sign at fine spacing (E). Separate it using the autoconversion-switch difference, split into a rain-sink part and an entrainment part.
   - Give an offline Stokes estimate of the cloud-top sedimentation flux to stand in for the broken P3 diagnostic (E).
   - Discuss the possible time-step artefact: P3 resets Nd to the CCN floor every step (D).
6. **Robustness (C 5, A 5).**
   - Use the 3D-turbulence pairs as perturbed twins to estimate run-to-run noise (~0.01 in S per C).
   - Add spatial block-bootstrap intervals (A).
   - Replace the autocorrelated 15-min standard deviation with these estimates.
   - Present the polluted-branch sign at ≤2.5 km (negative in 23 of 24 configurations) as the robust result, and the 100→200 sign at 312 m as the fragile one (A).

## Priority 3: diagnostics, case fidelity, structure

7. **Decoupling (E 3).** Δq_t alone ranks the runs backwards. Replace it with several metrics side by side: the buoyancy-flux minimum, cloud base relative to the LCL, and the two-part test of Jones et al. (2011).
8. **Validity of the mixed-layer budget (E 4).** Budget in-cloud LWP plus a separate cloud-fraction term, take cloud base from cloud-layer air, and restrict process attribution to coupled windows.
9. **Case fidelity (B M3, M4, M7).**
   - Prescribed surface fluxes are part of the RF02 protocol, so they are not a departure; correct this, and do not recommend interactive fluxes as a fix.
   - Discuss the radiation treatment without the subsidence-balancing term, the absence of wind and Coriolis, and the drop of Nd with height.
   - Statements about the Ackerman et al. (2009) specification must be checked against the paper.
10. **Satellite section (D 1–4, B).** Either move it to an appendix or redo it with a retrieval-like Nd, a pooled composite, satellite-style filters and an explicit split of the Nd variance. Remove the unsupported caution in Sect. 4.3. Label any satellite comparison as hypothetical, since the case is nocturnal.
11. **Economy and literature.** Build the paper around one mixed-layer argument. Add the verified references the reviewers suggest; each report lists them with DOIs.

## Editorial matters to resolve before submission

- **Authorship and AI-use policy (A, B).** Reviewers A and B note that ACP/Copernicus policy, as they read it, restricts generative-AI text and interpretation, and that COPE does not allow AI authorship. As written, with an AI as sole author and "human review pending", the manuscript would probably be returned without review. **This is for the human study leads to decide.** The revision keeps the author list they specified and flags the issue in the response letter.
- **Data availability.** Archive the output and scripts with persistent identifiers (e.g. Zenodo DOIs).

## Experiments recommended for future work (not required for this revision)

- A paired-perturbation design: spin up at Nd 100, then restart at 200 and 1000 alongside a control, run 24–36 h with seeds (C).
- A 312 m pair with 10–15 m vertical spacing at the inversion (B, E).
- A minimal 36 h set with a diurnal cycle (E).
- Sedimentation factor 0, and a second autoconversion pivot (first referee).
