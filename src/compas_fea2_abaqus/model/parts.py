from compas_fea2.model import Part, RigidPart
from collections import defaultdict

from compas_fea2.units import no_units


@no_units
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
    return f"""**
*Part, name={obj.name}
**
** - Nodes
**   -----
{_generate_nodes_section(obj) or '**'}
**
** - Elements
**   --------
{_generate_elements_section(obj) or '**'}
**
** - Sets
**   ----
{_generate_sets_section(obj) or '**'}
**
** - Releases
**   --------
**
*End Part"""


@no_units
def _generate_nodes_section(obj):
    return "\n".join(["*Node"] + [node.jobdata for node in obj.nodes.sorted])


@no_units
def _generate_elements_section(obj):
    part_data = []
    # Write elements, elsets and sections
    # this check is needed for rigid parts ->ugly, change!
    grouped_elements = obj._group_elements()
    for implementation, sections in grouped_elements.items():
        for section, orientations in sections.items():
            for orientation, elements in orientations.items():
                # Write elements
                elset_name = (
                    "aux_{}_{}".format(implementation, section.name)
                    if not isinstance(obj, RigidPart)
                    else "all_elements"
                )
                if orientation:
                    elset_name += "_{}".format(orientation.replace(".", ""))
                    orientation = orientation.split("_")
                part_data.append("*Element, type={}, elset={}".format(implementation, elset_name))
                for element in sorted(elements, key=lambda x: x.key):
                    part_data.append(element.jobdata)
                # if not isinstance(obj, RigidPart):
                part_data.append(section.jobdata(elset_name, orientation=orientation))
    return "\n".join(part_data)


@no_units
def _generate_sets_section(obj):
    return "\n".join([group.jobdata() for group in obj.groups])


@no_units
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
    return "\n".join(["*Instance, name={}-1, part={}".format(obj.name, obj.name), "*End Instance\n**"])


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
            orientation = "_".join(str(i) for i in el.frame.xaxis)
        except:
            orientation = None

        grouped_elements[implementation][section][orientation].add(el)

    return grouped_elements


class AbaqusPart(Part):
    """Abaqus implementation of :class:`Part`."""

    __doc__ = __doc__ or ""
    __doc__ += Part.__doc__ or ""

    def __init__(self, name=None, **kwargs):
        super(AbaqusPart, self).__init__(name=name, **kwargs)

    # =========================================================================
    #                       Generate input file data
    # =========================================================================
    def _group_elements(self):
        return _group_elements(self)

    @property
    @no_units
    def jobdata(self):
        return jobdata(self)

    @no_units
    def _generate_instance_jobdata(self):
        return _generate_instance_jobdata(self)


class AbaqusRigidPart(RigidPart):
    """Abaqus implementation of :class:`RigidPart`."""

    __doc__ = __doc__ or ""
    __doc__ += RigidPart.__doc__ or ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    @property
    @no_units
    def jobdata(self):
        return jobdata(self)

    @no_units
    def _generate_rigid_body_jobdata(self):
        return "*Rigid Body, ref node={0}-1.ref_point, elset={0}-1.all_elements".format(self.name)

    @no_units
    def _generate_instance_jobdata(self):
        return _generate_instance_jobdata(self)
