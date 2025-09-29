from compas_fea2.problem.fields import ForceField
from compas_fea2.problem.fields import GravityLoadField
from compas_fea2.problem.fields import TemperatureField

from compas_fea2.units import no_units


dofs = ["x", "y", "z", "xx", "yy", "zz"]

class AbaqusTemperatureField(TemperatureField):
    """Calculix implementation of :class:`PrescribedTemperatureField`.\n"""

    __doc__ = (__doc__ or "") + (TemperatureField.__doc__ or "")

    def __init__(self, temperature, distribution, load_case, combination_rank=1, **kwargs):
        super().__init__(temperature, distribution, load_case, combination_rank=combination_rank, **kwargs)

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
        raise NotImplementedError("Abaqus TemperatureField jobdata not implemented yet.")


class AbaqusForceField(ForceField):
    """Calculix implementation of :class:`ForceField`.\n"""

    __doc__ = (__doc__ or "") + (ForceField.__doc__ or "")

    def __init__(self, loads, distribution, load_case, combination_rank=1, modify=False, follow=False, **kwargs):
        super().__init__(loads=loads, distribution=distribution, load_case=load_case, combination_rank=combination_rank, **kwargs)
        self._modify = ", OP={}".format(modify) if modify else ", OP=MOD"  # In abaqus the default is MOD
        self._follow = ", follower" if follow else ""  
        
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

        data_section = [
            "** Name: {} Type: Concentrated Force".format(self.name),
            "*Cload{}{}".format(self._modify, self._follow),
        ]

        for node, load in self.node_load:
            for comp, dof in enumerate(dofs, 1):
                if getattr(load, dof):
                    data_section.append(f"{node.part.name}-1.{node.key}, {comp}, {getattr(load, dof)}")
        return "\n".join(data_section) or "**"

class AbaqusGravityLoadField(GravityLoadField):
    """Calculix implementation of :class:`GravityLoadField`.\n"""

    __doc__ = (__doc__ or "") + (GravityLoadField.__doc__ or "")

    def __init__(self,g=9.81, direction=(0, 0, -1), distribution=None, load_case=None, combination_rank=1, **kwargs):
        super().__init__(g=g, direction=direction, distribution=distribution, load_case=load_case, combination_rank=combination_rank, **kwargs)
        
        
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
        return (f"** Name: {self.name} Type: Gravity\n" "*Dload\n" f", GRAV, {self.g}, {self.direction[0]}, {self.direction[1]}, {self.direction[2]}")