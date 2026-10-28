# Starting with the two-compartment CA1 model

Run the simple passive soma–dendrite LIF comparison with Python alone:

```bash
python CA1_reduced_LIF/two_compartment.py
```

This writes voltage/current CSVs and a parameter/spike summary into `CA1_reduced_LIF/results/`. The comparison notebook in this folder plots the same simulations; install matplotlib in your notebook environment for plotting. Its historical filename ends in `brian2`, but it now uses the local Python simulator.

## What is already here

- `../OG-Lowet-ca1.ipynb`: HHca2 is already a two-compartment model. The soma has Na, persistent Na, Kdr, A, M, calcium-related currents and leak. The dendrite has leak and HCN. Default calcium conductance is zero; the displayed simulation also sets persistent Na to zero. It uses RK4 plus stochastic increments, with 8 Hz dendritic and 43 Hz somatic forcing.
- `CA1_03_Reduced_Model_Validation.ipynb`: density-based LIF, adaptation, and separate subthreshold HCN experiments. Previously measured HH rate/CV targets are hardcoded, rather than reproduced from the original here. Treat them as provisional until the exact reference protocol and spike detection are recovered.
- `ceballos_2025_soma_dendrite_lif_parameter_comparison_brian2.ipynb`: absolute-unit passive LIF comparison. Previously referenced a missing experiment package; now runs from the local simulator.
- `../ca3-ais/`: four passive compartments with illustrative geometry, not yet a two-compartment active CA3 model.

## First question: how do leak and coupling affect input location?

The new simulator uses the existing comparison notebook's choices: 200 pF per compartment, leak reversal −70 mV, somatic threshold/reset −50/−65 mV, no refractory interval, and a 400 pA step from 100 to 400 ms. These are exploration settings, not a validated physiological fit.

| Local parameter-set name | Leak per compartment (nS) | Coupling (nS) | Soma injection step rate (Hz) | Dendrite injection step rate (Hz) |
| --- | ---: | ---: | ---: | ---: |
| original | 10 | 10 | 56.67 | 0 |
| paper | 8 | 40 | 53.33 | 26.67 |
| HHca_leak | 10 | 40 | 30.00 | 0 |

Rates are from this simulator at dt = 0.025 ms. `original` names the existing reduced notebook's baseline, not the full Lowet HH model. `paper` is the notebook's inherited mapping label; publication values have not yet been independently verified. The 20,000 µm² effective area is an assumed mapping, not a measured morphology.

The table suggests two experiments: hold leak fixed while varying coupling, then hold coupling fixed while varying leak. Stronger coupling can load the soma during somatic input and improve transfer during dendritic input. This model can explore passive loading, attenuation, and reset-mediated interactions; it cannot establish ionic bursting mechanisms or intrinsic HCN resonance.

## Reference issues to resolve before fitting

The original HHca2 spike list appends every sample above 0 mV. Recompute spikes using upward threshold crossings before fitting firing rates or ISI CV. The external dendritic conductance expression also uses the somatic voltage in its driving force; document and test this separately before enabling that input. Preserve the original notebook as a reference.

Match both baseline currents (`Iapp`, `Iapp2`), stimulus, initial conditions, warm-up, and noise when comparing HH and reduced models. Density-based and absolute-unit models require an explicit area conversion.

## Next steps

1. Reproduce one deterministic HHca2 reference protocol with crossing-based spike detection.
2. Compare the simple model under that same protocol before fitting threshold, drive, or adaptation.
3. Add dendritic HCN as a separate mechanism experiment, with matched resting conditions.
4. Build the analogous soma–dendrite CA3 baseline and verify CA3 source parameters. Keep measured, inherited, and fitted values distinct. Existing CA3 scaffold constants are a starting inventory, not validated two-compartment parameters.

Verification performed: passive steady states agree with the two-node DC solution; an uncoupled soma stays at rest during dendritic injection; halving dt preserves somatic spike counts in all three sets (maximum spike-time shift below 0.4 ms). The local environment now includes plotting dependencies; the passive comparison notebook executes successfully with a noninteractive plotting backend.
