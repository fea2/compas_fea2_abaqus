
from compas_fea2.model.fields import BoundaryConditionsField
from compas_fea2.units import no_units

class AbaqusBoundaryConditionsField(BoundaryConditionsField):
    """Calculix implementation of :class:`BoundaryConditionsField`.

    Notes
    -----
    This is equivalent to a boundary conditions field in Calculix.

    """

    __doc__ = (__doc__ or "") + (BoundaryConditionsField.__doc__ or "")

    def __init__(self, distribution, condition, **kwargs):
        super().__init__(distribution=distribution, condition=condition, **kwargs)

    @property
    @no_units
    def jobdata(self):
        """Generates the string information for the input file."""
        dofs = ["x", "y", "z", "xx", "yy", "zz"]
        data = []
        data.append(self.distribution.jobdata())
        data.append(f"** Name: {self.name} Type: BC/Rotation \n*Boundary, op=NEW")
        data.extend([f'{self.distribution.name}, {comp}' for comp, dof in enumerate(dofs, 1) if getattr(self.condition, dof)])
        return '\n'.join(data) if data else "**"