"""
********************************************************************************
compas_fea2_abaqus
********************************************************************************
"""

import os
from dotenv import load_dotenv

__author__ = ["Francesco Ranaudo"]
__copyright__ = "Francesco Ranaudo"
__license__ = "MIT License"
__email__ = "francesco.ranaudo@gmail.com"
__version__ = "0.1.0"

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

from pydoc import ErrorDuringImport
import compas_fea2


# Models
from compas_fea2.model import Model
from compas_fea2.model import Part
from compas_fea2.model import RigidPart
from compas_fea2.model import Node

# Elements
from compas_fea2.model.elements import (
    MassElement,
    LinkElement,
    BeamElement,
    TrussElement,
    MembraneElement,
    ShellElement,
    _Element3D,
    TetrahedronElement,
)

# Sections
from compas_fea2.model.sections import (
    AngleSection,
    BeamSection,
    BoxSection,
    CircularSection,
    HexSection,
    ISection,
    MassSection,
    PipeSection,
    RectangularSection,
    SpringSection,
    StrutSection,
    TieSection,
    TrapezoidalSection,
    TrussSection,
    MembraneSection,
    ShellSection,
    SolidSection,
)

# Materials
from compas_fea2.model.materials.material import (
    ElasticIsotropic,
    ElasticOrthotropic,
    ElasticPlastic,
    Stiff,
    UserMaterial,
)
from compas_fea2.model.materials.concrete import (
    Concrete,
    ConcreteDamagedPlasticity,
    ConcreteSmearedCrack,
)
from compas_fea2.model.materials.steel import (
    Steel,
)

# Groups
from compas_fea2.model.groups import (
    NodesGroup,
    ElementsGroup,
    FacesGroup,
)

# Constraints
from compas_fea2.model.constraints import (
    TieConstraint,
    TieMPC,
    BeamMPC,
)

# Connectors
from compas_fea2.model.connectors import (
    RigidLinkConnector,
    SpringConnector,
    ZeroLengthSpringConnector,
    ZeroLengthContactConnector,
    # GroundSpringConnector,
)

# Releases
from compas_fea2.model.releases import (
    BeamEndPinRelease,
)

# Boundary Conditions
from compas_fea2.model.bcs import (
    FixedBC,
    FixedBCX,
    FixedBCY,
    FixedBCZ,
    ClampBCXX,
    ClampBCYY,
    ClampBCZZ,
    PinnedBC,
    RollerBCX,
    RollerBCXY,
    RollerBCXZ,
    RollerBCY,
    RollerBCYZ,
    RollerBCZ,
)

# Initial Conditions
from compas_fea2.model.ics import (
    InitialTemperatureField,
    InitialStressField,
)

# Interactions
from compas_fea2.model.interactions import (
    HardContactFrictionPenalty,
    HardContactNoFriction,
    HardContactRough,
    LinearContactFrictionPenalty,
)

# Interfaces
from compas_fea2.model.interfaces import Interface

# Problem
from compas_fea2.problem import Problem

# Steps
from compas_fea2.problem.steps import (
    ModalAnalysis,
    ComplexEigenValue,
    StaticStep,
    LinearStaticPerturbation,
    BucklingAnalysis,
    DynamicStep,
    QuasiStaticStep,
    DirectCyclicStep,
)

# Loads
from compas_fea2.problem.loads import (
    ConcentratedLoad,
    # EdgeLoad,
    # FaceLoad,
    TributaryLoad,
    PrestressLoad,
    GravityLoad,
    HarmonicPointLoad,
    HarmonicPressureLoad,
)

# Displacements
from compas_fea2.problem.displacements import (
    GeneralDisplacement,
)

# Results
from compas_fea2.results import (
    DisplacementFieldResults,
    ReactionFieldResults,
    StressFieldResults,
    SectionForcesFieldResults,
    ContactForcesFieldResults,
)

# Input File
from compas_fea2.job import (
    InputFile,
    ParametersFile,
)

# =========================================================================
#                           Abaqus CLASSES
# =========================================================================

try:
    # Abaqus Models
    from .model import AbaqusModel
    from .model import AbaqusPart
    from .model import AbaqusRigidPart
    from .model import AbaqusNode

    # Abaqus Elements
    from .model.elements import (
        AbaqusMassElement,
        AbaqusLinkElement,
        AbaqusBeamElement,
        AbaqusTrussElement,
        AbaqusMembraneElement,
        AbaqusShellElement,
        _AbaqusElement3D,
        AbaqusTetrahedronElement,
    )

    # Abaqus Sections
    from .model.sections import (
        AbaqusAngleSection,
        AbaqusBeamSection,
        AbaqusBoxSection,
        AbaqusCircularSection,
        AbaqusHexSection,
        AbaqusISection,
        AbaqusMassSection,
        AbaqusPipeSection,
        AbaqusRectangularSection,
        AbaqusSpringSection,
        AbaqusStrutSection,
        AbaqusTieSection,
        AbaqusTrapezoidalSection,
        AbaqusTrussSection,
        AbaqusMembraneSection,
        AbaqusShellSection,
        AbaqusSolidSection,
    )

    # Abaqus Materials
    from .model.materials.material import (
        AbaqusElasticIsotropic,
        AbaqusElasticOrthotropic,
        AbaqusElasticPlastic,
        AbaqusStiff,
        AbaqusUserMaterial,
    )
    from .model.materials.concrete import (
        AbaqusConcrete,
        AbaqusConcreteDamagedPlasticity,
        AbaqusConcreteSmearedCrack,
    )
    from .model.materials.steel import (
        AbaqusSteel,
    )

    # Abaqus Groups
    from .model.groups import (
        AbaqusNodesGroup,
        AbaqusElementsGroup,
        AbaqusFacesGroup,
    )

    # Abaqus Constraints
    from .model.constraints import (
        AbaqusTieConstraint,
        AbaqusBeamMPC,
        AbaqusTieMPC,
    )

    # Abaqus Connectors
    from .model.connectors import (
        AbaqusSpringConnector,
        AbaqusZeroLengthSpringConnector,
        AbaqusRigidLinkConnector,
        AbaqusZeroLengthContactConnector,
        # AbaqusGroundSpringConnector,
    )

    # Abaqus release
    from .model.releases import (
        AbaqusBeamEndPinRelease,
    )

    # Abaqus Boundary Conditions
    from .model.bcs import (
        AbaqusFixedBC,
        AbaqusFixedBCX,
        AbaqusFixedBCY,
        AbaqusFixedBCZ,
        AbaqusClampBCXX,
        AbaqusClampBCYY,
        AbaqusClampBCZZ,
        AbaqusPinnedBC,
        AbaqusRollerBCX,
        AbaqusRollerBCXY,
        AbaqusRollerBCXZ,
        AbaqusRollerBCY,
        AbaqusRollerBCYZ,
        AbaqusRollerBCZ,
    )

    # Initial Conditions
    from .model.ics import (
        AbaqusInitialTemperatureField,
        AbaqusInitialStressField,
    )

    # Interactions
    from .model.interactions import (
        AbaqusHardContactFrictionPenalty,
        AbaqusHardContactRough,
        AbaqusLinearContactFrictionPenalty,
        AbaqusHardContactNoFriction,
    )

    # Abaqus Interfaces
    from .model.interfaces import AbaqusInterface

    # Abaqus Problem
    from .problem import AbaqusProblem

    # Abaqus Steps
    from .problem.steps import (
        AbaqusModalAnalysis,
        AbaqusComplexEigenValue,
        AbaqusStaticStep,
        AbaqusLinearStaticPerturbation,
        AbaqusBucklingAnalysis,
        AbaqusDynamicStep,
        AbaqusQuasiStaticStep,
        AbaqusDirectCyclicStep,
    )

    # Abaqus Loads
    from .problem.loads import (
        AbaqusConcentratedLoad,
        AbaqusTributaryLoad,
        AbaqusPrestressLoad,
        AbaqusGravityLoad,
        AbaqusHarmonicPointLoad,
        AbaqusHarmonicPressureLoad,
    )

    # Abaqus Displacements
    from .problem.displacements import (
        AbaqusGeneralDisplacement,
    )

    # Abaqus Results
    from .results import (
        AbaqusStressFieldResults,
        AbaqusDisplacementFieldResults,
        AbaqusReactionFieldResults,
        AbaqusContactFieldResults,
        AbaqusSectionForcesFieldResults,
    )

    # Abaqus Input File
    from .job import (
        AbaqusInputFile,
        AbaqusParametersFile,
    )

    # build the plugin registry
    def _register_backend():
        backend = compas_fea2.BACKENDS["compas_fea2_abaqus"]

        backend[Model] = AbaqusModel
        backend[Part] = AbaqusPart
        backend[RigidPart] = AbaqusRigidPart
        backend[Node] = AbaqusNode

        backend[MassElement] = AbaqusMassElement
        backend[LinkElement] = AbaqusLinkElement
        backend[BeamElement] = AbaqusBeamElement
        backend[TrussElement] = AbaqusTrussElement
        backend[MembraneElement] = AbaqusMembraneElement
        backend[ShellElement] = AbaqusShellElement
        backend[_Element3D] = _AbaqusElement3D
        backend[TetrahedronElement] = AbaqusTetrahedronElement

        backend[AngleSection] = AbaqusAngleSection
        backend[BeamSection] = AbaqusBeamSection
        backend[BoxSection] = AbaqusBoxSection
        backend[CircularSection] = AbaqusCircularSection
        backend[HexSection] = AbaqusHexSection
        backend[ISection] = AbaqusISection
        backend[MassSection] = AbaqusMassSection
        backend[MembraneSection] = AbaqusMembraneSection
        backend[PipeSection] = AbaqusPipeSection
        backend[RectangularSection] = AbaqusRectangularSection
        backend[ShellSection] = AbaqusShellSection
        backend[SolidSection] = AbaqusSolidSection
        backend[SpringSection] = AbaqusSpringSection
        backend[StrutSection] = AbaqusStrutSection
        backend[TieSection] = AbaqusTieSection
        backend[TrapezoidalSection] = AbaqusTrapezoidalSection
        backend[TrussSection] = AbaqusTrussSection

        backend[ElasticIsotropic] = AbaqusElasticIsotropic
        backend[ElasticOrthotropic] = AbaqusElasticOrthotropic
        backend[ElasticPlastic] = AbaqusElasticPlastic
        backend[Stiff] = AbaqusStiff
        backend[UserMaterial] = AbaqusUserMaterial
        backend[Concrete] = AbaqusConcrete
        backend[ConcreteDamagedPlasticity] = AbaqusConcreteDamagedPlasticity
        backend[ConcreteSmearedCrack] = AbaqusConcreteSmearedCrack
        backend[Steel] = AbaqusSteel

        backend[NodesGroup] = AbaqusNodesGroup
        backend[ElementsGroup] = AbaqusElementsGroup
        backend[FacesGroup] = AbaqusFacesGroup

        backend[TieConstraint] = AbaqusTieConstraint
        backend[TieMPC] = AbaqusTieMPC
        backend[BeamMPC] = AbaqusBeamMPC

        backend[SpringConnector] = AbaqusSpringConnector
        backend[ZeroLengthSpringConnector] = AbaqusZeroLengthSpringConnector
        backend[RigidLinkConnector] = AbaqusRigidLinkConnector
        backend[ZeroLengthContactConnector] = AbaqusZeroLengthContactConnector
        # backend[GroundSpringConnector] = AbaqusGroundSpringConnector

        backend[BeamEndPinRelease] = AbaqusBeamEndPinRelease

        backend[FixedBC] = AbaqusFixedBC
        backend[FixedBCX] = AbaqusFixedBCX
        backend[FixedBCY] = AbaqusFixedBCY
        backend[FixedBCZ] = AbaqusFixedBCZ
        backend[ClampBCXX] = AbaqusClampBCXX
        backend[ClampBCYY] = AbaqusClampBCYY
        backend[ClampBCZZ] = AbaqusClampBCZZ
        backend[PinnedBC] = AbaqusPinnedBC
        backend[RollerBCX] = AbaqusRollerBCX
        backend[RollerBCXY] = AbaqusRollerBCXY
        backend[RollerBCXZ] = AbaqusRollerBCXZ
        backend[RollerBCY] = AbaqusRollerBCY
        backend[RollerBCYZ] = AbaqusRollerBCYZ
        backend[RollerBCZ] = AbaqusRollerBCZ

        backend[InitialStressField] = AbaqusInitialStressField
        backend[InitialTemperatureField] = AbaqusInitialTemperatureField

        backend[HardContactFrictionPenalty] = AbaqusHardContactFrictionPenalty
        backend[HardContactRough] = AbaqusHardContactRough
        backend[LinearContactFrictionPenalty] = AbaqusLinearContactFrictionPenalty
        backend[HardContactNoFriction] = AbaqusHardContactNoFriction

        backend[Interface] = AbaqusInterface

        backend[Problem] = AbaqusProblem

        backend[ModalAnalysis] = AbaqusModalAnalysis
        backend[ComplexEigenValue, StaticStep] = AbaqusComplexEigenValue
        backend[StaticStep] = AbaqusStaticStep
        backend[LinearStaticPerturbation] = AbaqusLinearStaticPerturbation
        backend[BucklingAnalysis] = AbaqusBucklingAnalysis
        backend[DynamicStep] = AbaqusDynamicStep
        backend[QuasiStaticStep] = AbaqusQuasiStaticStep
        backend[DirectCyclicStep] = AbaqusDirectCyclicStep

        backend[GravityLoad] = AbaqusGravityLoad
        backend[ConcentratedLoad] = AbaqusConcentratedLoad
        backend[TributaryLoad] = AbaqusTributaryLoad
        backend[PrestressLoad] = AbaqusPrestressLoad
        backend[HarmonicPointLoad] = AbaqusHarmonicPointLoad
        backend[HarmonicPressureLoad] = AbaqusHarmonicPressureLoad

        backend[GeneralDisplacement] = AbaqusGeneralDisplacement

        backend[StressFieldResults] = AbaqusStressFieldResults
        backend[DisplacementFieldResults] = AbaqusDisplacementFieldResults
        backend[ReactionFieldResults] = AbaqusReactionFieldResults
        backend[ContactForcesFieldResults] = AbaqusContactFieldResults
        backend[SectionForcesFieldResults] = AbaqusSectionForcesFieldResults

        backend[InputFile] = AbaqusInputFile
        backend[ParametersFile] = AbaqusParametersFile

        print("Abaqus implementations registered...")

except:
    raise ErrorDuringImport()


def init_fea2_abaqus(exe):
    """Create a default environment file if it doesn't exist and loads its variables.

    Parameters
    ----------
    verbose : bool, optional
        Be verbose when printing output, by default False
    point_overlap : bool, optional
        Allow two nodes to be at the same location, by default True
    global_tolerance : int, optional
        Tolerance for the model, by default 1
    precision : str, optional
        Values approximation, by default '3f'

    """

    env_path = os.path.abspath(os.path.join(HERE, ".env"))
    with open(env_path, "x") as f:
        f.write(
            "\n".join(
                [
                    "EXE={}".format(exe),
                ]
            )
        )
    load_dotenv(env_path)


if not load_dotenv():

    from sys import platform

    if platform == "linux" or platform == "linux2":
        # linux
        raise NotImplementedError()
    elif platform == "darwin":
        # OS X
        # raise SystemError("Abaqus is not available on Mac")
        exe = NotImplementedError()
    elif platform == "win32":
        # Windows
        exe = "C:/SIMULIA/Commands"
    else:
        raise ValueError("you must specify the location of the solver.")
    init_fea2_abaqus(exe)

EXE = os.getenv("EXE")
