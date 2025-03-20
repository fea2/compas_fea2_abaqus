from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.results import DisplacementFieldResults
from compas_fea2.results import StressFieldResults
from compas_fea2.results import SectionForcesFieldResults
from compas_fea2.results import ReactionFieldResults



class AbaqusDisplacementFieldResults(DisplacementFieldResults):
    def __init__(self, step, *args, **kwargs):
        super(AbaqusDisplacementFieldResults, self).__init__(step, *args, **kwargs)


class AbaqusStressFieldResults(StressFieldResults):
    def __init__(self,step, *args, **kwargs):
        super(AbaqusStressFieldResults, self).__init__(step, *args, **kwargs)
