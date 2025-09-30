from compas_fea2.problem.steps import ModalAnalysis
from compas_fea2.problem.steps import BucklingAnalysis
from compas_fea2.problem.steps import ComplexEigenValue
from compas_fea2.problem.steps import LinearStaticPerturbation
from compas_fea2.problem.steps import SteadyStateDynamic
from compas_fea2.problem.steps import SubstructureGeneration

from compas_fea2.units import no_units


@no_units
def _jobdata(obj):
    """Generates the string information for the input file.

    Parameters
    ----------
    obj :

    Returns
    -------
    input file data line (str).
    """
    return """** ----------------------------------------------------------------
**
** STEP: {0}
**
* Step, name={0}, nlgeom={1}, perturbation
*{2}
**\n""".format(
        obj.name, obj.nlgeom, obj.stype
    )


class AbaqusModalAnalysis(ModalAnalysis):
    """"""

    __doc__ += ModalAnalysis.__doc__

    def __init__(self, modes=1, name=None, **kwargs):
        super(AbaqusModalAnalysis, self).__init__(modes, name=name, **kwargs)

    @property
    @no_units
    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
         ----------
         None

         Returns
         -------
         input file data line(str).
        """
        return (
            "** ----------------------------------------------------------------\n"
            "**\n"
            "** STEP: {0}\n"
            "**\n"
            "*Step, name={0}\n"
            "*FREQUENCY, EIGENSOLVER=LANCZOS, NORMALIZATION=DISPLACEMENT\n"
            "{1}\n"
            "*End Step"
        ).format(self.name, self.modes)


class AbaqusComplexEigenValue(ComplexEigenValue):
    def __init__(self, name=None, **kwargs):
        super(AbaqusComplexEigenValue, self).__init__(name, **kwargs)
        raise NotImplementedError


class AbaqusBucklingAnalysis(BucklingAnalysis):
    """Initialises BuckleStep object for use in a buckling analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralStep.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.
    """

    def __init__(self, name=None, **kwargs):
        super(AbaqusBucklingAnalysis, self).__init__(name, **kwargs)
        self._nlgeom = (
            "NO"  # BUG this depends on the previous step -> loop through the steps order and adjust this parameter
        )
        self._stype = "Buckle"

    @property
    @no_units
    def jobdata(self):
        return _jobdata(self)


class AbaqusLinearStaticPerturbation(LinearStaticPerturbation):
    """Initialises the StaticLinearPertubationStep object for use in a static analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralStep.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.

    """

    __doc__ += LinearStaticPerturbation.__doc__

    def __init__(self, name=None, **kwargs):
        super(AbaqusLinearStaticPerturbation, self).__init__(name=name, **kwargs)

        # BUG this depends on the previous step -> loop through the steps order and adjust this parameter

    @property
    @no_units
    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """

        return f"""**
{self._generate_header_section()}
** - Displacements
**   -------------
{self._generate_displacements_section()}
**
** - Loads
**   -----
{self._generate_loads_section()}
**
** - Predefined Fields
**   -----------------
{self._generate_fields_section()}
**
** - Output Requests
**   ---------------
{self._generate_output_section()}
**
*End Step
**"""

    @no_units
    def _generate_header_section(self):
        data_section = []
        line = ("** PERTURBATION STEP: {0}\n" "**\n" "*Step, name={0}, nlgeom={1}, perturbation\n" "*Static").format(
            self.name, "YES" if self.step._nlgeom else "NO"
        )
        data_section.append(line)
        return "".join(data_section)

    @no_units
    def _generate_displacements_section(self):
        return (
            "\n".join(
                [
                    displacement.jobdata(node)
                    for pattern in self.displacements
                    for node, displacement in pattern.node_displacement
                ]
            )
            or "**"
        )

    @no_units
    def _generate_loads_section(self):
        # FIXME Loads are not summed between steps
        return "\n".join([load.jobdata(node) for pattern in self.loads for node, load in pattern.node_load]) or "**"

    @no_units
    def _generate_fields_section(self):
        return (
            "\n".join([load.jobdata(node) for pattern in self.load_fields for node, load in pattern.node_load]) or "**"
        )

    @no_units
    def _generate_output_section(self):
        # TODO check restart option
        data_section = [
            "**",
            "*Restart, write, frequency={}".format(self.restart or 0),
            "**",
        ]
        if self._field_outputs:
            for foutput in self._field_outputs:
                data_section.append(foutput.jobdata())
        if self._history_outputs:
            for houtput in self._history_outputs:
                data_section.append(houtput.jobdata())
        return "\n".join(data_section)


class AbaqusStedyStateDynamic(SteadyStateDynamic):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        raise NotImplementedError


class AbaqusSubstructureGeneration(SubstructureGeneration):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        raise NotImplementedError
