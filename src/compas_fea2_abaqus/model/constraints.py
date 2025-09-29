from compas_fea2.model.constraints import TieMPC
from compas_fea2.model.constraints import BeamMPC
from compas_fea2.model.constraints import TieConstraint

from compas_fea2.units import no_units


@no_units
def jobdata(obj):
    return "\n".join(
        ["** Constraint: {} Type: {}".format(obj.name, obj.constraint_type), "*MPC", "{}, ".format(obj.constraint_type)]
    )


class AbaqusTieMPC(TieMPC):
    """Abaqus implementation of the :class:`TieMPC`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += TieMPC.__doc__ or ""

    def __init__(self, name=None, **kwargs) -> None:
        super(AbaqusTieMPC, self).__init__(name=name, constraint_type="TIE", **kwargs)

    @property
    @no_units
    def jobdata(self):
        return jobdata(self)


class AbaqusBeamMPC(BeamMPC):
    """Abaqus implementation of the :class:`BeamMPC`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += BeamMPC.__doc__ or ""

    def __init__(self, name=None, **kwargs) -> None:
        super(AbaqusBeamMPC, self).__init__(name=name, constraint_type="BEAM", **kwargs)

    @property
    @no_units
    def jobdata(self):
        return jobdata(self)


class AbaqusTieConstraint(TieConstraint):
    """Abaqus implementation of the :class:`TieConstraint`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += TieConstraint.__doc__ or ""

    def __init__(self, name=None, **kwargs) -> None:
        super(AbaqusTieConstraint, self).__init__(name=name, **kwargs)
        self.adjust = "YES"

    @property
    @no_units
    def jobdata(self):
        return "\n".join(
            ["** Constraint: {} Type: Tie".format(self.name), "*Tie, name={}\n".format(self.name, self.adjust)]
        )
