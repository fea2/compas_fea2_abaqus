
from compas_fea2.model.fields import BoundaryConditionsField
from compas_fea2.units import no_units

dofs = ["x", "y", "z", "xx", "yy", "zz"]

class AbaqusBoundaryConditionsField(BoundaryConditionsField):
    """Calculix implementation of :class:`BoundaryConditionsField`.

    Notes
    -----
    This is equivalent to a boundary conditions field in Calculix.

    """

    __doc__ = (__doc__ or "") + (BoundaryConditionsField.__doc__ or "")

    def __init__(self, distribution, condition, follow=False, modify=False, **kwargs):
        super().__init__(distribution=distribution, condition=condition, **kwargs)
        self._modify = ", OP={}".format(modify) if modify else ", OP=MOD"  # In abaqus the default is MOD
        self._follow = ", follower" if follow else ""  
        
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

        data_section = [
            "** Name: {} Type: Boundary Condition".format(self.name),
            "*Boundary{}{}".format(self._modify, self._follow),
        ]

        for node, bc in self.node_bc:
            for comp, dof in enumerate(dofs, 1):
                if getattr(bc, dof):
                    data_section.append(f"{node.part.name}-1.{node.key}, {comp}")
        return "\n".join(data_section) or "**"