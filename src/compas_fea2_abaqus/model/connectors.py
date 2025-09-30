from compas_fea2.model import SpringConnector
from compas_fea2.model import ZeroLengthSpringConnector
from compas_fea2.model import RigidLinkConnector
from compas_fea2.model import ZeroLengthContactConnector
from compas_fea2.model import LinearConnector

from compas_fea2.units import no_units

# from compas_fea2.model import GroundSpringConnector


class AbaqusLinearConnector(LinearConnector):
    """Abaqus implementation of :class:`compas_fea2.model.connectors.LinearConnector`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += LinearConnector.__doc__ or ""

    def __init__(self, master, slave, section, **kwargs):
        super(AbaqusLinearConnector, self).__init__(master, slave, section, **kwargs)
        self.implementation = "CONN3D2"

    @property
    @no_units
    def jobdata(self):
        data = [f"*Element, type={self.implementation}"]
        data += [f"{self.key}, {self.master.part.name}-1.{self.master.key}, {self.slave.part.name}-1.{self.slave.key}"]
        data += [f"*Connector Section, elset=set-{self.name}, behavior={self.section.name}"]
        data += ["Axial,"]
        return "\n".join(data)


class AbaqusSpringConnector(SpringConnector):
    """Abaqus implementation of :class:`compas_fea2.model.connectors.SpringConnector`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += SpringConnector.__doc__ or ""

    def __init__(self, master, slave, **kwargs):
        super(AbaqusSpringConnector, self).__init__(master, slave, tol=None, **kwargs)

    @property
    @no_units
    def jobdata(self):
        return f"*Element, type=Spring2, elset=Springs/Dashpots-{self.name}\n{self.key}, {self.nodes[0].part.name}-1.{self.nodes[0].key}, {self.nodes[-1].part.name}-1.{self.nodes[-1].key}"


class AbaqusZeroLengthSpringConnector(ZeroLengthSpringConnector):
    """Abaqus implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += ZeroLengthSpringConnector.__doc__ or ""

    def __init__(self, nodes, section, directions, yielding=None, failure=None, **kwargs):
        super(AbaqusZeroLengthSpringConnector, self).__init__(nodes, section, directions, yielding, failure, **kwargs)

    @property
    @no_units
    def jobdata(self):
        element_type = "CONN3D2"
        elset_name = f"Springs/Dashpots-{self.name}"
        node1 = f"{self.nodes[0].part.name}-1.{self.nodes[0].key}"
        node2 = f"{self.nodes[-1].part.name}-1.{self.nodes[-1].key}"
        return f"*Element, type={element_type}, elset={elset_name}\n{self.key}, {node1}, {node2}"


class AbaqusZeroLengthBeamConnector(AbaqusZeroLengthSpringConnector):
    """Abaqus implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += ZeroLengthSpringConnector.__doc__ or ""

    def __init__(self, nodes, directions, yielding=None, failure=None, **kwargs):
        super(AbaqusZeroLengthSpringConnector, self).__init__(nodes, directions, yielding, failure, **kwargs)

    @property
    @no_units
    def jobdata(self):
        raise NotImplementedError()
        lines = []
        lines.append(
            f"*Element, type=CONN3D2, elset=Springs/Dashpots-{self.name}\n{self.key}, {self.nodes[0].part.name}-1.{self.nodes[0].key}, {self.nodes[-1].part.name}-1.{self.nodes[-1].key}"
        )
        lines.append('*Connector Section, elset=Wire-2-Set-1\nBeam,\n"Datum csys-1",')


class AbaqusRigidLinkConnector(RigidLinkConnector):
    """Abaqus implementation of :class:`compas_fea2.model.connectors.RigidLinkConnector`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += RigidLinkConnector.__doc__ or ""

    def __init__(self, master, slave, name=None, **kwargs):
        super(AbaqusRigidLinkConnector, self).__init__(master, slave, name=name, **kwargs)
        raise NotImplementedError()


class AbaqusZeroLengthContactConnector(ZeroLengthContactConnector):
    """Abaqus implementation of :class:`compas_fea2.model.connectors.ZeroLengthContactConnector`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += ZeroLengthContactConnector.__doc__ or ""

    def __init__(self, master, slave, name=None, **kwargs):
        super(AbaqusZeroLengthContactConnector, self).__init__(master, slave, name=name, **kwargs)
        raise NotImplementedError()


# class AbaqusGroundSpringConnector(GroundSpringConnector):
#     """Abaqus implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

#     __doc__ += ZeroLengthSpringConnector.__doc__

#     def __init__(self, nodes, direction, **kwargs):
#         super(AbaqusGroundSpringConnector, self).__init__(nodes=nodes, direction=direction, yielding=None, failure=None, **kwargs)

#     def jobdata(self):
#         lines = []
#         # lines.append(f'*Spring, elset=Springs/Dashpots-{self.name}\n{3}\n{10000.}')
#         lines.append(f"*Element, type=Spring1, elset=Springs/Dashpots-{self.name}")
#         for c, n in enumerate(self.nodes, 1):
#             lines.append(f'{self.key*10000+c}, {n.part.name}-1.{n.key}')
#         return '\n'.join(lines)
