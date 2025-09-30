import typing
from compas_fea2.model.fields import BeamReleaseField
from compas_fea2.model.elements import _Element1D
from compas_fea2.model.fields import BoundaryConditionsField
from compas_fea2.units import no_units

class AbaqusBeamReleaseField(BeamReleaseField):
    """Abaqus implementation of BeamReleaseField."""
    __doc__ += BeamReleaseField.__doc__

    def __init__(self, release, elements, end, name=None, **kwargs):
        super().__init__(release, elements, end, name, **kwargs)

        if end =='start':
            self.abaqus_end=['S1']
        elif end=='end':
            self.abaqus_end=['S2']
        elif end=='both':
            self.abaqus_end=['S1', 'S2']
        else :
            raise ValueError('The end of the release is not implemented.')

    @property
    def jobdata(self):
        data=["*Release"]
        for element in self.elements:
            for end in self.abaqus_end:
                for release_direction in self.release.release_directions:
                    if getattr(self.release, release_direction, None):
                        data+=[', '.join([str(element.key), end, release_direction])]
        return '\n'.join(data)


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
