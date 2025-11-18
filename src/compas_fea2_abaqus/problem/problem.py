import os
from pathlib import Path
from compas_fea2.problem import Problem

from compas_fea2.utilities._devtools import timer
from compas_fea2.utilities._devtools import launch_process

from ..results import results_to_sql
from ..job.input_file import _AbaqusRestartInputFile
import compas_fea2_abaqus

from compas_fea2.units import no_units


class AbaqusProblem(Problem):
    """Abaqus implementation of :class:`Problem`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += Problem.__doc__ or ""

    def __init__(self, name=None, description=None, **kwargs):
        super(AbaqusProblem, self).__init__(name=name, description=description, **kwargs)

    # =========================================================================
    #                         Analysis methods
    # =========================================================================
    def _build_command(self, path: str, name: str, **kwargs):
        # Set solver path
        exe_cmd = os.path.join(kwargs.get("exe", None) or "C:/SIMULIA/Commands", "abaqus")
        # Set options
        option_keywords = []
        if kwargs.get("overwrite", None):
            option_keywords.append("ask_delete=OFF")
        if umat := kwargs.get("user_mat", None):
            option_keywords.append(f"user={umat.path}")
        if oldjob := kwargs.get("oldjob", None):
            option_keywords.append(f"oldjob={oldjob}")
        if cpus := kwargs.get("cpus", None):
            option_keywords.append(f"cpus={cpus}")
        option_keywords = " ".join(option_keywords)

        return f"cd {path} && {exe_cmd} job={name} interactive resultsformat=odb {option_keywords}"

    def write_restart_file(self, path: str, start: str, steps):
        """Writes the abaqus input file.

        Parameters
        ----------
        path : :class:`pathlib.Path`
            Path to the folder where the input file is saved. In case the folder
            does not exist, one is created.
        restart : dict
            parameters for the restart option

        Returns
        -------
        None
        """
        if not path.exists():
            raise ValueError("No analysis results found for {!r}".format(self))
        restart_file = _AbaqusRestartInputFile.from_problem(problem=self, start=start, steps=steps)
        restart_file.write_to_file(self.path)
        return restart_file

    def analyse(
        self,
        path,
        exe=None,
        cpus=1,
        verbose=False,
        overwrite=True,
        user_mat=None,
        *args,
        **kwargs,
    ):
        """Runs the analysis through abaqus.

        Parameters
        ----------
        path : str, :class:`pathlib.Path`
            Path to the analysis folder. A new folder with the name
            of the problem will be created at this location for all the required
            analysis files.
        save : bool
            Save structure to .cfp before the analysis.
        exe : str, optional
            Full terminal command to bypass subprocess defaults, by default ``None``.
        cpus : int, optional
            Number of CPU cores to use, by default ``1``.
        output : bool, optional
            Print terminal output, by default ``True``.
        overwrite : bool, optional
            Overwrite existing analysis files, by default ``True``.
        restart : bool, optional
            If `True`, save additional files for restarting the analysis later,
            by default `False`

        Returns
        -------
        None

        """
        print("\nBegin the analysis...")
        self._check_analysis_path(path, kwargs.get("erase_data", False))
        self.write_input_file()
        cmd = self._build_command(
            overwrite=overwrite,
            user_mat=user_mat,
            exe=exe,
            path=self.path,
            name=self.name,
            cpus=cpus,
        )
        for line in launch_process(cmd_args=cmd, cwd=self.path, verbose=verbose):
            print(line)

    def restart_analysis(self, start, steps, exe=None, cpus=1, output=True, overwrite=True):
        """Runs the analysis through abaqus.

        Parameters
        ----------
        start : float
            Time-step increment.
        steps : [:class:`compas_fea2.problem.Step`]
            List of steps to add to the orignal problem.
        exe : str, optional
            Full terminal command to bypass subprocess defaults, by default ``None``.
        cpus : int, optional
            Number of CPU cores to use, by default ``1``.
        output : bool, optional
            Print terminal output, by default ``True``.
        overwrite : bool, optional
            Overwrite existing analysis files, by default ``True``.

        Returns
        -------
        None

        """
        if not self.path:
            raise AttributeError("No analysis path found! Are you sure you analysed this problem?")
        restart_file = self.write_restart_file(path=self.path, start=start, steps=steps)
        cmd = self._build_command(
            overwrite=overwrite,
            user_mat=None,
            exe=exe,
            path=self.path,
            name=restart_file._job_name,
            cpus=cpus,
            oldjob=self.name,
        )
        print("\n\n*** RESTARTING PREVIOUS JOB ***\n")
        for line in launch_process(cmd_args=cmd, cwd=self.path, verbose=output):
            print(line)

    def analyse_and_extract(
        self,
        path,
        exe=None,
        cpus=1,
        verbose=False,
        overwrite=True,
        user_mat=None,
        fields=None,
        *args,
        **kwargs,
    ):
        """_summary_

        Parameters
        ----------
        path : _type_
            _description_
        exe : _type_, optional
            _description_, by default None
        cpus : int, optional
            _description_, by default 1
        output : bool, optional
            _description_, by default True
        overwrite : bool, optional
            _description_, by default True
        user_mat : _type_, optional
            _description_, by default None
        database_path : _type_, optional
            _description_, by default None
        database_name : _type_, optional
            _description_, by default None
        fields : [str], optional
            Output fields to extract from the odb file, by default None, which
            means that all available fields are extracted.

        Returns
        -------
        _type_
            _description_
        """
        self.analyse(
            path,
            exe=exe,
            cpus=cpus,
            verbose=True,
            overwrite=overwrite,
            user_mat=user_mat,
            *args,
            **kwargs,
        )
        return self.extract_results(fields=fields)

    # ==========================================================================
    # Extract results
    # ==========================================================================
    @timer(message="Data extracted from Abaqus .odb file in")
    def extract_results(self, database_path=None, database_name=None, fields=None, **kwargs):
        """Extract data from the Abaqus .odb file and store into a SQLite database.

        Parameters
        ----------
        fields : list
            Output fields to extract, by default 'None'. If `None` all available
            fields will be extracted, which might require considerable time.

        Returns
        -------
        None

        """
        print("\nExtracting data from Abaqus .odb file...")
        database_path = database_path or self.path
        database_name = database_name or self.name
        if not fields:
            fields = self.steps[-1].field_outputs
        field_input = '.'.join([field.field_name+"/"+','.join(field.abaqus_field_names) # compas_field_name/abaqus_fields_names
                                +'-'
                                +",".join([abaq_comp+'/'+compas_comp for compas_comp,abaq_comp in field.compas_to_abaqus_component_names.items()# abaqus_component/compas_component
                                           ]) 
                                for field in fields])
        args = [
            os.path.join(kwargs.get("exe", None) or "C:/SIMULIA/Commands", "abaqus"),
            "python",
            Path(results_to_sql.__file__),
            field_input,
            database_path,
            database_name,
        ]
        for line in launch_process(cmd_args=args, cwd=database_path, verbose=True):
            print(line)

        return [Path(database_path).joinpath(f"{database_name}-results.db")]

    # =============================================================================
    #                               Job data
    # =============================================================================

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
        return "\n".join([step.jobdata for step in self.steps])
