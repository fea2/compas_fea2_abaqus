from compas_fea2.model.fields import BoundaryConditionsField, BeamReleaseField
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


class AbaqusBeamReleaseField(BeamReleaseField):
    """Abaqus implementation of BeamReleaseField."""

    __doc__ += BeamReleaseField.__doc__

    def __init__(self, release, elements, end, name=None, **kwargs):
        super().__init__(release, elements, end, name, **kwargs)

        if end == "start":
            self.abaqus_end = ["S1"]
        elif end == "end":
            self.abaqus_end = ["S2"]
        elif end == "both":
            self.abaqus_end = ["S1", "S2"]
        else:
            raise ValueError("The end of the release is not implemented.")

    @property
    def jobdata(self):
        data = ["*Release"]
        for element in self.elements:
            for end in self.abaqus_end:
                for release_component in self.release.release_components:
                    if getattr(self.release, release_component, None):
                        data += [", ".join([str(element.key), end, release_component])]
        return "\n".join(data)
