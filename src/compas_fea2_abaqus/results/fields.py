from compas_fea2.results.fields import DisplacementFieldResults
from compas_fea2.results.fields import ReactionFieldResults
from compas_fea2.results.fields import SectionForcesFieldResults
from compas_fea2.results.fields import StressFieldResults
from compas_fea2.results.fields import ContactForcesFieldResults
from compas_fea2.results.fields import TemperatureFieldResults


class AbaqusDisplacementFieldResults(DisplacementFieldResults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "U"
        self.output_type = "node"

    def jobdata(self):
        return "U"


class AbaqusReactionFieldResults(ReactionFieldResults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "RF"
        self.output_type = "node"

    def jobdata(self):
        return "RF"


class AbaqusSectionForcesFieldResults(SectionForcesFieldResults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "SF"
        self.output_type = "element"

    def jobdata(self):
        return "SF"


class AbaqusStressFieldResults(StressFieldResults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "S"
        self.output_type = "element"

    def jobdata(self):
        return "S"


class AbaqusContactFieldResults(ContactForcesFieldResults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "CFORCE"
        self.output_type = "element"

    def jobdata(self):
        return "CFORCE"


class AbaqusTemperatureFieldResults(TemperatureFieldResults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "NT"
        self.output_type = "node"

    def jobdata(self):
        return "NT"
