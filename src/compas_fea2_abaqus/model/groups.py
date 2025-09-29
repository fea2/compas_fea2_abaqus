from compas_fea2.model import NodesGroup
from compas_fea2.model import ElementsGroup
from compas_fea2.model.groups import FacesGroup
from compas_fea2.model.groups import MaterialsGroup
from itertools import groupby

from compas_fea2.units import no_units


@no_units
def jobdata(self, instance):
    """Generates the common string information for the input file for all the
    groups.

    Parameters
    ----------
    instance: bool
        if ``True`` the set is generated at the instance level, otherwise only
        at the part level

    Returns
    -------
    input file data line (str).
    """
    data_section = []
    name = self.name if not instance else f"{self.name}_i"
    line = "*{0}, {0}={1}".format(self._set_type, name)
    if instance:
        for part, members in groupby(self._members, key=lambda x: x.part):
            data_section.append(line + f", instance={part.name + "-1"}")
            data = [str(member.key) for member in members]
            chunks = [data[x : x + 15] for x in range(0, len(data), 15)]  # split data for readibility
            for chunk in chunks:
                data_section.append(", ".join(chunk))
    else:
        data_section.append(line)
        data = [str(member.key) for member in self._members]
        chunks = [data[x : x + 15] for x in range(0, len(data), 15)]  # split data for readibility
        for chunk in chunks:
            data_section.append(", ".join(chunk))
    return "\n".join(data_section)


class AbaqusNodesGroup(NodesGroup):
    """Abaqus implementation of :class:`NodesGroup`

    Notes
    -----
    This is equivalent to a node set in Abaqus

    """

    __doc__ = __doc__ or ""
    __doc__ += NodesGroup.__doc__ or ""

    def __init__(self, members, **kwargs):
        super(AbaqusNodesGroup, self).__init__(members=members, **kwargs)
        self._set_type = "nset"

    @no_units
    def jobdata(self, instance=None):
        return jobdata(self, instance)


class AbaqusElementsGroup(ElementsGroup):
    """Abaqus implementation of :class:`ElementsGroup`

    Notes
    -----
    This is equivalent to a element set in Abaqus

    """

    __doc__ = __doc__ or ""
    __doc__ += ElementsGroup.__doc__ or ""

    def __init__(self, members, **kwargs):
        super(AbaqusElementsGroup, self).__init__(members=members, **kwargs)
        self._set_type = "elset"

    @no_units
    def jobdata(self, instance=None):
        return jobdata(self, instance)


class AbaqusFacesGroup(FacesGroup):
    """Abaqus implementation of :class:`FacesGroup`

    Notes
    -----
    This is equivalent to a `Surface` in Abaqus

    """

    __doc__ = __doc__ or ""
    __doc__ += NodesGroup.__doc__ or ""

    def __init__(self, members, **kwargs):
        super(AbaqusFacesGroup, self).__init__(members=members, **kwargs)

    @property
    @no_units
    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            input file data line.
        """
        lines = ["*Surface, type=ELEMENT, name={}_i".format(self._name)]
        for face in self.faces:
            lines.append("{}-1.{}, {}".format(face.part.name, face.element.key, face.tag))
        lines.append("**")
        return "\n".join(lines)

class AbaqusMaterialsGroup(MaterialsGroup):
    """Calculix implementation of :class:`MaterialsGroup`

    Notes
    -----
    This is equivalent to a material set in Calculix

    """

    __doc__ = (__doc__ or "") + (MaterialsGroup.__doc__ or "")

    def __init__(self, members, **kwargs):
        super(AbaqusMaterialsGroup, self).__init__(members=members, **kwargs)
        self._set_type = "mset"

    @property
    @no_units
    def jobdata(self):
        return '\n'.join([material.jobdata for material in self.members])