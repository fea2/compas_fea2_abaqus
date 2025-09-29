from compas_fea2.problem import DynamicStep


class AbaqusDynamicStep(DynamicStep):
    """Abaqus implementation of :class:`compas_fea2.problem.DynamicStep`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += DynamicStep.__doc__ or ""

    def __init__(self, name=None, **kwargs):
        super(AbaqusDynamicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError
