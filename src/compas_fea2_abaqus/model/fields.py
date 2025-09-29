import typing
from compas_fea2.model.fields import BeamReleaseField
from compas_fea2.model.elements import _Element1D

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