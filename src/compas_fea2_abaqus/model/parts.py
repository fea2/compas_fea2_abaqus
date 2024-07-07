from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import DeformablePart, RigidPart
from collections import defaultdict

def jobdata(obj):
    """Generate the string information for the input file.

    Parameters
    ----------
    None

    Returns
    -------
    str
        input file data lines.
    """
    return """**
*Part, name={}
**
** - Nodes
**   -----
{}
**
** - Elements
**   --------
{}
**
** - Sets
**   ----
{}
{}
**
** - Releases
**   --------
{}
**
*End Part""".format(obj.name,
                    _generate_nodes_section(obj),
                    _generate_elements_section(obj) or '**',
                    _generate_nodesets_section(obj) or '**',
                    _generate_elementsets_section(obj) or '**',
                    _generate_releases_section(obj) or '**')


def _generate_nodes_section(obj):
    return '\n'.join(['*Node']+[node.jobdata() for node in obj.nodes])


def _generate_elements_section(obj):
    part_data = []
    # Write elements, elsets and sections
    # this check is needed for rigid parts ->ugly, change!
    grouped_elements = obj._group_elements()
    for implementation, sections in grouped_elements.items():
        for section, orientations in sections.items():
            for orientation, elements in orientations.items():
                # Write elements
                elset_name = 'aux_{}_{}'.format(implementation, section.name) if not isinstance(obj, RigidPart) else 'all_elements'
                if orientation:
                    elset_name += '_{}'.format(orientation.replace(".", ""))
                    orientation = orientation.split('_')
                part_data.append("*Element, type={}, elset={}".format(implementation, elset_name))
                for element in elements:
                    part_data.append(element.jobdata())
                # if not isinstance(obj, RigidPart):
                part_data.append(section.jobdata(elset_name, orientation=orientation))
    return '\n'.join(part_data)


def _generate_nodesets_section(obj):
    if obj.nodesgroups:
        return '\n'.join([group.jobdata() for group in obj.nodesgroups])
    else:
        return '**'


def _generate_elementsets_section(obj):
    if obj.elementsgroups:
        return '\n'.join([group.jobdata() for group in obj.elementsgroups])
    else:
        return '**'


def _generate_releases_section(obj):
    if isinstance(obj, DeformablePart):
        if obj.releases:
            return '\n'.join(['*Release']+[release.jobdata() for release in obj.releases])
    else:
        return '**'


def _generate_instance_jobdata(obj):
    """Generates the string information for the input file.

    Note
    ----
    The creation of instances from the same part (which is a specific abaqus
    feature) is less useful in a scripting context (where it is easy to generate
    the parts already in their correct locations).

    Note
    ----
    The name of the instance is automatically generated using abaqus convention
    of adding a "-1" to the name of the part from which it is generated.

    Parameters
    ----------
    None

    Returns
    -------
    input file data line (str).
    """
    return '\n'.join(['*Instance, name={}-1, part={}'.format(obj.name, obj.name),
                      '*End Instance\n**'])

def _group_elements(obj):
    """Group the elements. This is used internally to generate the input
    file.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        {implementation:{section:{orientation: [elements]},},}
    """

    # Group elements by implementation
    grouped_elements = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

    for el in obj.elements:
        implementation = el._implementation
        section = el.section
        try:
            orientation = '_'.join(str(i) for i in el.frame.xaxis)
        except:
            orientation = None

        grouped_elements[implementation][section][orientation].add(el)

    return grouped_elements

class AbaqusDeformablePart(DeformablePart):
    """Abaqus implementation of :class:`DeformablePart`.
    """
    __doc__ += DeformablePart.__doc__

    def __init__(self, name=None, **kwargs):
        super(AbaqusDeformablePart, self).__init__(name=name, **kwargs)

    # =========================================================================
    #                       Generate input file data
    # =========================================================================
    def _group_elements(self):
        return _group_elements(self)

    def jobdata(self):
        return jobdata(self)

    def _generate_instance_jobdata(self):
        return _generate_instance_jobdata(self)


class AbaqusRigidPart(RigidPart):
    def __init__(self, name=None, **kwargs):
        super(AbaqusRigidPart, self).__init__(name=name, **kwargs)

    # def _generate_rigid_boundary(self):
    #     from compas_fea2.model import ShellElement

    #     mesh = self.discretized_boundary_mesh
    #     vertex_node = {vertex: self.find_closest_nodes_to_point(point=mesh.vertex_coordinates(vertex), distance=0.1, number_of_nodes=1)[0] for vertex in mesh.vertices()}
    #     rigid_faces = []
    #     for k, face in enumerate(mesh.faces()):
    #         nodes = [vertex_node[vertex] for vertex in mesh.face_vertices(face)]
    #         element = ShellElement(nodes=nodes, section=None, rigid=True)
    #         element._key = k
    #         element._registration = self
    #         rigid_faces.append(element)
    #     return rigid_faces

    # =========================================================================
    #                       Generate input file data
    # =========================================================================

    def _group_elements(self):
        return _group_elements(self)

    def jobdata(self):
        return jobdata(self)

    def _generate_rigid_body_jobdata(self):
        return "*Rigid Body, ref node={0}-1.ref_point, elset={0}-1.all_elements".format(self.name)

    def _generate_instance_jobdata(self):
        return _generate_instance_jobdata(self)
