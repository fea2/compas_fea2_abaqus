from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Interface
from compas_fea2.model import Contact
from compas_fea2.model import _Constraint

# TODO maybe move the extra parameters to base


class AbaqusInterface(Interface):
    """Abaqus implementation of :class:`Interface`.

    Note
    ----
    This is equivalent to a `Contact Pair` in Abaqus.

    """
    __doc__ += Interface.__doc__

    def __init__(self, master, slave, behavior, small_sliding=False, adjust=0, no_tickness=False, **kwargs):
        super(AbaqusInterface, self).__init__(master=master, slave=slave, behavior=behavior, **kwargs)

        self._small_sliding = ', small sliding' if small_sliding else ''
        self._no_tickness = ', no tickness' if no_tickness else ''
        self._adjust = ', adjust={}'.format(adjust) if adjust else ''

    def _generate_jobdata(self):
        if isinstance(self.behavior, Contact):
            return """** Interface: {}
*Contact Pair, interaction={}, type=SURFACE TO SURFACE{}{}{}
{}_i, {}_i
**""".format(self._name,
             self._behavior.name,
             self._no_tickness,
             self._small_sliding,
             self._adjust,
             self._master.name,
             self._slave.name)

        elif isinstance(self.behavior, _Constraint):
            return "{}{}_i, {}_i\n**".format(self.behavior._generate_jobdata(), self._slave.name, self._master.name,)

    def _generate_controls_jobdata(self):
        return """**
*CONTACT CONTROLS,  STABILIZE, MASTER={}_i, SLAVE ={}_i
**""".format(self._master.name,
             self._slave.name)

#         return """**
# *CONTACT CONTROLS, APPROACH, MASTER={}, SLAVE ={}
# **""".format(self._master.name,
#              self._slave.name)
