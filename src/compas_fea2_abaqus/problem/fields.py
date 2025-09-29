from compas_fea2.problem.fields import GravityLoadField
# from compas_fea2.problem.fields import PrescribedTemperatureField

class AbaqusGravityLoadField(GravityLoadField):
    """Abaqus implementation of :class:`GravityLoadField`.\n"""
    __doc__=GravityLoadField.__doc__
    __doc__+= """
Nota
----
In Abaqus, gevity can only be applied to the entire model.
"""
    def __init__(self, g=9.81, load_case='DL', **kwargs):
        super().__init__(g=g, load_case=load_case, **kwargs)

    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return ("** Name: {} Type: Gravity\n*Dload\n, GRAV, {}, {}, {}, {}").format(
            self.name, self.g, 0, 0, -1
        )


# class AbaqusPrescribedTemperatureField(PrescribedTemperatureField):
#     """Abaqus implementation of :class:`PrescribedTemperatureField`.\n"""

#     __doc__ += PrescribedTemperatureField.__doc__

#     def __init__(self, temperature=None, step=None, inc=None, name=None, **kwargs):
#         super(AbaqusPrescribedTemperatureField, self).__init__(temperature=temperature, name=name, **kwargs)
#         self._ictype = "TEMPERATURE"
#         if step:
#             self._step = step
#         if inc:
#             self._inc = inc

#     @classmethod
#     def from_file(cls, path):
#         return "**"

#     def jobdata(self, nodes):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).

#         """
#         if getattr(self, "_path", None):  # implementation of temperaturefield via an abaqus file output (.odb)
#             if not (self._step) or not (self._inc):
#                 raise ValueError(
#                     "The step and the increment of the field imported from an Abaqus file output must be indicated."
#                 )
#             # data_field = [f"""** Name: {self.name} Type: Temperature Field\n*Initial Conditions, type={self._ictype}, file="{self._path}", step={self._step}, inc={self._inc}, interpolate"""]
#             return f"""** Name: {self.name} Type: Temperature Field\n*{self._ictype}, file="{self._path}", bstep={self._step}, binc={self._inc}, estep={self._step}, einc={self._inc}, interpolate"""

#         data_field = [f"""** Name: {self.name} Type: Temperature Field"""]

#         data_field.append("*{self._ictype}")
#         for node in nodes:
#             data_field.append(f"{node.part.name}-1.{node.key}, {self.temperature}")
#         return "\n".join(data_field)
#         # data_field = ['** Name: {} Type: Temperature Field'.format(self.name),
#         #                 '*Temperature']
#         # for node in nodes:
#         #     data_field += ['{}-1.{}, {}'.format(node.part.name, node.key, self._t)]
#         # return '\n'.join(data_field)
