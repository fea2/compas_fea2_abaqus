from compas_fea2.model import GeneralBC
from compas_fea2.model import FixedBC
from compas_fea2.model import FixedBCX
from compas_fea2.model import FixedBCY
from compas_fea2.model import FixedBCZ
from compas_fea2.model import PinnedBC
from compas_fea2.model import ClampBCXX
from compas_fea2.model import ClampBCYY
from compas_fea2.model import ClampBCZZ
from compas_fea2.model import RollerBCX
from compas_fea2.model import RollerBCY
from compas_fea2.model import RollerBCZ
from compas_fea2.model import RollerBCXY
from compas_fea2.model import RollerBCYZ
from compas_fea2.model import RollerBCXZ
from compas_fea2.model.bcs import ImposedTemperature


dofs = ["x", "y", "z", "xx", "yy", "zz"]


def _jobdata(bc, nodes):
    """Generates the string information for the input file.

    Note
    ----
    A node set is created during the input file generation to group the application
    point of the boundary condition. The new set name follows this name scheme:
    `_aux_{bc.name}_{instance_name}`

    Note
    ----
    Ideally, this would have not been necessary
    because it is possible to retreive nodes within the Assembly-Part definition
    by just using the format `instance_name.node_key`. However Tosca Structure
    throws an exception during the flattening of the input file (it can not run
    if the model is organised in Assembly and Parts). Below the orginal implementation
    for future reference.

    .. code-block:: python

        data_section = [f'** Name: {bc.name} Type: BC/Rotation',
                        '*Boundary, op=NEW']
        for node in nodes:
            for comp, dof in enumerate(dofs, 1):
                if dof in bc.components:
                    data_section += [f'{instance}.{node+1}, {comp}, {bc.components[dof]}']

    Parameters
    ----------
    bc : :class:`compas_fea2.model._BoundaryCondition`
        The boundary condition.
    nodes: list
        List of the node where the boundary condition is applied.

    Returns
    -------
    input file data line (str).

    """
    data_section = [
        "** Name: {} Type: BC/Rotation".format(bc.name),
        "*Boundary, op=NEW",
    ]
    for node in nodes:
        for comp, dof in enumerate(dofs, 1):
            if getattr(bc, dof):
                data_section += ["{}.{}, {}, 0".format("{}-1".format(node.part.name), node.key, comp)]
    return "\n".join(data_section)


class AbaqusGeneralBC(GeneralBC):
    """Abaqus implementation of :class:`compas_fea2.model.GeneralBC`.\n"""

    __doc__ += GeneralBC.__doc__

    def __init__(self, **kwargs):
        super(AbaqusGeneralBC, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusFixedBC(FixedBC):
    """Abaqus implementation of :class:`compas_fea2.model.FixedBC`.\n"""

    __doc__ += FixedBC.__doc__

    def __init__(self, **kwargs):
        super(AbaqusFixedBC, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusFixedBCX(FixedBCX):
    """Abaqus implementation of :class:`compas_fea2.model.FixedBCX`.\n"""

    __doc__ += FixedBCX.__doc__

    def __init__(self, **kwargs):
        super(AbaqusFixedBCX, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusFixedBCY(FixedBCY):
    """Abaqus implementation of :class:`compas_fea2.model.FixedBCY`.\n"""

    __doc__ += FixedBCY.__doc__

    def __init__(self, **kwargs):
        super(AbaqusFixedBCY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusFixedBCZ(FixedBCZ):
    """Abaqus implementation of :class:`compas_fea2.model.FixedBCZ`.\n"""

    __doc__ += FixedBCZ.__doc__

    def __init__(self, **kwargs):
        super(AbaqusFixedBCZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusPinnedBC(PinnedBC):
    """Abaqus implementation of :class:`compas_fea2.model.PinnedBC`.\n"""

    __doc__ += PinnedBC.__doc__

    def __init__(self, **kwargs):
        super(AbaqusPinnedBC, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusClampBCXX(ClampBCXX):
    """Abaqus implementation of :class:`compas_fea2.model.ClampBCXX`.\n"""

    __doc__ += ClampBCXX.__doc__

    def __init__(self, **kwargs):
        super(AbaqusClampBCXX, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusClampBCYY(ClampBCYY):
    """Abaqus implementation of :class:`compas_fea2.model.ClampBCYY`.\n"""

    __doc__ += ClampBCYY.__doc__

    def __init__(self, **kwargs):
        super(AbaqusClampBCYY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusClampBCZZ(ClampBCZZ):
    """Abaqus implementation of :class:`ClampBCZZ`.\n"""

    __doc__ += ClampBCZZ.__doc__

    def __init__(self, **kwargs):
        super(AbaqusClampBCZZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusRollerBCX(RollerBCX):
    """Abaqus implementation of :class:`RollerBCX`.\n"""

    __doc__ += RollerBCX.__doc__

    def __init__(self, **kwargs):
        super(AbaqusRollerBCX, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusRollerBCY(RollerBCY):
    """Abaqus implementation of :class:`RollerBCY`.\n"""

    __doc__ += RollerBCY.__doc__

    def __init__(self, **kwargs):
        super(AbaqusRollerBCY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusRollerBCZ(RollerBCZ):
    """Abaqus implementation of :class:`RollerBCZ`.\n"""

    __doc__ += RollerBCZ.__doc__

    def __init__(self, **kwargs):
        super(AbaqusRollerBCZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusRollerBCXY(RollerBCXY):
    """Abaqus implementation of :class:`RollerBCXY`.\n"""

    __doc__ += RollerBCXY.__doc__

    def __init__(self, **kwargs):
        super(AbaqusRollerBCXY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusRollerBCYZ(RollerBCYZ):
    """Abaqus implementation of :class:`RollerBCYZ`.\n"""

    __doc__ += RollerBCYZ.__doc__

    def __init__(self, **kwargs):
        super(AbaqusRollerBCYZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusRollerBCXZ(RollerBCXZ):
    """Abaqus implementation of :class:`RollerBCXZ`.\n"""

    __doc__ += RollerBCXZ.__doc__

    def __init__(self, **kwargs):
        super(AbaqusRollerBCXZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class AbaqusImposedTemperature(ImposedTemperature):
    def __init__(self, temperature, **kwargs):
        super().__init__(temperature=temperature, **kwargs)

    def jobdata(self, nodes):
        data_section = [
            "** Name: {} Type: Temperature".format(self.name),
            "*Boundary, op=New",
        ]
        for node in nodes:
            # if getattr(self, '_temp'):
            data_section += [f"{node.part.name}-1.{node.key}, 11, 11, {self.temperature}"]
        return "\n".join(data_section)
    