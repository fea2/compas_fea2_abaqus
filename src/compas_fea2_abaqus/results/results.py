from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path

from compas_fea2.results import Results, NodeFieldResults
from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import launch_process


class AbaqusResults(Results):
    """Abaqus implementation of :class:`Results`.\n"""
    __doc__ += Results.__doc__

    def __init__(self, location, components, invariants, name=None, *kwargs):
        super(AbaqusResults, self).__init__(location, components, invariants, name=name, *kwargs)



class AbaqusNodeFieldResults(NodeFieldResults):
    def __init__(self, field_name,step, name=None, *args, **kwargs):
        """Abaqus implementation of :class:`NodeFieldResults`.\n
        """
        super(AbaqusNodeFieldResults, self).__init__(field_name, step, name, *args, **kwargs)
