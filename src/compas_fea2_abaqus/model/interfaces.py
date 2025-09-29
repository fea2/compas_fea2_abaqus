from compas_fea2.model import _Interface
from compas_fea2.model.interfaces import BoundaryInterface, PartPartInterface
from compas_fea2.model import Contact
from compas_fea2.model import _Constraint


class AbaqusPartPartInterface(PartPartInterface):
    """Abaqus implementation of :class:`Interface`.

    Note
    ----
    This is equivalent to a `Contact Pair` in Abaqus.

    """

    __doc__ += PartPartInterface.__doc__

    def __init__(
        self,
        master,
        slave,
        behavior,
        small_sliding=False,
        adjust=0,
        no_tickness=False,
        **kwargs,
    ):
        super(AbaqusPartPartInterface, self).__init__(master=master, slave=slave, behavior=behavior, **kwargs)

        self._small_sliding = ", small sliding" if small_sliding else ""
        self._no_tickness = ", no tickness" if no_tickness else ""
        self._adjust = ", adjust={}".format(adjust) if adjust else ""

    def _generate_jobdata(self):
        if isinstance(self.behavior, Contact):
            return f"""** Interface: {self._name}
*Contact Pair, interaction={self._behavior.name}, type=SURFACE TO SURFACE{self._no_tickness}{self._small_sliding}{self._adjust}
{self._master.name}_i, {self._slave.name}_i
**"""

        elif isinstance(self.behavior, _Constraint):
            return f"{self.behavior.jobdata()}, {self.master.name}, {self.slave.name}\n**"

    def _generate_controls_jobdata(self):
        return f"""**
*CONTACT CONTROLS,  STABILIZE, MASTER={self._master.name}_i, SLAVE ={self._slave.name}_i
**"""

class AbaqusBoundaryInterface(BoundaryInterface):
    def __init__(
        master,
        behavior,
        **kwargs,
    ):
        super().__init__(master=master, behavior=behavior, **kwargs)
    
    def _generate_jobdata(self):
        return self.behavior.jobdata(self.master)