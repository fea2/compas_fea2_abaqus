from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import LoadCombination

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']

# TODO check if `modify` can be moved to _base


class AbaqusLoadCombination(LoadCombination):
    """OpenSees implementation of :class:`compas_fea2.problem.LoadCombination`.\n
    """
    __doc__ += LoadCombination.__doc__

    def __init__(self, factors, name=None, **kwargs):
        super(AbaqusLoadCombination, self).__init__(factors=factors, name=name, **kwargs)

    def jobdata(self):
        index = self.problem._steps_order.index(self.step)
        factor = 1
        #TODO check if possible to create LC in OpenSees
        loads = '\n'.join([load.jobdata(node) for node, load in self.node_load])

        return f"pattern Plain {index} {index} -fact {factor} {{\n{loads}\n}}"
