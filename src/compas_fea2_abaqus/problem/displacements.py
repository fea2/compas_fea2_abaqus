from typing import Iterable

from compas_fea2.problem import GeneralDisplacement

dofs = ["x", "y", "z", "xx", "yy", "zz"]


class AbaqusGeneralDisplacement(GeneralDisplacement):
    """Abaqus implementation of :class:`GeneralDisplacement`.\n"""

    __doc__ += GeneralDisplacement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    modify : bool, optional
        If ``True``, change previous displacements applied at the same location, otherwise
        add the displacement to the previous. By defult is ``True``.
    """

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes="global", **kwargs):
        super(AbaqusGeneralDisplacement, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, **kwargs)

    def jobdata(self, nodes):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data_section = [
            f"** Name: {self.name} Type:  Displacement/Rotation".format(),
            "*Boundary, OP=MOD",
        ]
        if not isinstance(nodes, Iterable):
            nodes = [nodes]
        for node in nodes:
            for comp, dof in enumerate(dofs, 1):
                if getattr(self, dof):
                    data_section += [f"{node.part.name}-1.{node.key}, {comp}, {comp}, {self.components[dof]}"]
        return "\n".join(data_section)
