from compas_fea2.problem.steps import StaticStep
from compas_fea2.problem.steps import StaticRiksStep
from compas_fea2.problem.fields import GravityLoadField
from compas_fea2.results.fields import NodeFieldResults, ElementFieldResults

from compas_fea2.units import no_units


class AbaqusStaticStep(StaticStep):
    """"""

    __doc__ = __doc__ or ""
    __doc__ += StaticStep.__doc__ or ""
    """
    Warning
    -------
    In general steps the loads must be specified as total values, not incremental
    values. For example, if a concentrated load has a value of 1000 N in the
    first step and it is increased to 3000 N in the second general step, the
    magnitude given on the *CLOAD option in the two steps should be 1000 N and
    3000 N, not 1000 N and 2000 N.

    Note
    ----
    the data for the input file for this object is generated at runtime.

    """

    def __init__(
        self,
        max_increments=1000,
        initial_inc_size=1,
        min_inc_size=0.00001,
        max_inc_size=1,
        time=1,
        nlgeom=False,
        modify=True,
        restart=False,
        name=None,
        **kwargs,
    ):
        super().__init__(
            max_increments=max_increments,
            initial_inc_size=initial_inc_size,
            min_inc_size=min_inc_size,
            max_inc_size=max_inc_size,
            time=time,
            nlgeom=nlgeom,
            modify=modify,
            name=name,
            **kwargs,
        )
        self._stype = "Static"
        self._restart = restart

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
        return f"""**
** STEP: {self._name}
*Step, name={self.name}, nlgeom={'YES' if self._nlgeom else 'NO'}, inc={self._max_increments}
*{self._stype}
{self._initial_inc_size}, {self._time}, {self._min_inc_size}, {self._time}
**
** - Imposed Displacements
**   ---------------------
{'\n'.join([force_field.jobdata for force_field in self.displacements] if self.displacements else ['**'])}
**
** - Loads
**   -----
{'\n'.join([force_field.jobdata for force_field in self.fields] if self.fields else ['**'])}
**
** - Predefined Fields
**   -----------------
**
{self._generate_prescribed_field_section()}
** - Output Requests
**   ---------------
{self._generate_output_section()}
**
*End Step
"""

    # @no_units
    # def _generate_header_section(self):
    #     data = [
    #         f"** STEP: {self._name}",
    #         f"*Step, name={self._name}, nlgeom={'YES' if self._nlgeom else 'NO'}, inc={self._max_increments}",
    #         f"*{self._stype}",
    #         f"{self._initial_inc_size}, {self._time}, {self._min_inc_size}, {self._time}",
    #     ]
    #     return "\n".join(data)

    # @no_units
    # def _generate_displacements_section(self):
    #     return (
    #         "\n".join(
    #             [
    #                 displacement.jobdata(node)
    #                 for field in self.displacements
    #                 for node, displacement in field.node_displacement
    #             ]
    #         )
    #         or "**"
    #     )

    # @no_units
    # def _generate_loads_section(self):
    #     data = []
    #     for node, load in self.combination.node_load:
    #         data.append(load.jobdata(node))
    #     return "\n".join(data) or "**"

    @no_units
    def _generate_output_section(self):
        from itertools import groupby

        if self._field_outputs:
            data = [
                "**",
                "*Restart, write, frequency={}".format(self.restart or 0),
                "**",
            ]
            data.append("*Output, field")
            grouped_outputs = {
                k: list(g)
                for k, g in groupby(self._field_outputs, key=lambda x: x.output_type)
            }
            if element_outputs := grouped_outputs.get("element", None):
                data.append("*Element Output, direction=YES")
                data.append(", ".join([output.jobdata for output in element_outputs]))
            if node_outputs := grouped_outputs.get("node", None):
                data.append("*Node Output")
                data.append(", ".join([output.jobdata for output in node_outputs]))
            if contact_outputs := grouped_outputs.get("contact", None):
                data.append("*Contact Output")
                data.append(", ".join([output.jobdata for output in contact_outputs]))
            return "\n".join(data)
        else:
            return "*Output, field, variable=ALL\n**"

    # @no_units
    # def _generate_history_section(self):
    #     if self._history_outputs:
    #         data = []
    #         for output in self._history_outputs:
    #             data.append(f"** HISTORY OUTPUT: {output.name}")
    #             data.append("**")
    #             data.append("*Output, history, variable=ALL")
    #             data.append("**")

    # @no_units
    # def _generate_perturbations_section(self):
    #     if self._perturbations:
    #         return "\n".join(
    #             [perturbation.jobdata() for perturbation in self.perturbations]
    #         )
    #     else:
    #         return "**"

    def _generate_prescribed_field_section(self):
        """

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        return "**"
        return "\n".join([ic.jobdata(nodes) for ic, nodes in self.prescribed_fields.items()]) or "**"
        # return "\n".join([ic.jobdata() if isinstance(ic, InitialTemperatureField) else "" for ic, nodes in self.model.ics.items()]) or "**"

    def _generate_prescribed_field_section(self):
        """

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        return "**"
        return "\n".join([ic.jobdata(nodes) for ic, nodes in self.prescribed_fields.items()]) or "**"
        # return "\n".join([ic.jobdata() if isinstance(ic, InitialTemperatureField) else "" for ic, nodes in self.model.ics.items()]) or "**"


class AbaqusStaticRiksStep(StaticRiksStep):
    """Abaqus implementation of :class:`StaticRiksStep`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += StaticRiksStep.__doc__ or ""

    def __init__(
        self,
        max_increments=100,
        initial_inc_size=1,
        min_inc_size=0.00001,
        time=1,
        nlgeom=False,
        modify=True,
        name=None,
        **kwargs,
    ):
        super().__init__(
            max_increments,
            initial_inc_size,
            min_inc_size,
            time,
            nlgeom,
            modify,
            name,
            **kwargs,
        )
        raise NotImplementedError
