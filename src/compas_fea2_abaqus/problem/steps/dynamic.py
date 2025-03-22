from compas_fea2.problem import DynamicStep


class AbaqusDynamicStep(DynamicStep):
    def __init__(self, name=None, **kwargs):
        super(AbaqusDynamicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError
