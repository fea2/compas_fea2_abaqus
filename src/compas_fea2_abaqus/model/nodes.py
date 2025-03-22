from compas_fea2.model import Node


# =============================================================================
# General
# =============================================================================


class AbaqusNode(Node):
    """Abaqus implementation of :class:`compas_fea2.model.Node`."""

    __doc__ += Node.__doc__

    def __init__(self, xyz, mass=None, name=None, **kwargs):
        super(AbaqusNode, self).__init__(xyz=xyz, mass=mass, name=name, **kwargs)

    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        x, y, z = self.xyz
        return "{:>10}, {:>10.3f}, {:>10.3f}, {:>10.3f}".format(self.key, x, y, z)
