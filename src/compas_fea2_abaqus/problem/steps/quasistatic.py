from compas_fea2.problem import QuasiStaticStep
from compas_fea2.problem import DirectCyclicStep


class AbaqusQuasiStaticStep(QuasiStaticStep):
    def __init__(self, name=None, **kwargs):
        super(AbaqusQuasiStaticStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError


class AbaqusDirectCyclicStep(DirectCyclicStep):
    def __init__(self, name=None, **kwargs):
        super(AbaqusDirectCyclicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError
