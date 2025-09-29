from datetime import datetime
import compas_fea2
import compas_fea2_abaqus
from compas_fea2.job import InputFile
from compas_fea2.job.input_file import ParametersFile

from compas_fea2.units import no_units


class AbaqusInputFile(InputFile):
    """"""

    def __init__(self, problem, **kwargs):
        super(AbaqusInputFile, self).__init__(problem=problem, **kwargs)
        self._extension = "inp"

    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    @property
    @no_units
    def jobdata(self):
        """Generate the content of the input file from the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Resturn
        -------
        str
            content of the input file
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"""*Heading
** Job name: {self.problem.name}
** Generated using:
**      compas_fea2 version {compas_fea2.__version__}
**      compas_fea2_abaqus version {compas_fea2_abaqus.__version__}
** Author: {self.model.author}
** Date: {now}
** Model Description : {self.model.description}
** Problem Description : {self.problem.description}
**
*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMANN=5.67e-8
**
**------------------------------------------------------------------
**------------------------------------------------------------------
** MODEL
**------------------------------------------------------------------
**------------------------------------------------------------------
**
{self.model.jobdata}**
**------------------------------------------------------------------
**------------------------------------------------------------------
** PROBLEM
**------------------------------------------------------------------
**------------------------------------------------------------------
{self.problem.jobdata}"""


class _AbaqusRestartInputFile(InputFile):
    """"""

    def __init__(self, start, steps, name=None, **kwargs):
        super(_AbaqusRestartInputFile, self).__init__(name=name, **kwargs)
        self._extension = "inp"
        self._start = start
        self._steps = steps

    @property
    def start(self):
        return self._start

    @property
    def steps(self):
        return self._steps

    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    @classmethod
    def from_problem(cls, problem, start, steps):
        """Create an AbaqusRestartInputFile object from a :class:`compas_fea2.problem.Problem`,
        a starting increment and and additional steps

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            Problem to be converted to InputFile.

        Returns
        -------
        obj
            InputFile for the analysis.
        """
        restart_file = cls(start=start, steps=steps)
        restart_file._registration = problem
        restart_file._job_name = problem.name + "_restart"
        restart_file._file_name = "{}.{}".format(restart_file._job_name, restart_file._extension)

        return restart_file

    @property
    @no_units
    def jobdata(self):
        """Generate the content of the input file from the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Resturn
        -------
        str
            content of the input file
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return """*Heading
** Job name: {}
** Generated using compas_fea2 version {}
** Author: {}
** Date: {}
** Model Description : {}
** Problem Description : {}
**
*Restart, read, step={}
**
**------------------------------------------------------------------
**------------------------------------------------------------------
** ADDITIONAL STEPS
**------------------------------------------------------------------
**------------------------------------------------------------------
{}""".format(
            self._job_name,
            compas_fea2.__version__,
            self.model.author,
            now,
            self.model.description,
            self.problem.description,
            self.start,
            "\n".join([step.jobdata() for step in self.steps]),
        )


class AbaqusParametersFile(ParametersFile):
    """"""

    def __init__(self, name=None, **kwargs):
        super(AbaqusParametersFile, self).__init__(name, **kwargs)
        self._extension = "par"

    @classmethod
    def from_problem(cls, problem, smooth):
        """[summary]

        Parameters
        ----------
        problem : obj
            :class:`compas_fea2.problem.Problem` sub class object.
        smooth : obj, optional
            if a :class:`compas_fea2.optimisation.SmoothingParameters` subclass object is passed, the
            optimisation results will be postprocessed and smoothed, by defaut
            ``None`` (no smoothing)

        Returns
        -------
        obj
            InputFile for the analysis.
        """
        input_file = cls()
        input_file._job_name = problem._name
        input_file._file_name = "{}.{}".format(problem._name, input_file._extension)
        input_file._job_data = input_file.jobdata(problem, smooth)
        input_file._registration = problem
        return input_file

    @no_units
    def jobdata(self, opti_problem, smooth):
        """Generate the content of the parameter file from the optimisation
        settings of the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Resturn
        -------
        str
            content of the .par file
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"""! Optimization Process name: {self._job_name}
! Model name: {opti_problem._problem.model.name}
! Task name: TopOpt
! Generated using compas_fea2 version {compas_fea2.__version__}
! Author: {opti_problem._problem.author}
! Date: {now}
!
! ----------------------------------------------------------------
! Input model
!
FEM_INPUT
  ID_NAME        = OPTIMIZATION_MODEL
  FILE           = {opti_problem._problem._name}.inp
END_
!
! ----------------------------------------------------------------
! Design area
{opti_problem._design_variables.jobdata()}!
! ----------------------------------------------------------------
! Design responses
{"".join([value.jobdata() for value in opti_problem._design_responses.values()])}!
! ----------------------------------------------------------------
! Objective Function
{opti_problem._objective_function.jobdata()}!
! ----------------------------------------------------------------
! Constraints
{"".join([value.jobdata() for value in opti_problem._constraints.values()])}!
! ----------------------------------------------------------------
! Task
{opti_problem.jobdata()}!
! ----------------------------------------------------------------
! Parameters
{opti_problem._parameters.jobdata(opti_problem._name)}!
!
! ----------------------------------------------------------------
!
{smooth.jobdata() if smooth else "!"}
EXIT"""
