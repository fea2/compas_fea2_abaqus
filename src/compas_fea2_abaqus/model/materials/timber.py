from compas_fea2.model.materials.timber import Timber

from compas_fea2.units import no_units


class AbaqusTimber(Timber):
    """"""

    __doc__ = __doc__ or ""
    __doc__ += Timber.__doc__ or ""

    def __init__(self, *, name=None, **kwargs):
        super(AbaqusTimber, self).__init__(name=name, **kwargs)
        raise NotImplementedError("The current material is not available in Abaqus")

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
        raise NotImplementedError
