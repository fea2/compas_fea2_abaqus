from compas_fea2.model import Contact
from compas_fea2.model import _Constraint
from compas_fea2.model.interfaces import PartPartInterface

from compas_fea2.units import no_units


class AbaqusPartPartInterface(PartPartInterface):
    """Abaqus implementation of :class:`Interface`.

    Note
    ----
    This is equivalent to a `Contact Pair` in Abaqus.

    """

    __doc__ = __doc__ or ""
    __doc__ += PartPartInterface.__doc__ or ""

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
        super().__init__(master=master, slave=slave, behavior=behavior, **kwargs)

        self._small_sliding = ", small sliding" if small_sliding else ""
        self._no_tickness = ", no tickness" if no_tickness else ""
        self._adjust = ", adjust={}".format(adjust) if adjust else ""

    @property
    @no_units
    def jobdata(self):
        if isinstance(self.behavior, Contact):
            return f"""** Interface: {self._name}
*Contact Pair, interaction={self._behavior.name}, type=SURFACE TO SURFACE{self._no_tickness}{self._small_sliding}{self._adjust}
{self._master.name}_i, {self._slave.name}_i
**"""

        elif isinstance(self.behavior, _Constraint):
            return f"{self.behavior.jobdata()}{self._slave.name}_i, {self._master.name}_i\n**"


#     @property
#     @no_units
#     def jobdata(self):
#         return f"""**
# *CONTACT CONTROLS,  STABILIZE, MASTER={self._master.name}_i, SLAVE ={self._slave.name}_i
# **"""
