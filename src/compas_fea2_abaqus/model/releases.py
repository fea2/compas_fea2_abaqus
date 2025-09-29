from compas_fea2.model.releases import BeamEndPinRelease

from compas_fea2.units import no_units


class AbaqusBeamEndPinRelease(BeamEndPinRelease):
    """Abaqus implementation of the :class:`BeamEndPinRelease`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += BeamEndPinRelease.__doc__ or ""

    def __init__(self, m1=False, m2=False, t=False, name=None, **kwargs):
        super(AbaqusBeamEndPinRelease, self).__init__(m1=m1, m2=m2, t=t, name=name, **kwargs)

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
        ends = {"start": "S1", "end": "S2"}
        dofs = {"m1": "M1", "m2": "M2", "t": "T"}
        return "{},{},{}\n".format(
            self.element.key, ends[self.location], ", ".join(dofs[dof] for dof in dofs if getattr(self, dof))
        )
