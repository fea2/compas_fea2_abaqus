from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import SpringConnector
from compas_fea2.model import ZeroLengthSpringConnector


class AbaqusSpringConnector(SpringConnector):
    def __init__(self, master, slave, name=None, **kwargs):
        super(AbaqusSpringConnector, self).__init__(master, slave, tol=None, name=name, **kwargs)
        raise NotImplementedError


class AbaqusZeroLengthSpringConnector(ZeroLengthSpringConnector):
    """Abaqus implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

    __doc__ += ZeroLengthSpringConnector.__doc__

    def __init__(self, nodes, section, directions, yielding=None, failure=None, **kwargs):
        super(AbaqusZeroLengthSpringConnector, self).__init__(nodes, section, directions, yielding, failure, **kwargs)
        raise NotImplementedError
