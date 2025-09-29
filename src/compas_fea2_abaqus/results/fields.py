from compas_fea2.results.fields import DisplacementFieldResults
from compas_fea2.results.fields import ReactionFieldResults
from compas_fea2.results.fields import SectionForcesFieldResults
from compas_fea2.results.fields import StressFieldResults
from compas_fea2.results.fields import ContactForcesFieldResults

from compas_fea2.units import no_units


class AbaqusDisplacementFieldResults(DisplacementFieldResults):
    """Abaqus implementation of :class:`DisplacementFieldResults`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += DisplacementFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "U"
        self.output_type = "node"

    @property
    @no_units
    def jobdata(self):
        return "U"


class AbaqusReactionFieldResults(ReactionFieldResults):
    """Abaqus implementation of :class:`ReactionFieldResults`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += ReactionFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "RF"
        self.output_type = "node"

    @property
    @no_units
    def jobdata(self):
        return "RF"


class AbaqusSectionForcesFieldResults(SectionForcesFieldResults):
    """Abaqus implementation of :class:`SectionForcesFieldResults`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += SectionForcesFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "SF"
        self.output_type = "element"

    @property
    @no_units
    def jobdata(self):
        return "SF"


class AbaqusStressFieldResults(StressFieldResults):
    """Abaqus implementation of :class:`StressFieldResults`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += StressFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "S"
        self.output_type = "element"

    @property
    @no_units
    def jobdata(self):
        return "S"


class AbaqusContactFieldResults(ContactForcesFieldResults):
    """Abaqus implementation of :class:`ContactForcesFieldResults`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += ContactForcesFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "CFORCE"
        self.output_type = "element"

    @property
    @no_units
    def jobdata(self):
        return "CFORCE"
