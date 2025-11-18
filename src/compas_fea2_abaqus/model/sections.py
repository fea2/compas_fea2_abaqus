from compas_fea2.model.sections import SpringSection
from compas_fea2.model.sections import ConnectorSection
from compas_fea2.model.sections import GenericBeamSection
from compas_fea2.model.sections import AngleSection
from compas_fea2.model.sections import BoxSection
from compas_fea2.model.sections import HexSection
from compas_fea2.model.sections import ISection
from compas_fea2.model.sections import CircularSection
from compas_fea2.model.sections import RectangularSection
from compas_fea2.model.sections import ShellSection
from compas_fea2.model.sections import MembraneSection
from compas_fea2.model.sections import SolidSection
from compas_fea2.model.sections import TrussSection
from compas_fea2.model.sections import TrapezoidalSection
from compas_fea2.model.sections import StrutSection
from compas_fea2.model.sections import TieSection
from compas_fea2.model.sections import PipeSection
from compas_fea2.units import _strip_magnitudes

from compas_fea2.units import no_units, units_io

# NOTE: these classes are sometimes overwriting the _base ones because Abaqus offers internal ways of computing beam sections' properties


@no_units
def _generate_beams_jobdata(obj, set_name, orientation, stype):
    """Generates the common string information for the input file of all the
    abaqus predefined beam sections.

    Parameters
    ----------
    obj : :class:`compas_fea2.model.sections.GenericBeamSection`
        Section to write in the input file.
    set_name : str
        Name of the element set to which the section is assigned.
    orientation : str
        Section orientation information.
    stype : str
        Abaqus identifier for the section. This is used to automatically generate
        the sectional properties.

    Returns
    -------
    input file data line (str).
    """
    orientation_line = ", ".join([str(v) for v in orientation])
    return """** Section: {}
*Beam Section, elset={}, material={}, section={}
{}
{}""".format(
        obj.name,
        set_name,
        obj.material.name,
        stype,
        ", ".join([str(_strip_magnitudes(v)) for v in obj._properties]),
        orientation_line,
    )


# ==============================================================================
# 0D
# ==============================================================================
# class AbaqusMassSection(MassSection):
#     """Abaqus implementation of the :class:`MassSection`.\n"""

#     __doc__ = __doc__ or ""
#     __doc__ += MassSection.__doc__ or ""

#     def __init__(self, mass, name=None, **kwargs):
#         super(AbaqusMassSection, self).__init__(mass, name=name, **kwargs)

#     @no_units
#     def jobdata(self, set_name):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).
#         """
#         return """** Section: \"{}\"
# *Mass, elset={}
# {}\n""".format(
#             self.name, set_name, self.mass
#         )


class AbaqusSpringSection(SpringSection):
    """Abaqus implementation of the :class:`SpringSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += SpringSection.__doc__ or ""
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, axial, lateral, rotational, **kwargs):
        super(AbaqusSpringSection, self).__init__(axial, lateral, rotational, **kwargs)

    @no_units
    def jobdata(self, elset):
        return f"*Spring, elset=Springs/Dashpots-{elset}\n{3}\n{self.axial}"


class AbaqusConnectorSection(ConnectorSection):
    """Abaqus implementation of the :class:`ConnectorSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += ConnectorSection.__doc__ or ""
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(
        self,
        axial: float = None,
        lateral: float = None,
        rotational: float = None,
        **kwargs,
    ):
        super(AbaqusConnectorSection, self).__init__(axial=axial, lateral=lateral, rotational=rotational, **kwargs)

    @property
    @no_units
    def jobdata(self):
        # FIXME: this is a placeholder only working for axial connectors
        data = [f"*Connector Behavior, name={self.name}"]
        data += ["*Connector Elasticity, component=1"]
        data += [f"{self.axial},"]
        return "\n".join(data)


# ==============================================================================
# 1D
# ==============================================================================


class AbaqusGenericBeamSection(GenericBeamSection):
    """Abaqus implementation of the :class:`GenericBeamSection`.\n"""

    __doc__ += GenericBeamSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, *, A, Ixx, Iyy, Ixy, Avx, Avy, J, g0, gw, material, name=None, **kwargs):
        super().__init__(
            A=A,
            Ixx=Ixx,
            Iyy=Iyy,
            Ixy=Ixy,
            Avx=Avx,
            Avy=Avy,
            J=J,
            g0=g0,
            gw=gw,
            material=material,
            name=name,
            **kwargs,
        )
        raise NotImplementedError("{self.__class__.__name__} is not available in Abaqus")


class AbaqusAngleSection(AngleSection):
    """Abaqus implementation of the :class:`AngleSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += AngleSection.__doc__ or ""
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    @units_io(types_in=("length", "length", "length"), types_out=None)
    def __init__(self, w, h, t, material, name=None, **kwargs):
        super(AbaqusAngleSection, self).__init__(w, h, t, material, name=name, **kwargs)
        if not isinstance(t, list):
            t = [t] * 2
        self._properties = [w, h, *t]

    @no_units
    def jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, "L")


class AbaqusBoxSection(BoxSection):
    """Abaqus implementation of the :class:`BoxSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += BoxSection.__doc__ or ""
    __doc__ += """Box section.

    Note
    ----
    This is temporarily inconsistent with the base class. WIP

    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    @units_io(types_in=("length", "length", "length", "length", "length"), types_out=None)
    def __init__(self, w, h, tw, tf, r, material, **kwargs):
        super(AbaqusBoxSection, self).__init__(w=w, h=h, tw=tw, tf=tf, r=r, material=material, **kwargs)
        if not isinstance(tw, list):
            tw = [tw] * 4
        self._properties = [w, h, *tw]

    @no_units
    def jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, "box")


class AbaqusCircularSection(CircularSection):
    """Abaqus implementation of the :class:`CircularSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += CircularSection.__doc__ or ""
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    @units_io(types_in=("length"), types_out=None)
    def __init__(self, r, material, name=None, **kwargs):
        super(AbaqusCircularSection, self).__init__(r, material, name=name, **kwargs)
        self._properties = [r]

    @no_units
    def jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, "circ")


class AbaqusHexSection(HexSection):
    """Abaqus implementation of the :class:`HexSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += HexSection.__doc__ or ""
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    @units_io(types_in=("length", "length"), types_out=None)
    def __init__(self, r, t, material, name=None, **kwargs):
        super(AbaqusHexSection, self).__init__(r, t, material, name=name, **kwargs)
        self._stype = "hex"
        self.properties = [r, t]


class AbaqusISection(ISection):
    """Abaqus implementation of the :class:`ISection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += ISection.__doc__ or ""
    __doc__ += """I or T section.

    Note
    ----
    This is temporarily inconsistent with the base class. WIP

    Note
    ----
    Set b1 and t1 or b2 and t2 to zero to model a T-section

    Note
    ----
    The section properties are automatically computed by Abaqus.
    """

    @units_io(types_in=("length", "length", "length", "length"), types_out=None)
    def __init__(self, w, h, ttf, tbf, material, l=None, name=None, **kwargs):  # noqa: E741
        super(AbaqusISection, self).__init__(w=w, h=h, ttf=ttf, tbf=tbf, material=material, name=name, **kwargs)
        self._stype = "I"
        t = ttf
        if not isinstance(w, list):
            w = [w] * 2
        if not isinstance(h, list):
            t = [t] * 3
        if not l:
            h_crosscenter = h / 2
        self._properties = [h_crosscenter, h, *w, *t]

    def jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, "I")


class AbaqusPipeSection(PipeSection):
    """Abaqus implementation of the :class:`PipeSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += PipeSection.__doc__ or ""
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    @units_io(types_in=("length", "length"), types_out=None)
    def __init__(self, r, t, material, name=None, **kwarg):
        super(AbaqusPipeSection, self).__init__(r, t, material, name=name, **kwarg)
        self._stype = "pipe"
        self.properties = [r, t]


class AbaqusRectangularSection(RectangularSection):
    """Abaqus implementation of the :class:`RectangularSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += RectangularSection.__doc__ or ""
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    @units_io(types_in=("length", "length"), types_out=None)
    def __init__(self, w, h, material, name=None, **kwargs):
        super(AbaqusRectangularSection, self).__init__(w=w, h=h, material=material, name=name, **kwargs)
        self._properties = [w, h]

    @no_units
    def jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, "rect")


class AbaqusTrapezoidalSection(TrapezoidalSection):
    """Abaqus implementation of the :class:`TrapezoidalSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += TrapezoidalSection.__doc__ or ""
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    @units_io(types_in=("length", "length", "length"), types_out=None)
    def __init__(self, w1, w2, h, material, name=None, **kwargs):
        super(AbaqusTrapezoidalSection, self).__init__(w1, w2, h, material, name=name, **kwargs)
        raise NotImplementedError("{self.__class__.__name__} is not available in Abaqus")


# TODO -> check how these sections are implemented in ABAQUS
class AbaqusTrussSection(TrussSection):
    """Abaqus implementation of the :class:`TrussSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += TrussSection.__doc__ or ""
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    @units_io(types_in=("area"), types_out=None)
    def __init__(self, A, material, name=None, **kwargs):
        super(AbaqusTrussSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError("{self.__class__.__name__} is not available in Abaqus")


class AbaqusStrutSection(StrutSection):
    """Abaqus implementation of the :class:`StrutSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += StrutSection.__doc__ or ""
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    @units_io(types_in=("area"), types_out=None)
    def __init__(self, A, material, name=None, **kwargs):
        super(AbaqusStrutSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError("{self.__class__.__name__} is not available in Abaqus")


class AbaqusTieSection(TieSection):
    """Abaqus implementation of the :class:`TieSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += TieSection.__doc__ or ""
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    @units_io(types_in=("area"), types_out=None)
    def __init__(self, A, material, name=None, **kwargs):
        super(AbaqusTieSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError("{} is not available in Abaqus".format(TieSection.__name__))


# ==============================================================================
# 2D
# ==============================================================================


class AbaqusShellSection(ShellSection):
    """Abaqus implementation of the :class:`ShellSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += ShellSection.__doc__ or ""
    __doc__ += """
    Additional Parameters
    ---------------------
    int_points : int
        number of integration points. 5 by default.
    """

    @units_io(types_in=("length",), types_out=None)
    def __init__(self, t, material, int_points=5, name=None, **kwargs):
        super(AbaqusShellSection, self).__init__(t, material, name=name, **kwargs)
        self.int_points = int_points

    @no_units
    def jobdata(self, set_name, orientation):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        jobdata = []
        if orientation:
            jobdata.append(f"*Orientation, name=Ori_{self.material.name}")
            # In Abaqus, the *Orientation option define a local (x, y, z) frame of the section
            # Then, the orthonormal local frame (1,2,3) of the element is defined such as :
            # the normal is parallel to z-axis and has the same direction
            # Direction 1 is parallel to x and direction 2 parallel to y
            # The frame defined in compas_fea2 corresponds directly to the local (1,2,3) frame
            # This is why below the input for *Orientation is adapted.
            jobdata.append(
                orientation[3]
                + ", "
                + orientation[4]
                + ", "
                + orientation[5]
                + ", "
                + str(-float(orientation[0]))
                + ", "
                + str(-float(orientation[1]))
                + ", "
                + str(-float(orientation[2]))
            )
        jobdata.append(f"** Section: {self.name}")
        if "C2D" in set_name.split("_")[1]:
            jobdata.append(f"*Solid Section, elset={set_name}, material={self.material.name}")
            return "\n".join(jobdata)
        else:
            jobdata.append(f"*Shell Section, elset={set_name}, material={self.material.name}")
        if orientation:
            jobdata[-1] += f", orientation=Ori_{self.material.name}"
        jobdata.append(f"{self.t}, {self.int_points}")
        return "\n".join(jobdata)


class AbaqusMembraneSection(MembraneSection):
    """Abaqus implementation of the :class:`MembraneSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += MembraneSection.__doc__ or ""

    def __init__(self, t, material, name=None, **kwargs):
        super(AbaqusMembraneSection, self).__init__(t, material, name=name, **kwargs)

    @no_units
    def jobdata(self, set_name, **kwargs):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return """** Section: {}
*Membrane Section, elset={}, material={}
{},""".format(
            self.name, set_name, self.material.name, self.t
        )


# ==============================================================================
# 3D
# ==============================================================================


class AbaqusSolidSection(SolidSection):
    """Abaqus implementation of the :class:`SolidSection`.\n"""

    __doc__ = __doc__ or ""
    __doc__ += SolidSection.__doc__ or ""

    def __init__(self, material, **kwargs):
        super(AbaqusSolidSection, self).__init__(material, **kwargs)

    @no_units
    def jobdata(self, set_name, **kwargs):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """

        return f"""** Section: {self.name}
*Solid Section, elset={set_name}, material={self.material.name}"""
