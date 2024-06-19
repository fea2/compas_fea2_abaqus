from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import SpringConnector
from compas_fea2.model import ZeroLengthSpringConnector


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


class AbaqusZeroLengthBeamConnector():
    """Abaqus implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

    __doc__ += ZeroLengthSpringConnector.__doc__

    def __init__(self, nodes, directions, yielding=None, failure=None, **kwargs):
        super(AbaqusZeroLengthSpringConnector, self).__init__(nodes, directions, yielding, failure, **kwargs)

    def jobdata(self):
        raise NotImplementedError()
        lines = []
        lines.append(f"*Element, type=CONN3D2, elset=Springs/Dashpots-{self.name}\n{self.input_key}, {self.nodes[0].part.name}-1.{self.nodes[0].input_key}, {self.nodes[-1].part.name}-1.{self.nodes[-1].input_key}")
        lines.append('*Connector Section, elset=Wire-2-Set-1\nBeam,\n"Datum csys-1",')
