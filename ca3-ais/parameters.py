"""Explicit units; reference values are separate from demonstration geometry."""

# Hemond et al. (2008), ModelDB 101629, ca3b-cell1zr.hoc.
REFERENCE = dict(Cm_uF_cm2=1.41, Rm_ohm_cm2=25370.0,
                 Ri_ohm_cm=150.0, axon_Ri_ohm_cm=50.0,
                 initial_mV=-64.0, ENa_mV=55.0, EK_mV=-90.0,
                 Eh_mV=-30.0, temperature_C=35.0)

# Numerical experiment settings, not biological measurements.
EXPERIMENT = dict(dt_ms=0.025, duration_ms=100.0, stim_start_ms=20.0,
                  exc_nS=2.0, exc_tau_ms=3.0, Eexc_mV=0.0,
                  inh_start_ms=20.0, inh_nS=5.0, inh_tau_ms=8.0,
                  EGABA_mV=-64.0)

# Illustrative cylinders: NOT the reconstructed Hemond morphology.
# Replace these dimensions before interpreting results as CA3 biology.
# name, length (um), diameter (um), parent index
GEOMETRY = [('dendrite', 150.0, 3.0, 1),
            ('soma', 20.0, 20.0, None),
            ('AIS', 40.0, 1.0, 1),
            ('axon', 100.0, 1.0, 2)]

# Figure 9D reference densities in mS/cm2; inactive in passive demo.
REFERENCE_DENSITIES = {
    'soma': dict(gNa=22., gKdr=10., gA=20., gh=0.01),
    'dendrite': dict(gNa=22., gKdr=10., gA=20., gh=0.01),
    'axon': dict(gNa=110., gKdr=10., gA=20., gh=0.),
}
