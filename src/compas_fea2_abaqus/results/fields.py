from compas_fea2.results.fields import DisplacementFieldResults
from compas_fea2.results.fields import ReactionFieldResults
from compas_fea2.results.fields import SectionForcesFieldResults
from compas_fea2.results.fields import StressFieldResults
from compas_fea2.results.fields import ContactForcesFieldResults
from compas_fea2.results.fields import TemperatureFieldResults

from compas_fea2.units import no_units


class AbaqusDisplacementFieldResults(DisplacementFieldResults):
    """Abaqus implementation of :class:`DisplacementFieldResults`.\n"""

    abaqus_field_names = ["U", "UR"]
    compas_to_abaqus_component_names = {
        "x": "U1",
        "y": "U2",
        "z": "U3",
        "xx": "UR1",
        "yy": "UR2",
        "zz": "UR3",
    }

    __doc__ = __doc__ or ""
    __doc__ += DisplacementFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "U"
        self.output_type = "node"

    @property
    @no_units
    def jobdata(self):
        return "*Node Output\nU"


class AbaqusReactionFieldResults(ReactionFieldResults):
    """Abaqus implementation of :class:`ReactionFieldResults`.\n"""

    abaqus_field_names = ["RF", "RM"]
    compas_to_abaqus_component_names = {
        "x": "RF1",
        "y": "RF2",
        "z": "RF3",
        "xx": "RM1",
        "yy": "RM2",
        "zz": "RM3",
    }

    __doc__ = __doc__ or ""
    __doc__ += ReactionFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "RF"
        self.output_type = "node"

    @property
    @no_units
    def jobdata(self):
        return "*Node Output\nRF"


class AbaqusSectionForcesFieldResults(SectionForcesFieldResults):
    """Abaqus implementation of :class:`SectionForcesFieldResults`.\n"""

    abaqus_field_names = ["SF", "SM"]
    compas_to_abaqus_component_names = {
        "Fx_1": "SF1",
        "Fz_1": "SF2",
        "Fy_1": "SF3",
        "Mx_1": "SM3",
        "My_1": "SM1",
        "Mz_1": "SM2",
        "Fx_2": "S",
        "Fz_2": "R",
        "Fy_2": "T",
        "Mx_2": "U",
        "My_2": "V",
        "Mz_2": "W",
    }

    __doc__ = __doc__ or ""
    __doc__ += SectionForcesFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "SF"
        self.output_type = "element"

    @property
    @no_units
    def jobdata(self):
        return "*Element Output, direction=YES\nSF"


class AbaqusStressFieldResults(StressFieldResults):
    """Abaqus implementation of :class:`StressFieldResults`.\n"""

    abaqus_field_names = ["S"]
    compas_to_abaqus_component_names = {
        "s11": "S11",
        "s22": "S22",
        "s33": "S33",
        "s12": "S12",
        "s13": "S13",
        "s23": "S23",
    }

    __doc__ = __doc__ or ""
    __doc__ += StressFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "S"
        self.output_type = "element"

    @property
    @no_units
    def jobdata(self):
        return "*Element Output, direction=YES\nS"


class AbaqusContactFieldResults(ContactForcesFieldResults):
    """Abaqus implementation of :class:`ContactForcesFieldResults`.\n"""

    abaqus_field_names = ["CNORMF", "CSHEARF"]
    compas_to_abaqus_component_names = {
        "Nx": "CNORMF1",
        "Ny": "CNORMF2",
        "Nz": "CNORMF3",
        "Tx": "CSHEARF1",
        "Ty": "CSHEARF2",
        "Tz": "CSHEARF3",
    }

    __doc__ = __doc__ or ""
    __doc__ += ContactForcesFieldResults.__doc__ or ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "CFORCE"
        self.output_type = "element"

    @property
    @no_units
    def jobdata(self):
        return "*Contact Output\nCFORCE,"


class AbaqusTemperatureFieldResults(TemperatureFieldResults):
    abaqus_field_names = ["NT"]
    compas_to_abaqus_component_names = {"T": "NT"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_name = "NT"
        self.output_type = "node"

    def jobdata(self):
        return "*Node Output\nNT"
