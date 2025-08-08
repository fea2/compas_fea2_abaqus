from compas_fea2.model import Model, RigidPart
from compas_fea2.model import ElementsGroup, NodesGroup
from compas_fea2.model import _Constraint, _Interaction
from compas_fea2.utilities._utils import timer


class AbaqusModel(Model):
    """Abaqus implementation of :class:`Model`.

    Note
    ----
    For many aspects, this is equivalent to an `Assembly` in Abaqus.

    """

    __doc__ += Model.__doc__

    def __init__(self, name=None, description=None, author=None, **kwargs):
        super(AbaqusModel, self).__init__(name=name, description=description, author=author, **kwargs)
        self._starting_key = 1

    @classmethod
    def from_cae(cls, filepath):
        """Import a .cae abaqus file into a :class:`compas_fea2.model.Model` object.

        Note
        ----
        check this: http://130.149.89.49:2080/v2016/books/cmd/default.htm?startat=pt05ch09s05.html

        Parameters
        ----------
        filepath : _type_
            _description_

        Raises
        ------
        NotImplementedError
            _description_
        """
        raise NotImplementedError()

    # =============================================================================
    #                               Job data
    # =============================================================================

    @timer(message="Model generated in ")
    def jobdata(self):
        self.assign_keys(restart=True)
        return f"""**
** PARTS
**
{self._generate_part_section() or "**"}
**
** ASSEMBLY
**
{self._generate_assembly_section() or "**"}
**
**AMPLITUDES
**
{self._generate_amplitude_section() or "**"}
**
** MATERIALS
**
{self._generate_material_section() or "**"}
**
** INTERACTIONS
**
{self._generate_interactions_section() or "**"}
**
** INTERFACES
**
{self._generate_interfaces_section() or "**"}
**
** INITIAL and BOUNDARY CONDITIONS
**
{self._generate_bcs_section() or "**"}
**
{self._generate_ics_section() or "**"}
"""

    def _generate_part_section(self):
        """Generate the content relatitive the each DeformablePart for the input file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        data_section = []
        for part in self.parts:
            if isinstance(part, RigidPart):
                part.add_group(ElementsGroup(elements=list(part.elements), name="all_elements"))
                part.add_group(NodesGroup(nodes=[part.reference_point], name="ref_point"))
            data_section.append(part.jobdata())
        return "\n".join(data_section)

    def _generate_assembly_section(self):
        """Generate the content of the assembly for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """

        data_section = ["*Assembly, name={}".format(self.name)]
        for part in self._parts:
            data_section.append(part._generate_instance_jobdata())
            if isinstance(part, RigidPart):
                data_section.append(part._generate_rigid_body_jobdata())
            for group in part.groups:
                data_section.append(group.jobdata())
        data_section.append("**\n** CONNECTORS\n**")
        connector_gorups = []
        for connector in self.connectors:
            connector_gorups.append(ElementsGroup(elements=[connector], name=f"set-{connector.name}"))
            data_section.append(connector.jobdata())
        data_section.append("**\n** CONSTRAINTS\n**")
        for interface in filter(lambda i: isinstance(i.behavior, _Constraint), self.interfaces):
            data_section.append(interface._generate_jobdata())
        data_section.append("**\n** INTERFACES\n**")
        surface_set=set()
        for interface in self.interfaces:
            surface_set.add(interface.master)
            if interface.slave:
                surface_set.add(interface.slave)
        for surface in surface_set:
            data_section.append(surface.jobdata())
        # for group in self.partgroups:
        #     data_section.append(group.jobdata(instance=True))
        for group in connector_gorups:
            data_section.append(group.jobdata())
        data_section.append("*End Assembly")

        return "\n".join(data_section)

    def _generate_amplitude_section(self):
        data_section = []
        # model amplitudes
        for amplitude in self.amplitudes:
            data_section.append(f"*Amplitude, name={amplitude.name}")
            for multiplier, time in amplitude.multipliers_times:
                data_section.append(f"{time}, {multiplier},")
        # steps amplitudes
        for problem in self.problems:
            for step in problem.steps:
                for amplitude in step.amplitudes:
                    data_section.append(f"*Amplitude, name={amplitude.name}")
                    for multiplier, time in amplitude.multipliers_times:
                        data_section.append(f"{time}, {multiplier},")
        data_section.append("**")
        return "\n".join(data_section)

    def _generate_material_section(self):
        """Generate the content relatitive to the material section for the input
        file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        data_section = []
        for material in self.materials:
            data_section.append(material.jobdata())
        return "\n".join(data_section)

    def _generate_interactions_section(self):
        """Generate the content relatitive to the interactions section for the input
        file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        data = []
        for interaction in self.interactions:
            data.append(interaction.jobdata() if not(isinstance(interaction, ThermalInteraction)) else "**")
        connector_sections = set([connector.section for connector in self.connectors])
        for connector_section in connector_sections:
            data.append(connector_section.jobdata())
        return "\n".join(data)

    def _generate_interfaces_section(self):
        """Generate the content relatitive to the interfaces section for the input
        file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        interfaces = list(filter(lambda i: isinstance(i.behavior, _Interaction) and not(isinstance(i.behavior, ThermalInteraction)), self.interfaces))
        return "\n".join(interface._generate_jobdata() for interface in interfaces) if interfaces else "**"

    def _generate_bcs_section(self):
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
        data_section =[]
        for field in self.bcs_fields:
            for node, bc in field.node_bc:
                data_section.append(bc.jobdata([node]))
        return "\n".join(data_section) or "**"

    def _generate_ics_section(self):
        """Generate the content relatitive to the initial conditions section
        for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        data_section =[]
        for field in self.ics_fields:
            for node, ic in field.node_ic:
                data_section.append(ic.jobdata([node]))
        return "\n".join(data_section) or "**"