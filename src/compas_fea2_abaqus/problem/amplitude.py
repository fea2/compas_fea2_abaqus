from compas_fea2.problem import Amplitudes


class AbaqusAmplitudes(Amplitudes):
    """ """

    def __init__(self, multipliers, times, **kwargs):
        super().__init__(multipliers, times, **kwargs)

    def jobdata(self):
        data_amplitude = []
        data_amplitude.append(f"*Amplitude, name={self.name}")
        for multiplier, time in self.multipliers_time:
            data_amplitude.append(f"{time}, {multiplier},")
        return "\n".join(data_amplitude)
