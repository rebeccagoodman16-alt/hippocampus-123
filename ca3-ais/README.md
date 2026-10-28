# CA3 AIS starter

Open this entire folder in VS Code. This project is a small starting scaffold,
with a runnable passive cable demonstration. It is not yet a validated CA3
spiking model or a CA3–CA1 network.

## Setup (macOS / Linux)

Use Python 3.11 or 3.12. In VS Code's terminal, inside this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python simulation.py
```

Choose `.venv` with Python: Select Interpreter. For the notebook choose
Select Kernel > Python Environments > .venv. Open notebooks/start_here.ipynb.
If using Windows, activate with `.venv\Scripts\Activate.ps1` and select
`.venv\Scripts\python.exe` in VS Code.

After a successful local run, capture exact package versions:
```bash
python -m pip freeze > requirements-lock.txt
git init
git add .
git commit -m "Initial CA3 AIS scaffold"
```

## What to edit

- parameters.py: reference constants, illustrative geometry, experiment controls.
- channels.py: deliberate checkpoint for active channel equations.
- simulation.py: physical axial coupling and passive membrane integration.
- results/: voltage CSV files, figure, and run configuration.
- reference_models/: links and notes on the published source.

Run the demo before changing anything. Then change inh_nS or inh_start_ms
and rerun. Inhibition is a prescribed local conductance at the illustrative
AIS, not a simulated chandelier neuron. Geometry and synaptic settings are
demonstration choices, not extracted measurements. Each section is one
cylinder with one voltage node; spatial refinement is a later step.

## Next scientific checkpoint

Reproduce the original NEURON CA3 model in a separate environment. Then
translate and validate its kinetics, add a justified AIS and extended axon,
and test spike initiation and propagation. Add CA1 only after this works.
HCN, Na, K, calcium, and Kv7 currents are not active in the passive demo.
There are no spikes or conduction-failure measurements yet.

For the later Brian2 port:
```bash
python -m pip install -r requirements-brian2.txt
```
An optional dependency declaration is included; Brian2 has not been used or
validated by this passive demonstration. No NEURON installation is required
to run the starter.
