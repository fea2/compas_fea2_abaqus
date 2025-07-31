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

from pydoc import ErrorDuringImport  # noqa: E402
import compas_fea2  # noqa: E402


# Models
from compas_fea2.model import Model  # noqa: E402
from compas_fea2.model import Part  # noqa: E402
from compas_fea2.model import RigidPart  # noqa: E402
from compas_fea2.model import Node  # noqa: E402

# Elements
from compas_fea2.model.elements import (  # noqa: E402
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
from compas_fea2.model.sections import (  # noqa: E402
    SpringSection,
    AngleSection,
    GenericBeamSection,
    BoxSection,
    CircularSection,
    HexSection,
    ISection,
    # MassSection,
    PipeSection,
    RectangularSection,
    StrutSection,
    TieSection,
    TrapezoidalSection,
    TrussSection,
    MembraneSection,
    ShellSection,
    SolidSection,
)

# Materials
from compas_fea2.model.materials.material import (  # noqa: E402
    ElasticIsotropic,
    ElasticOrthotropic,
    ElasticPlastic,
    Stiff,
    UserMaterial,
    ThermalElasticIsotropic,
)
from compas_fea2.model.materials.concrete import (  # noqa: E402
    Concrete,
    ConcreteDamagedPlasticity,
    ConcreteSmearedCrack,
)
from compas_fea2.model.materials.steel import (  # noqa: E402
    Steel,
)
from compas_fea2.model.materials.timber import (  # noqa: E402
    Timber,
)

# Groups
from compas_fea2.model.groups import (  # noqa: E402
    # NodesGroup,
    ElementsGroup,
    FacesGroup,
    EdgesGroup,
)

# Constraints
from compas_fea2.model.constraints import (  # noqa: E402
    TieConstraint,
    TieMPC,
    BeamMPC,
)

# Connectors
from compas_fea2.model.connectors import (  # noqa: E402
    RigidLinkConnector,
    SpringConnector,
    ZeroLengthSpringConnector,
    ZeroLengthContactConnector,
    # GroundSpringConnector,
)

# Releases
from compas_fea2.model.releases import (  # noqa: E402
    BeamEndPinRelease,
)

# Boundary Conditions
from compas_fea2.model.bcs import (  # noqa: E402
    GeneralBC,
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
    ImposedTemperature,
    ImposedHeatFlux
)

# Initial Conditions
from compas_fea2.model.ics import (  # noqa: E402
    InitialTemperatureField,
    InitialStressField,
)

# Interactions
from compas_fea2.model.interactions import (  # noqa: E402
    HardContactFrictionPenalty,
    # HardContactNoFriction,
    HardContactRough,
    LinearContactFrictionPenalty,
    Convection,
    Radiation,
)

# Interfaces
# from compas_fea2.model.interfaces import Interface

# Problem
from compas_fea2.problem import Problem  # noqa: E402

# Steps
from compas_fea2.problem.steps import (  # noqa: E402
    ModalAnalysis,
    ComplexEigenValue,
    StaticStep,
    LinearStaticPerturbation,
    BucklingAnalysis,
    DynamicStep,
    QuasiStaticStep,
    DirectCyclicStep,
    HeatTransferStep,
)

# Loads
from compas_fea2.problem.loads import (  # noqa: E402
    ScalarLoad,
    VectorLoad
)

# Fields
from compas_fea2.problem.fields import (  # noqa: E402
    # TemperatureField,
    PrescribedTemperatureField
)


# Displacements
from compas_fea2.problem.displacements import (  # noqa: E402
    GeneralDisplacement,
)

# Results
from compas_fea2.results import (  # noqa: E402
    DisplacementFieldResults,
    ReactionFieldResults,
    StressFieldResults,
    SectionForcesFieldResults,
    ContactForcesFieldResults,
    TemperatureFieldResults,
)

# Input File
from compas_fea2.job import (  # noqa: E402
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
        AbaqusSpringSection,
        # AbaqusConnectorSection,
        AbaqusAngleSection,
        AbaqusGenericBeamSection,
        AbaqusBoxSection,
        AbaqusCircularSection,
        AbaqusHexSection,
        AbaqusISection,
        # AbaqusMassSection,
        AbaqusPipeSection,
        AbaqusRectangularSection,
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
        AbaqusThermalElasticIsotropic,
    )
    from .model.materials.concrete import (
        AbaqusConcrete,
        AbaqusConcreteDamagedPlasticity,
        AbaqusConcreteSmearedCrack,
    )
    from .model.materials.steel import (
        AbaqusSteel,
    )
    from .model.materials.timber import (
        AbaqusTimber,
    )

    # Abaqus Groups
    from .model.groups import (
        # AbaqusNodesGroup,
        AbaqusElementsGroup,
        AbaqusFacesGroup,
        AbaqusEdgesGroup,
    )

    # Abaqus Constraints
    from .model.constraints import (
        AbaqusTieConstraint,
        AbaqusBeamMPC,
        AbaqusTieMPC,
    )

    # Abaqus Connectors
    from .model.connectors import (
        # AbaqusLinearConnector,
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
        AbaqusGeneralBC,
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
        AbaqusImposedTemperature,
        AbaqusImposedHeatFlux
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
        # AbaqusHardContactNoFriction,
        AbaqusConvection,
        AbaqusRadiation,
    )

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
        AbaqusHeatTransferStep,
    )

    # Abaqus Loads
    from .problem.loads import (
        AbaqusScalarLoad,
        AbaqusVectorLoad
    )

    # Abaqus Displacements
    from .problem.displacements import (
        AbaqusGeneralDisplacement,
    )

    # Abaqus LoadFields
    from .problem.fields import (
        AbaqusPrescribedTemperatureField,
    )

    # Abaqus Results
    from .results import (
        AbaqusStressFieldResults,
        AbaqusDisplacementFieldResults,
        AbaqusReactionFieldResults,
        AbaqusContactFieldResults,
        AbaqusSectionForcesFieldResults,
        AbaqusTemperatureFieldResults,
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

        backend[SpringSection] = AbaqusSpringSection
        backend[AngleSection] = AbaqusAngleSection
        backend[GenericBeamSection] = AbaqusGenericBeamSection
        backend[BoxSection] = AbaqusBoxSection
        backend[CircularSection] = AbaqusCircularSection
        backend[HexSection] = AbaqusHexSection
        backend[ISection] = AbaqusISection
        # backend[MassSection] = AbaqusMassSection
        backend[MembraneSection] = AbaqusMembraneSection
        backend[PipeSection] = AbaqusPipeSection
        backend[RectangularSection] = AbaqusRectangularSection
        backend[ShellSection] = AbaqusShellSection
        backend[SolidSection] = AbaqusSolidSection
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
        backend[ThermalElasticIsotropic] = AbaqusThermalElasticIsotropic
        backend[Timber] = AbaqusTimber

        # backend[NodesGroup] = AbaqusNodesGroup
        backend[ElementsGroup] = AbaqusElementsGroup
        backend[EdgesGroup] = AbaqusEdgesGroup
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

        backend[GeneralBC] = AbaqusGeneralBC
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
        backend[ImposedTemperature] = AbaqusImposedTemperature
        backend[ImposedHeatFlux] = AbaqusImposedHeatFlux

        backend[InitialStressField] = AbaqusInitialStressField
        backend[InitialTemperatureField] = AbaqusInitialTemperatureField

        backend[HardContactFrictionPenalty] = AbaqusHardContactFrictionPenalty
        backend[HardContactRough] = AbaqusHardContactRough
        backend[LinearContactFrictionPenalty] = AbaqusLinearContactFrictionPenalty
        # backend[HardContactNoFriction] = AbaqusHardContactNoFriction

        backend[Convection] = AbaqusConvection
        backend[Radiation] = AbaqusRadiation

        backend[Problem] = AbaqusProblem

        backend[ModalAnalysis] = AbaqusModalAnalysis
        backend[ComplexEigenValue, StaticStep] = AbaqusComplexEigenValue
        backend[StaticStep] = AbaqusStaticStep
        backend[LinearStaticPerturbation] = AbaqusLinearStaticPerturbation
        backend[BucklingAnalysis] = AbaqusBucklingAnalysis
        backend[DynamicStep] = AbaqusDynamicStep
        backend[QuasiStaticStep] = AbaqusQuasiStaticStep
        backend[DirectCyclicStep] = AbaqusDirectCyclicStep
        backend[HeatTransferStep] = AbaqusHeatTransferStep

        backend[ScalarLoad] = AbaqusScalarLoad
        backend[VectorLoad] = AbaqusVectorLoad

        backend[GeneralDisplacement] = AbaqusGeneralDisplacement

        backend[PrescribedTemperatureField] = AbaqusPrescribedTemperatureField

        backend[StressFieldResults] = AbaqusStressFieldResults
        backend[DisplacementFieldResults] = AbaqusDisplacementFieldResults
        backend[ReactionFieldResults] = AbaqusReactionFieldResults
        backend[ContactForcesFieldResults] = AbaqusContactFieldResults
        backend[SectionForcesFieldResults] = AbaqusSectionForcesFieldResults
        backend[TemperatureFieldResults] = AbaqusTemperatureFieldResults

        backend[InputFile] = AbaqusInputFile
        backend[ParametersFile] = AbaqusParametersFile

        print("Abaqus implementations registered...")

except:  # noqa: E722
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
