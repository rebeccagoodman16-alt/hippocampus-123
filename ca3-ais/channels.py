"""Active-channel translation checkpoint."""

def active_equations():
    raise NotImplementedError(
        'Translate and validate the reference .mod kinetics first. '
        'Hemond Kdr uses n, not n**4; sodium has m, h, s gates. '
        'No AIS-specific density is supplied by that reference.')
