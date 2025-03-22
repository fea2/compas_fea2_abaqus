from compas_fea2.model import InitialTemperatureField
from compas_fea2.model import InitialStressField


class AbaqusInitialTemperatureField(InitialTemperatureField):
    """Abaqus implementation of :class:`InitialTemperatureField`\n"""

    __doc__ += InitialTemperatureField.__doc__

    def __init__(self, nodes, temperature, **kwargs):
        super(AbaqusInitialTemperatureField, self).__init__(nodes, temperature, **kwargs)
        self._ictype = "TEMPERATURE"

    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        data_section = [f"** Name: {self.name} Type: Temperature Field\n*Initial Conditions, type={self._ictype}"]
        for f in self.field:
            data_section += ["{}-1.{}, {}".format(f.part.name, f.input_key, self._field_value)]
        return "\n".join(data_section)


class AbaqusInitialStressField(InitialStressField):
    """Abaqus implementation of :class:`InitialStressField`\n"""

    __doc__ += InitialStressField.__doc__

    def __init__(self, elements, stress, **kwargs):
        super(AbaqusInitialStressField, self).__init__(elements, stress, **kwargs)
        self._ictype = "STRESS"

    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        data_section = [f"** Name: {self.name} Type: Stress Field\n*Initial Conditions, type={self._ictype}"]
        for f in self.field:
            data_section += [
                "{}-1.{}, {}".format(f.part.name, f.input_key, ", ".join(str(v) for v in self._field_value))
            ]
        return "\n".join(data_section)
