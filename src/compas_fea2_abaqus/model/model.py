from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import groupby

from compas_fea2.model import Model, RigidPart
from compas_fea2.model import ElementsGroup, NodesGroup
from compas_fea2.model import _Constraint, _Interaction
from compas_fea2.model import InitialStressField, InitialTemperatureField
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

    @timer(message='Model generated in ')
    def jobdata(self):
        return """**
** PARTS
**
{}
**
** ASSEMBLY
**
{}
**
**
** MATERIALS
**
{}
**
** INTERACTIONS
**
{}
**
** INTERFACES
**
{}
**
** INITIAL and BOUNDARY CONDITIONS
**
{}
**
{}
""".format(self._generate_part_section(),
           self._generate_assembly_section(),
           self._generate_material_section(),
           self._generate_interactions_section(),
           self._generate_interfaces_section(),
           self._generate_bcs_section(),
           self._generate_ics_section()
           )


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
                part.add_group(ElementsGroup(elements=list(part.elements), name='all_elements'))
                part.add_group(NodesGroup(nodes=[part.reference_point], name='ref_point'))
            data = part.jobdata()
            data_section.append(data)
        return '\n'.join(data_section)

    def _generate_assembly_section(self):
        """Generate the content relatitive the assembly for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        data_section = ['*Assembly, name={}'.format(self.name)]
        for part in self._parts:
            data_section.append(part._generate_instance_jobdata())
            if isinstance(part, RigidPart):
                data_section.append(part._generate_rigid_body_jobdata())
            for group in part.nodesgroups:
                data_section.append(group.jobdata(instance=True))
            for group in part.elementsgroups:
                data_section.append(group.jobdata(instance=True))
            for group in part.facesgroups:
                data_section.append(group.jobdata())
        data_section.append("**\n** CONNECTORS\n**")
        for connector in self.connectors:
            data_section.append("\n".join([connector.section.jobdata(connector.name), connector.jobdata()]))
        for interface in filter(lambda i: isinstance(i.behavior, _Constraint), self.interfaces):
            data_section.append(interface._generate_jobdata())
        data_section.append('*End Assembly')

        return '\n'.join(data_section)

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
        return '\n'.join(data_section)


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
        return '\n'.join(interaction._generate_jobdata() for interaction in self.interactions) if self.interactions else '**'

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
        interfaces = list(filter(lambda i: isinstance(i.behavior, _Interaction), self.interfaces))
        return '\n'.join(interface._generate_jobdata() for interface in interfaces) if interfaces else '**'


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
        data_section = []
        for bc, nodes in self.bcs.items():
            for part, part_nodes in groupby(nodes, lambda n: n.part):
                data_section.append(bc.jobdata(part_nodes))
        return '\n'.join(data_section) or '**'

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
        return '\n'.join([ic.jobdata() for ic in self.ics]) or '**'
