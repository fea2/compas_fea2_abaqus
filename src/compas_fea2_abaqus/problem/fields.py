from compas_fea2.problem import PrescribedTemperatureField
from compas_fea2.problem import HeatFluxField
from compas_fea2.problem import ConvectionField
from compas_fea2.problem import RadiationField
from compas_fea2.problem import TemperatureLoad


class AbaqusConvectionField(ConvectionField):
    def __init__(self, temperature, h, surface, **kwargs):
        super().__init__(temperature=temperature, h=h, surface=surface, **kwargs)
    
    def jobdata(self):
#         if isinstance(self.temperature[-1], TransientTemperatureLoad):
#             return f"""**Convection Interaction, name={self.name}
# *Sfilm, amplitude={self.temperature[-1].name}
# {self.surface._name}_i, F, 1., {self.h}
# **"""
            return "**"

#         if isinstance(self.temperature[-1], TemperatureLoad):
#             return f"""**Convection Interaction, name={self.name}
# *Sfilm
# {self.surface._name}_i, F, {self.temperature[-1].temperature}, {self.h}
# **"""

class AbaqusRadiationField(RadiationField):
    def __init__(self, temperature, eps, surface, **kwargs):
        super().__init__(temperature=temperature, eps=eps, surface=surface, **kwargs)

    def jobdata(self):
#         if isinstance(self.temperature[-1], TransientTemperatureLoad):
#             return f"""**Radiation Interaction, name={self.name}
# *Sradiate, amplitude={self.temperature[-1].name}
# {self.surface.name}_i, R, 1., {self.eps}"""


        if isinstance(self.temperature[-1], TemperatureLoad):
            return f"""**Radiation Interaction, name={self.name}
*Sradiate
{self.surface.name}_i, R, {self.temperature[-1].temperature}, {self.eps}"""

class AbaqusHeatFluxField(HeatFluxField):

    """Abaqus implementation of :class:`HeatFluxLoad`.\n"""
    __doc__ += HeatFluxField.__doc__

    def __init__(self, heatflux, surface, **kwargs):
        super().__init__(heatflux=heatflux, surface=surface, **kwargs)

    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        data_field=[]
        data_field.append(f"** Name: {self.name} Type: Surface heat flux")
        data_field.append("*Dsflux")
        if self.heatflux[0].amplitude :
            data_field[-1] += f", amplitude={self.heatflux[0].amplitude.name}"
        data_field.append(f"{self.surface._name}_i, S, {self.heatflux[0].q}")
        return '\n'.join(data_field)
    
class AbaqusPrescribedTemperatureField(PrescribedTemperatureField):
    """Abaqus implementation of :class:`PrescribedTemperatureField`.\n"""
    __doc__ += PrescribedTemperatureField.__doc__

    def __init__(self, temperature=None, step=None, inc=None, name=None, **kwargs):
        super(AbaqusPrescribedTemperatureField, self).__init__(temperature=temperature, name=name, **kwargs)
        self._ictype = "TEMPERATURE"
        if step:
            self._step=step
        if inc:
            self._inc=inc

    def jobdata(self, nodes):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        if getattr(self, '_path', None): #implementation of temperaturefield via an abaqus file output (.odb)
            if not(self._step) or not(self._inc):
                raise ValueError("The step and the increment of the field imported from an Abaqus file output must be indicated.")
            # data_field = [f"""** Name: {self.name} Type: Temperature Field\n*Initial Conditions, type={self._ictype}, file="{self._path}", step={self._step}, inc={self._inc}, interpolate"""]
            return f"""** Name: {self.name} Type: Temperature Field\n*{self._ictype}, file="{self._path}", bstep={self._step}, binc={self._inc}, estep={self._step}, einc={self._inc}, interpolate"""
        
        data_field = [f"""** Name: {self.name} Type: Temperature Field"""]
        
        data_field.append("*{self._ictype}")
        for node in nodes:
            data_field.append(f"{node.part.name}-1.{node.key}, {self.temperature}")
        return "\n".join(data_field)
        # data_field = ['** Name: {} Type: Temperature Field'.format(self.name),
        #                 '*Temperature']
        # for node in nodes:
        #     data_field += ['{}-1.{}, {}'.format(node.part.name, node.key, self._t)]
        # return '\n'.join(data_field)
