from compas_fea2.problem import PrescribedTemperatureField


class AbaqusPrescribedTemperatureField(PrescribedTemperatureField):
    """Abaqus implementation of :class:`PrescribedTemperatureField`.\n"""
    __doc__ += PrescribedTemperatureField.__doc__

    def __init__(self, temperature, name=None, **kwargs):
        super(AbaqusPrescribedTemperatureField, self).__init__(temperature, name, **kwargs)

    def jobdata(self, nodes):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """

        data_section = ['** Name: {} Type: Temperature Field'.format(self.name),
                        '*Temperature']
        for node in nodes:
            data_section += ['{}-1.{}, {}'.format(node.part.name, node.key, self._t)]
        return '\n'.join(data_section)
