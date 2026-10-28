# Hippocampal CA1 and CA3 models

Exploratory CA1 soma–dendrite reductions, the original Lowet HHca2 notebook,
and a passive CA3 scaffold.

## Environment

The current environment uses Python 3.14.2. Create and activate a virtual
environment from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In VS Code, select `.venv/bin/python` as both the Python interpreter and the
notebook kernel. `requirements.txt` lists direct dependencies;
`requirements-lock.txt` captures the installed environment for reproducibility.
The lock reflects this platform and Python version. The virtual environment
itself is excluded from Git.

## Start here

- `CA1_reduced_LIF/CA1_04_Axial_Coupling_Ih_Resonance_Clean.ipynb`: cleaned existing EPSP, axial coupling, Ih, resonance, kinetics, and theta/gamma experiments. Run cells from the top in a fresh kernel. Results export to `ca1_resonance_results/` under the notebook's working directory.
- `CA1_reduced_LIF/ceballos_2025_soma_dendrite_lif_parameter_comparison_brian2.ipynb`: passive parameter comparison using the local simulator (historical Brian2 filename).
- `CA1_reduced_LIF/CA1_03_Reduced_Model_Validation.ipynb`: earlier reduction/adaptation work with provisional HH target measurements.
- `OG-Lowet-ca1.ipynb`: original reference notebook, preserved.
- `ca3-ais/`: passive cable demonstration; see its README for scope and limitations.

Parameters in reduced models include illustrative and effective choices. They
are not all experimentally measured or independently verified paper values.
