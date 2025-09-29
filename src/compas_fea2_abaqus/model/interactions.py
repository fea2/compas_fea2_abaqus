from compas_fea2.model.interactions import HardContactFrictionPenalty
from compas_fea2.model.interactions import LinearContactFrictionPenalty
from compas_fea2.model.interactions import HardContactRough
from compas_fea2.model.interactions import HardContactNoFriction

from compas_fea2.units import no_units


class AbaqusHardContactFrictionPenalty(HardContactFrictionPenalty):
    """Abaqus implementation of the :class:`HardContactFrictionPenalty`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += HardContactFrictionPenalty.__doc__ or ""

    def __init__(self, *, mu, tol=0.005, **kwargs) -> None:
        super(AbaqusHardContactFrictionPenalty, self).__init__(mu=mu, tol=tol, **kwargs)

    @property
    @no_units
    def jobdata(self):
        return """*Surface Interaction, name={}
*Friction, slip tol={}
{},
*Surface Behavior, pressure-overclosure={}
**""".format(
            self._name, self._tol, self._tangent, self._normal
        )


class AbaqusLinearContactFrictionPenalty(LinearContactFrictionPenalty):
    """Abaqus implementation of the :class:`LinearContactFrictionPenalty`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += LinearContactFrictionPenalty.__doc__ or ""

    def __init__(self, *, mu, tol=0.005, **kwargs) -> None:
        super(AbaqusLinearContactFrictionPenalty, self).__init__(mu=mu, tol=tol, **kwargs)

    @property
    @no_units
    def jobdata(self):
        return """*Surface Interaction, name={}
*Friction, slip tol={}
{},
*Surface Behavior, pressure-overclosure={}
{}
**""".format(
            self._name, self._tolerance, self._tangent, self._normal, self._stiffness
        )


class AbaqusHardContactRough(HardContactRough):
    """Abaqus implementation of the :class:`HardContactRough`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += HardContactRough.__doc__ or ""

    def __init__(self, **kwargs) -> None:
        super(AbaqusHardContactRough, self).__init__(**kwargs)

    @property
    @no_units
    def jobdata(self):
        return """*Surface Interaction, name={}
*Friction, rough
*Surface Behavior, pressure-overclosure={}
**""".format(
            self._name, self._normal
        )


class AbaqusHardContactNoFriction(HardContactNoFriction):
    """Abaqus implementation of the :class:`HardContactNoFriction`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += HardContactNoFriction.__doc__ or ""

    def __init__(self, **kwargs) -> None:
        super(AbaqusHardContactNoFriction, self).__init__(**kwargs)
        raise NotImplementedError()
