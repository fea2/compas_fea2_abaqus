from compas_fea2.model.constraints import TieMPC
from compas_fea2.model.constraints import BeamMPC
from compas_fea2.model.constraints import TieConstraint


def jobdata(obj):
    return "\n".join(
        [
            "** Constraint: {} Type: {}".format(obj.name, obj.constraint_type),
            "*MPC",
            "{}".format(obj.constraint_type),
        ]
    )


class AbaqusTieMPC(TieMPC):
    """Abaqus implementation of the :class:`TieMPC`.\n"""

    __doc__ += TieMPC.__doc__

    def __init__(self, name=None, **kwargs) -> None:
        super(AbaqusTieMPC, self).__init__(name=name, constraint_type="TIE", **kwargs)

    def jobdata(self):
        return jobdata(self)


class AbaqusBeamMPC(BeamMPC):
    """Abaqus implementation of the :class:`BeamMPC`.\n"""

    __doc__ += BeamMPC.__doc__

    def __init__(self, name=None, **kwargs) -> None:
        super(AbaqusBeamMPC, self).__init__(name=name, constraint_type="BEAM", **kwargs)

    def jobdata(self):
        return jobdata(self)


class AbaqusTieConstraint(TieConstraint):
    """Abaqus implementation of the :class:`TieConstraint`.\n"""

    __doc__ += TieConstraint.__doc__

    def __init__(self,name=None, adjust='no', position_tolerance=0.001, **kwargs) -> None:
        super(AbaqusTieConstraint, self).__init__(name=name, **kwargs)
        self.adjust = adjust
        self.position_tolerance = position_tolerance

    def jobdata(self, master, slave):
        return "\n".join(
            [
                "** Constraint: {} Type: Tie".format(self.name),
                f"*Tie, name={self.name}, adjust={self.adjust}, position tolerance={self.position_tolerance}",
                f"{master.name}, {slave.name}"

            ]
        )
