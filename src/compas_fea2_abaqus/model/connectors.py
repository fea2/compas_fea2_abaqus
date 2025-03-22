from compas_fea2.model import SpringConnector
from compas_fea2.model import ZeroLengthSpringConnector
# from compas_fea2.model import GroundSpringConnector


class AbaqusSpringConnector(SpringConnector):
    def __init__(self, master, slave, name=None, **kwargs):
        super(AbaqusSpringConnector, self).__init__(master, slave, tol=None, name=name, **kwargs)

    def jobdata(self, nodes):
        return f"*Element, type=Spring2, elset=Springs/Dashpots-{self.name}\n{self.input_key}, {self.nodes[0].part.name}-1.{self.nodes[0].input_key}, {self.nodes[-1].part.name}-1.{self.nodes[-1].input_key}"


class AbaqusZeroLengthSpringConnector(ZeroLengthSpringConnector):
    """Abaqus implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

    __doc__ += ZeroLengthSpringConnector.__doc__

    def __init__(self, nodes, section, directions, yielding=None, failure=None, **kwargs):
        super(AbaqusZeroLengthSpringConnector, self).__init__(nodes, section, directions, yielding, failure, **kwargs)

    def jobdata(self):
        return f"*Element, type=CONN3D2, elset=Springs/Dashpots-{self.name}\n{self.input_key}, {self.nodes[0].part.name}-1.{self.nodes[0].input_key}, {self.nodes[-1].part.name}-1.{self.nodes[-1].input_key}"


class AbaqusZeroLengthBeamConnector(AbaqusZeroLengthSpringConnector):
    """Abaqus implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

    __doc__ += ZeroLengthSpringConnector.__doc__

    def __init__(self, nodes, directions, yielding=None, failure=None, **kwargs):
        super(AbaqusZeroLengthSpringConnector, self).__init__(nodes, directions, yielding, failure, **kwargs)

    def jobdata(self):
        raise NotImplementedError()
        lines = []
        lines.append(f"*Element, type=CONN3D2, elset=Springs/Dashpots-{self.name}\n{self.input_key}, {self.nodes[0].part.name}-1.{self.nodes[0].input_key}, {self.nodes[-1].part.name}-1.{self.nodes[-1].input_key}")
        lines.append('*Connector Section, elset=Wire-2-Set-1\nBeam,\n"Datum csys-1",')


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
#             lines.append(f'{self.input_key*10000+c}, {n.part.name}-1.{n.input_key}')
#         return '\n'.join(lines)

