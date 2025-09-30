from compas_fea2.model.interactions import HardContactFrictionPenalty
from compas_fea2.model.interactions import LinearContactFrictionPenalty
from compas_fea2.model.interactions import HardContactRough
from compas_fea2.model.interactions import Convection
from compas_fea2.model.interactions import Radiation

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


class AbaqusConvection(Convection):
    """Abaqus implementation of the :class:`HardContactNoFriction`.\n"""

    __doc__ += Convection.__doc__

    def __init__(self, h, temperature_value, temperature_amplitude, **kwargs) -> None:
        super().__init__(h=h, temperature_value=temperature_value, temperature_amplitude=temperature_amplitude, **kwargs)

    def jobdata(self, master):
        data_interface = []
        data_interface.append(f"** Name: {self.name} Type: Convection interaction")
        data_interface.append("*Sfilm")
        if self.temperature.amplitude:
            data_interface[-1] += f", amplitude={self.temperature.amplitude.name}"
        data_interface.append(f"{master._name}_i, F, {self.temperature.scalar_load}, {self.h}")
        return "\n".join(data_interface)

class AbaqusRadiation(Radiation):
    """Abaqus implementation of the :class:`HardContactNoFriction`.\n"""

    __doc__ += Convection.__doc__

    def __init__(self, eps, temperature_value, temperature_amplitude, **kwargs) -> None:
        super().__init__(eps=eps, temperature_value=temperature_value, temperature_amplitude=temperature_amplitude, **kwargs)

    def jobdata(self, master):
        data_interface = []
        data_interface.append(f"** Name: {self.name} Type: Radiation interaction")
        data_interface.append("*Sradiate")
        if self.temperature.amplitude:
            data_interface[-1] += f", amplitude={self.temperature.amplitude.name}"
        data_interface.append(f"{master._name}_i, R, {self.temperature.scalar_load}, {self.eps}")
        return "\n".join(data_interface)
