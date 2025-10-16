from compas_fea2.model import Steel

from compas_fea2.units import no_units

# ==============================================================================
# non-linear metal
# ==============================================================================


class AbaqusSteel(Steel):
    """Abaqus implementation of :class:`Steel`\n"""

    __doc__ = __doc__ or ""
    __doc__ += Steel.__doc__ or ""

    def __init__(self, *, fy, fu, eu, E, v, density, name=None, **kwargs):
        super(AbaqusSteel, self).__init__(fy=fy, fu=fu, eu=eu, E=E, v=v, density=density, name=name, **kwargs)

    @property
    @no_units
    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data_section = []
        line = ("*Material, name={}\n" "*Density\n" "{},\n" "*Elastic\n" "{}, {}").format(
            self.name, self.density, self.E, self.v
        )
        data_section.append(line)

        # for i, j in zip(self.compression["f"], self.compression["e"]):
        #     line = """{}, {}""".format(abs(i), abs(j))
        #     data_section.append(line)
        return "\n".join(data_section)
