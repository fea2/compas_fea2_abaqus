from compas_fea2.model.interactions import ThermalInteraction
from compas_fea2.problem.steps import HeatTransferStep


class AbaqusHeatTransferStep(HeatTransferStep):
    """"""

    __doc__ += HeatTransferStep.__doc__
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
        self._stype = "Heat Transfer"
        self._restart = restart

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
{self._generate_header_section()}
** - Boundary Conditions
**   -------------
{self._generate_imposedTemperature_section()}
**
** - Loads
**   -----
{self._generate_loads_section()}
** - Surface Interactions
**   -----
{self._generate_thermalinterfaces_section()}
**
** - Predefined Fields
**   -----------------
**
{self._generate_predifined_fields()}
** - Output Requests
**   ---------------
{self._generate_output_section()}
**
*End Step
**
**
"""

    def _generate_header_section(self):
        data = [
            f"** STEP: {self._name}",
            f"*Step, name={self._name}, nlgeom={'YES' if self._nlgeom else 'NO'}, inc={self._max_increments}",
            f"*{self._stype}, end=PERIOD, deltmx={self.max_temp_delta}, mxdem={self.max_emiss_change}",
            f"{self._initial_inc_size}, {self._time}, {self._min_inc_size}, {self._max_inc_size}",
        ]
        return "\n".join(data)
    
    def _generate_imposedTemperature_section(self):
        """Generate the content relatitive to the boundary conditions section
        for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        from compas_fea2.model.bcs import ImposedTemperature
        return "\n".join([bc.jobdata(nodes) if isinstance(bc, ImposedTemperature) else "**" for bc, nodes in self.model.bcs_nodes.items()]) or "**"

    def _generate_loads_section(self):
        data = []
        for load_field in self.load_fields:
            data.append(load_field.jobdata())
        return "\n".join(data) or "**"

    def _generate_thermalinterfaces_section(self):
        """ """
        data = ["**"]
        for interface in self.model.interfaces:
            if isinstance(interface.behavior, ThermalInteraction):
                data.append(interface.behavior.jobdata(interface.master))
        return "\n".join(data)

    def _generate_predifined_fields(self):
        return "**"

    def _generate_output_section(self):
        from itertools import groupby

        if self._field_outputs:
            data = ["**", "*Restart, write, frequency={}".format(0), "**"]
            data.append("*Output, field")
            grouped_outputs = {k: list(g) for k, g in groupby(self._field_outputs, key=lambda x: x.output_type)}
            if element_outputs := grouped_outputs.get("element", None):
                data.append("*Element Output, direction=YES")
                data.append(", ".join([output.jobdata() for output in element_outputs]))
            if node_outputs := grouped_outputs.get("node", None):
                data.append("*Node Output")
                data.append(", ".join([output.jobdata() for output in node_outputs]))
            if contact_outputs := grouped_outputs.get("contact", None):
                data.append("*Contact Output")
                data.append(", ".join([output.jobdata() for output in contact_outputs]))
            return "\n".join(data)
        else:
            return "*Output, field, variable=ALL\n**"

    def _generate_history_section(self):
        if self._history_outputs:
            data = []
            for output in self._history_outputs:
                data.append(f"** HISTORY OUTPUT: {output.name}")
                data.append("**")
                data.append("*Output, history, variable=ALL")
                data.append("**")
