"""Runnable passive cable check. No active spikes, release, or CA1 cell."""
from pathlib import Path
import json
import numpy as np
from parameters import REFERENCE, EXPERIMENT, GEOMETRY

def simulate(inhibition=False, experiment=None):
    p = dict(EXPERIMENT if experiment is None else experiment)
    names = [s[0] for s in GEOMETRY]
    length = np.array([s[1] for s in GEOMETRY]) * 1e-4  # cm
    diameter = np.array([s[2] for s in GEOMETRY]) * 1e-4
    area = np.pi * length * diameter  # lateral membrane, cm2
    cross = np.pi * (diameter / 2)**2
    capacitance = REFERENCE['Cm_uF_cm2'] * area * 1e3  # nF
    leak = area / REFERENCE['Rm_ohm_cm2'] * 1e6  # uS
    rho = np.array([REFERENCE['Ri_ohm_cm']]*2 +
                   [REFERENCE['axon_Ri_ohm_cm']]*2)
    laplacian = np.zeros((len(names), len(names)))
    for j, section in enumerate(GEOMETRY):
        i = section[3]
        if i is None:
            continue
        resistance = rho[i]*length[i]/(2*cross[i]) + rho[j]*length[j]/(2*cross[j])
        coupling = 1e6 / resistance  # uS; half-section resistances in series
        laplacian[i,i] += coupling
        laplacian[j,j] += coupling
        laplacian[i,j] -= coupling
        laplacian[j,i] -= coupling
    dt = p['dt_ms']
    t = np.arange(round(p['duration_ms']/dt)+1)*dt
    v = np.full((len(t), len(names)), REFERENCE['initial_mV'])
    for k in range(1,len(t)):
        elapsed = t[k] - p['stim_start_ms']
        ge = p['exc_nS']/1000*np.exp(-elapsed/p['exc_tau_ms']) if elapsed >= 0 else 0.
        elapsed_i = t[k] - p['inh_start_ms']
        gi = p['inh_nS']/1000*np.exp(-elapsed_i/p['inh_tau_ms']) if inhibition and elapsed_i >= 0 else 0.
        syn = np.zeros(len(names)); syn[0] = ge; syn[2] = gi
        drive = leak*REFERENCE['initial_mV']
        drive[0] += ge*p['Eexc_mV']; drive[2] += gi*p['EGABA_mV']
        matrix = np.diag(capacitance/dt + leak + syn) + laplacian
        v[k] = np.linalg.solve(matrix, capacitance/dt*v[k-1]+drive)
    return t, v, names

def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    output = Path(__file__).parent/'results'
    output.mkdir(exist_ok=True)
    fig, axes = plt.subplots(2,1,figsize=(9,6),sharex=True)
    for inhibited, ax in zip([False,True],axes):
        t,v,names = simulate(inhibited)
        assert np.isfinite(v).all(), 'Non-finite voltage'
        label = 'with_inhibition' if inhibited else 'baseline'
        np.savetxt(output/f'{label}.csv',np.column_stack([t,v]),delimiter=',',
                   header=','.join(['time_ms']+names),comments='')
        for j,name in enumerate(names):
            ax.plot(t,v[:,j],label=name)
        ax.set(title=label.replace('_',' '),ylabel='Voltage (mV)')
        ax.legend(); ax.grid(alpha=.2)
    axes[-1].set_xlabel('Time (ms)')
    fig.suptitle('Passive cable demonstration — no action potentials')
    fig.tight_layout()
    fig.savefig(output/'passive_comparison.png',dpi=160)
    plt.close(fig)
    (output/'run_parameters.json').write_text(json.dumps(
        dict(reference=REFERENCE,experiment=EXPERIMENT,geometry=GEOMETRY),indent=2))
    print(f'Passive check complete: {output}')

if __name__ == '__main__':
    main()
