from compas_fea2.problem import QuasiStaticStep
from compas_fea2.problem import DirectCyclicStep


class AbaqusQuasiStaticStep(QuasiStaticStep):
    """Abaqus implementation of :class:`compas_fea2.problem.QuasiStaticStep`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += QuasiStaticStep.__doc__ or ""

    def __init__(self, name=None, **kwargs):
        super(AbaqusQuasiStaticStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError


class AbaqusDirectCyclicStep(DirectCyclicStep):
    """Abaqus implementation of :class:`compas_fea2.problem.DirectCyclicStep`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += DirectCyclicStep.__doc__ or ""

    def __init__(self, name=None, **kwargs):
        super(AbaqusDirectCyclicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError
