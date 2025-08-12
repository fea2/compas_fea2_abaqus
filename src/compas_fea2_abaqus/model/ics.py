from compas_fea2.model import InitialTemperature


class AbaqusInitialTemperature(InitialTemperature):
    """Abaqus implementation of :class:`InitialTemperatureField`\n"""

    __doc__ += InitialTemperature.__doc__

    def __init__(self, temperature=None, step=None, inc=None, **kwargs):
        super(AbaqusInitialTemperature, self).__init__(temperature, **kwargs)
        self._ictype = "TEMPERATURE"
        if step:
            self._step = step
        if inc:
            self._inc = inc

    def jobdata(self, nodes):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """

        if getattr(self, "_path", None):  # implementation of temperaturefield via an abaqus file output (.odb)
            if not (self._step) or not (self._inc):
                raise ValueError(
                    "The step and the increment of the field imported from an Abaqus file output must be indicated."
                )
            # data_section = [f"""** Name: {self.name} Type: Temperature Field\n*Initial Conditions, type={self._ictype}, file="{self._path}", step={self._step}, inc={self._inc}, interpolate"""]
            return f"""** Name: {self.name} Type: Temperature Field\n*Initial Conditions, type={self._ictype}, file="{self._path}", step={self._step}, inc={self._inc}, interpolate"""

        data_section = [f"""** Name: {self.name} Type: Temperature Field"""]

        data_section.append("*Initial Conditions, type=temperature")
        for node in nodes:
            data_section.append(f"{node.part.name}-1.{node.key}, {self.temperature}")
        return "\n".join(data_section)

        # for f in self.field:
        #     data_section += ["{}-1.{}, {}".format(f.part.name, f.key, self._field_value)]
        # return "\n".join(data_section)

