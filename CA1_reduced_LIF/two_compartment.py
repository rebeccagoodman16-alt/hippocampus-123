"""Passive soma–dendrite LIF exploration; units: ms, mV, pF, nS, pA.

Parameter mappings are copied from the local Ceballos comparison notebook,
not independently verified against the publication. No active ionic currents.
"""
from dataclasses import asdict, dataclass, replace
import argparse
import csv
import json
from pathlib import Path


@dataclass(frozen=True)
class Parameters:
    cs: float = 200.0
    cd: float = 200.0
    gls: float = 10.0
    gld: float = 10.0
    gax: float = 10.0
    el: float = -70.0
    threshold: float = -50.0
    reset: float = -65.0


PARAMETER_SETS = {
    'original': Parameters(),
    'paper': Parameters(gls=8.0, gld=8.0, gax=40.0),
    'HHca_leak': Parameters(gax=40.0),
}


def simulate(mode='original', *, location='soma', dt=0.025,
             duration=500.0, start=100.0, end=400.0, current=400.0,
             spiking=True, coupling=None):
    """Forward Euler with simultaneous voltage updates and somatic reset.

    No refractory period, matching the local comparison notebook. State is
    recorded after reset; action-potential waveforms are not represented.
    """
    p = PARAMETER_SETS[mode]
    if coupling is not None:
        p = replace(p, gax=coupling)
    if location not in ('soma', 'dendrite'):
        raise ValueError('location must be soma or dendrite')
    if dt <= 0 or duration <= 0 or not 0 <= start <= end <= duration:
        raise ValueError('require dt > 0 and 0 <= start <= end <= duration')
    if p.gax < 0:
        raise ValueError('coupling must be nonnegative')
    # Conservative Euler stability restriction for the passive two-node system.
    if dt >= min(p.cs/(p.gls+2*p.gax), p.cd/(p.gld+2*p.gax)):
        raise ValueError('dt too large for this passive system')
    vs = vd = p.el
    rows = [(0.0, vs, vd, 0.0, 0.0, 0.0)]
    spikes = []
    for i in range(round(duration/dt)):
        tm = i*dt
        drive = current if start <= tm < end else 0.0
        Is, Id = (drive, 0.0) if location == 'soma' else (0.0, drive)
        axial = p.gax*(vd-vs)
        new_vs = vs + dt*(p.gls*(p.el-vs)+axial+Is)/p.cs
        new_vd = vd + dt*(p.gld*(p.el-vd)-axial+Id)/p.cd
        if spiking and new_vs >= p.threshold:
            spikes.append((i+1)*dt)
            new_vs = p.reset
        vs, vd = new_vs, new_vd
        rows.append(((i+1)*dt, vs, vd, p.gax*(vd-vs), Is, Id))
    return rows, spikes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).parent/'results')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    summary = []
    for mode in PARAMETER_SETS:
        for location in ('soma', 'dendrite'):
            rows, spikes = simulate(mode, location=location)
            name = f'{mode}_{location}'
            with (args.output/f'{name}.csv').open('w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['time_ms', 'vs_mV', 'vd_mV', 'axial_into_soma_pA', 'Is_pA', 'Id_pA'])
                writer.writerows(rows)
            record = dict(mode=mode, location=location, parameters=asdict(PARAMETER_SETS[mode]),
                          dt_ms=0.025, duration_ms=500, step_start_ms=100, step_end_ms=400,
                          step_pA=400, spikes_ms=spikes,
                          stimulus_rate_Hz=sum(100 <= s < 400 for s in spikes)/0.3)
            summary.append(record)
            print(f'{name}: {len(spikes)} spikes; step rate {record["stimulus_rate_Hz"]:.2f} Hz')
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')


if __name__ == '__main__':
    main()
