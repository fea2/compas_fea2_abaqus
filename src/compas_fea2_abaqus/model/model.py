from compas_fea2.model import Model, RigidPart
from compas_fea2.model import ElementsGroup, NodesGroup
from compas_fea2.model import _Constraint, _Interaction
from compas_fea2.model.interactions import ThermalInteraction
from compas_fea2.model.interfaces import PartPartInterface, BoundaryInterface
from compas_fea2.model.bcs import MechanicalBC

from compas_fea2.units import no_units


class AbaqusModel(Model):
    """Abaqus implementation of :class:`Model`.

    Note
    ----
    For many aspects, this is equivalent to an `Assembly` in Abaqus.

    """

    __doc__ = __doc__ or ""
    __doc__ += Model.__doc__ or ""

    def __init__(self, name=None, description=None, author=None, **kwargs):
        super(AbaqusModel, self).__init__(
            name=name, description=description, author=author, **kwargs
        )
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

    @property
    @no_units
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
{self.materials.jobdata or "**"}
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

    @no_units
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
                part.add_group(
                    ElementsGroup(
                        members=list(part.elements), name=f"all_elements_{part.name}"
                    )
                )
                part.add_group(
                    NodesGroup(
                        members=[part.reference_point], name=f"ref_point_{part.name}"
                    )
                )
            data_section.append(part.jobdata)
        return "\n".join(data_section)

    @no_units
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

        # Header
        data_section = ["*Assembly, name={}".format(self.name)]

        # Nodes and elements
        data_section.append(
            f"*NSET,NSET=Nall,GENERATE\n{self._starting_key},{len(self.nodes)}"
        )
        data_section.append(
            f"*ELSET,ELSET=Eall,GENERATE\n{self._starting_key},{len(self.elements)}"
        )
        "\n".join(data_section)

        # Groups/sets defined at the part level
        for part in self._parts:
            data_section.append(part._generate_instance_jobdata)
            if isinstance(part, RigidPart):
                data_section.append(part._generate_instance_jobdata)
            for group in part.groups:
                data_section.append(group.jobdata(instance=True))

        # Connectors
        data_section.append("**\n** CONNECTORS\n**")
        for connector in self.connectors:
            data_section.append(connector.jobdata)
        data_section.append("**\n** INTERFACES\n**")
        interface_groups = set()
        for interface in self.interfaces:
            interface_groups.add(interface.master)
            if isinstance(interface, PartPartInterface):
                interface_groups.add(interface.slave)
        for interface_group in interface_groups:
            data_section.append(interface_group.jobdata)
        data_section.append("**\n** CONSTRAINTS\n**")
        for interface in filter(lambda i: isinstance(i.behavior, _Constraint), self.interfaces):
            data_section.append(interface.jobdata)
        # for group in self.partgroups:
        #     data_section.append(group.jobdata(instance=True))
        data_section.append("*End Assembly")

        return "\n".join(data_section)

    @no_units
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
                if step.amplitudes :
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
            data_section.append(material.jobdata)
        return "\n".join(data_section)

    @no_units
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
            #Thermal Interactions must be implemented in the step part
            data.append(interaction.jobdata if not(isinstance(interaction, ThermalInteraction)) else "**")
        connector_sections = set([connector.section for connector in self.connectors])
        for connector_section in connector_sections:
            data.append(connector_section.jobdata())
        return "\n".join(data)

    @no_units
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
        interfaces = list(filter(lambda i: (isinstance(i, PartPartInterface) and not(isinstance(i.behavior, _Constraint))), self.interfaces ))
        return "\n".join(interface.jobdata for interface in interfaces) if interfaces else "**"

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
        return "\n".join([bc_filed.jobdata for bc_filed in self.bcs]) or "**"

    @no_units
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
        return "\n".join([ic.jobdata() for ic in self.ics]) or "**"

    @no_units
    def _generate_groups_section(self):
        """Generate the content relatitive to the groups section for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        data_section = []
        for group in self.groups:
            if isinstance(group, (NodesGroup, ElementsGroup)):
                data_section.append(group.jobdata)
        return "\n".join(data_section) or "**"
