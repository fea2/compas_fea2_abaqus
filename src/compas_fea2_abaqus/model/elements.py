from compas_fea2.model import MassElement
from compas_fea2.model import BeamElement
from compas_fea2.model import TrussElement
from compas_fea2.model import ShellElement
from compas_fea2.model import MembraneElement
from compas_fea2.model import _Element3D
from compas_fea2.model import TetrahedronElement
from compas_fea2.model import HexahedronElement
from compas_fea2.model import LinkElement

from compas_fea2.units import no_units


@no_units
def _jobdata(element):
    """Generates the common string information for the input file of all the
    elements.

    Note
    ----
    the string portion `*Element, type=___` is generated in the part section
    to group elements with the same type.

    Parameters
    ----------
    None

    Returns
    -------
    input file data line (str).

    """
    return "{0}, {1}".format(element.key, ", ".join(str(node.key) for node in element.nodes))


# ==============================================================================
# 0D elements
# ==============================================================================
class AbaqusMassElement(MassElement):
    """Abaqus implementation of :class:`MassElement`\n"""

    __doc__ = __doc__ or ""
    __doc__ += MassElement.__doc__ or ""

    def __init__(self, *, node, section, name=None, **kwargs):
        super(AbaqusMassElement, self).__init__(nodes=[node], section=section, name=name, **kwargs)

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
        return f"""
*ELEMENT, TYPE=MASS, ELSET={self.elset}
{self.elset}, {self.node}
*MASS, ELSET={self.elset}
{self.node}
"""


class AbaqusLinkElement(LinkElement):
    """Abaqus implementation of :class:`LinkElement`\n"""

    __doc__ = __doc__ or ""
    __doc__ += LinkElement.__doc__ or ""

    def __init__(self, nodes, section, name=None, **kwargs):
        super(AbaqusLinkElement, self).__init__(nodes=nodes, section=section, name=name, **kwargs)
        raise NotImplementedError()


# ==============================================================================
# 1D elements
# ==============================================================================


class AbaqusBeamElement(BeamElement):
    """Abaqus implementation of :class:`BeamElement`.

    Note
    ----
    For more information check here:

        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-c-beamelem.htm?contextscope=cloud&id=b7b26e5cc0cd473fab5848eb786599ae
        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-r-beamlibrary.htm?contextscope=cloud&id=7b2be9375d9744a58ad0c44fd2729028


    """

    __doc__ = __doc__ or ""
    __doc__ += BeamElement.__doc__ or ""
    __doc__ += """
    Additional Parameters
    ---------------------
    type : str, optional
        Name of the implementation model.
    iterpolation : int, optional
        Number of interpolation points, from 1 to 3, by default 1.
    hybrid : bool, optional
        Use hybrid formulation, by default `False`. [WIP]
    implementation : str, optional
        Name of the implementation model to be used, by default `None`. This can
        be used alternatively to the `type`, `interpolation` and `hybrid` parameters
        to directly define the model to be used. If both are specified, the
        `implementation` overwrites the others.

    Note
    ----
    Only 3d elements are implemented.
    The available implementations are listed below

        - B3
        - PIPE3

    Warning
    -------
    The `Open Section(OS)` formulation is currently under development.

    """

    def __init__(
        self,
        nodes,
        section,
        type="B3",
        interpolation=1,
        hybrid=None,
        implementation=None,
        name=None,
        **kwargs,
    ):
        super(AbaqusBeamElement, self).__init__(
            nodes=nodes,
            section=section,
            implementation=implementation or "".join([type, str(interpolation), "H" if hybrid else ""]),
            name=name,
            **kwargs,
        )
        self._type = type
        self._interpolation = interpolation
        self._hybrid = hybrid
        self._elset = None

    @property
    @no_units
    def jobdata(self):
        if any(x in self.implementation for x in ["B3", "PIPE"]):
            return _jobdata(self)
        else:
            raise NotImplementedError


class AbaqusTrussElement(TrussElement):
    """Abaqus implementation of :class:`TrussElement`\n"""

    __doc__ = __doc__ or ""
    __doc__ += TrussElement.__doc__ or ""

    def __init__(self, nodes, section, type="T3D", name=None, **kwargs):
        super(AbaqusTrussElement, self).__init__(
            nodes=nodes,
            section=section,
            implementation="".join(
                [
                    type,
                    str(len(nodes)),
                ]
            ),
            name=name,
            **kwargs,
        )
        self._elset = None
        self._orientation = None
        self._type = type
        if len(nodes) not in [2, 3]:
            raise ValueError("A truss element with {} nodes cannot be created".format(len(nodes)))

    @property
    @no_units
    def jobdata(self):
        return getattr(self, "_" + self._type.lower())()

    def _t3d(self):
        return _jobdata(self)


# ==============================================================================
# 2D elements
# ==============================================================================


class AbaqusShellElement(ShellElement):
    """Abaqus implementation of :class:`ShellElement`.

    Note
    ----
    For more information check here:

        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-c-shellelem.htm?contextscope=cloud#simaelm-c-shellelem-t-namingconven1


    """

    __doc__ = __doc__ or ""
    __doc__ += ShellElement.__doc__ or ""
    __doc__ += """
    Additional Parameters
    ---------------------
    implementation : str, optional
        Name of the implementation model to be used, by default `None`. This can
        be used alternatively to the `type`, `reduced`, `optional` and `warping parameters
        to directly define the model to be used. If both are specified, the
        `implementation` overwrites the others.
    reduced : bool, optional
        Reduce the integration points, by default ``False``.
    optional : str, optional
        String with additional optional parameters, by default `None`.
    warping : str, optional
        Include warping effects, by default `False`.


    Note
    ----
    Only 3d elements are implemented.
    The available implementations are listed below

        - S
        - R3D

    Warning
    -------
    The `Open Section(OS)` formulation is currently under development.
    """

    def __init__(
        self,
        nodes,
        section,
        heat=None,
        implementation="S",
        reduced=False,
        optional=None,
        warping=False,
        rigid=False,
        name=None,
        **kwargs,
    ):
        implementation = "".join(
            [
                "D" if heat else "",
                implementation or "S" if not rigid else "R3D",
                str(len(nodes)),
                "R" if reduced else "",
                optional or "",
                "W" if warping else "",
            ]
        )
        super(AbaqusShellElement, self).__init__(
            nodes=nodes,
            section=section,
            implementation=implementation,
            rigid=rigid,
            name=name,
            **kwargs,
        )
        self._elset = None
        self._reduced = reduced
        self._optional = optional
        self._warping = warping

    @property
    @no_units
    def jobdata(self):
        return getattr(self, "_" + self._implementation.lower())()

    @no_units
    def _s3(self):
        return _jobdata(self)

    @no_units
    def _dc2d4(self):
        return _jobdata(self)

    @no_units
    def _dc2d3(self):
        return _jobdata(self)

    def _s4(self):
        return _jobdata(self)

    @no_units
    def _sc(self):
        raise NotImplementedError()

    @no_units
    def _r3d4(self):
        return _jobdata(self)

    @no_units
    def _r3d3(self):
        return _jobdata(self)


class AbaqusMembraneElement(MembraneElement):
    """Abaqus implementation of :class:`MembraneElement`.

    Note
    ----
    Only general 3d membran elements are implemented.
    For more information check here:

        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-c-membrane.htm?contextscope=cloud&id=bf007ad805834a7c952e935c80f8746a
        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-r-membranelibrary.htm?contextscope=cloud&id=2e94e8c91da249a0bdf25601839722ed

    """

    __doc__ = __doc__ or ""
    __doc__ += MembraneElement.__doc__ or ""
    __doc__ += """
    Additional Parameters
    ---------------------
    type : str, optional
        Name of the implementation model.
    reduced : bool, optional
        Reduce the integration points, by default ``False``.
    implementation : str, optional
        Name of the implementation model to be used, by default `None`. This can
        be used alternatively to the `type` and `reduced` parameters
        to directly define the model to be used. If both are specified, the
        `implementation` overwrites the others.
    """

    def __init__(
        self,
        nodes,
        section,
        frame=None,
        type="M3D",
        reduced=False,
        implementation=None,
        name=None,
        **kwargs,
    ):
        super(AbaqusMembraneElement, self).__init__(
            nodes=nodes,
            section=section,
            frame=frame,
            implementation=implementation
            or "".join(
                [
                    type,
                    str(len(nodes)),
                    "R" if reduced and len(nodes) > 3 else "",
                ]
            ),
            name=name,
            **kwargs,
        )
        self._type = type.upper()
        self._reduced = reduced
        self._elset = None
        if len(self._nodes) not in (3, 4, 6, 8, 9):
            raise ValueError("A membrane element with {} nodes cannot be created.".format(len(nodes)))

    @property
    @no_units
    def jobdata(self):
        if self._type != "M3D":
            raise ValueError("{} is not a valid implementation model.".format(self._type))
        return _jobdata(self)


# ==============================================================================
# 3D elements
# ==============================================================================


class _AbaqusElement3D(_Element3D):
    """Abaqus implementation of :class:`_Element3D`

    Note
    ----
    Only general 3d elements are implemented.
    For more information check here:

        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-c-solidcont.htm?contextscope=cloud&id=4ca54694ed664f459b7603ca652f5b7a
        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-r-3delem.htm?contextscope=cloud&id=ef2239f0cc404c199127f51c39a2834f

    """

    __doc__ = __doc__ or ""
    __doc__ += _Element3D.__doc__ or ""
    __doc__ += """
    Additional Parameters
    ---------------------
    reduced : bool, optional
        Reduce the integration points, by default ``False``.
    hybrid : bool, optional
        Use hybrid formulation, by default ``False``.
    optional : str, optional
        String with additional optional parameters, by default `None`.
    implementation : str, optional
        Name of the implementation model to be used, by default `None`. This can
        be used alternatively to the `type`, `reduced`, `optional` and `warping parameters
        to directly define the model to be used. If both are specified, the
        `implementation` overwrites the others.

    """

    def __init__(
        self,
        nodes,
        section=None,
        heat=None,
        type="C3D",
        reduced=False,
        hybrid=False,
        optional=None,
        implementation=None,
        name=None,
        **kwargs,
    ):
        super(_AbaqusElement3D, self).__init__(
            nodes=nodes,
            section=section,
            implementation=implementation
            or "".join(
                [
                    "D" if heat else "",
                    type,
                    str(len(nodes)),
                    "R" if reduced else "",
                    "H" if hybrid else "",
                    optional or "",
                ]
            ),
            name=name,
            **kwargs,
        )
        self._type = type.upper()
        self._reduced = reduced
        self._hybrid = hybrid
        self._optional = optional
        if len(self._nodes) not in (4, 5, 6, 8, 10, 15, 20):
            raise ValueError("A solid element with {} nodes cannot be created.".format(len(nodes)))

    @property
    @no_units
    def jobdata(self):
        try:
            return getattr(self, "_" + self.implementation[:4])()
        except:  # noqa: E722
            raise ValueError("{} is not a valid implementation.".format(self._implementation))

    # def _c3d8(self):
    #     """A Solid cuboid element with 6 faces (extruded rectangle).

    #     Note
    #     ----
    #     The face labels are as follows:
    #         - S1: (0, 1, 2)
    #         - S2: (0, 1, 3)
    #         - S3: (1, 2, 3)
    #         - S4: (0, 2, 3)
    #     where the number is the index of the the node in the nodes list
    #     """
    #     self._faces_indices = {'s1': (0, 1, 2, 3),
    #                            's2': (4, 5, 6, 7),
    #                            's3': (0, 1, 4, 5),
    #                            's4': (1, 2, 5, 6),
    #                            's5': (2, 3, 6, 7),
    #                            's6': (0, 3, 4, 7)
    #                            }
    #     self._faces = self._construct_faces(self._face_indices)
    #     return jobdata(self)

    # def _css(self):
    #     raise NotImplementedError

    # def _q3d(self):
    #     raise NotImplementedError

    # def _dc3d(self):
    #     raise NotImplementedError

    # def _dcc3d(self):
    #     raise NotImplementedError

    # def _ac3d(self):
    #     raise NotImplementedError

    # def _emc3d(self):
    #     raise NotImplementedError

    # def _qec3d(self):
    #     raise NotImplementedError


# TODO double inheritance from _AbaqusElement3D
class AbaqusTetrahedronElement(TetrahedronElement):
    """Abaqus implementation of :class:`TetrahedronElement`

    Note
    ----
    For more information check here:

        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-c-solidcont.htm?contextscope=cloud&id=4ca54694ed664f459b7603ca652f5b7a
        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-r-3delem.htm?contextscope=cloud&id=ef2239f0cc404c199127f51c39a2834f

    """

    __doc__ = __doc__ or ""
    __doc__ += TetrahedronElement.__doc__ or ""
    __doc__ += """
    Additional Parameters
    ---------------------
    reduced : bool, optional
        Reduce the integration points, by default ``False``.
    hybrid : bool, optional
        Use hybrid formulation, by default ``False``.
    optional : str, optional
        String with additional optional parameters, by default `None`.
    implementation : str, optional
        Name of the implementation model to be used, by default `None`. This can
        be used alternatively to the `type`, `reduced`, `optional` and `warping parameters
        to directly define the model to be used. If both are specified, the
        `implementation` overwrites the others.

    """

    def __init__(
        self,
        nodes,
        section=None,
        type="C3D",  # FIXME remove this,
        heat=False,
        reduced=False,
        hybrid=False,
        optional=None,
        implementation=None,
        rigid=False,
        **kwargs,
    ):
        super(AbaqusTetrahedronElement, self).__init__(
            nodes=nodes,
            section=section,
            implementation=(
                "".join(
                    [
                        "D" if heat else "",
                        implementation or "C3D",
                        str(len(nodes)),
                        "R" if reduced else "",
                        "H" if hybrid else "",
                        optional or "",
                    ]
                )
                if not (implementation)
                else implementation
            ),
            rigid=rigid,
            **kwargs,
        )
        self._type = type.upper()
        self._heat = heat
        self._reduced = reduced
        self._hybrid = hybrid
        self._optional = optional
        if len(self._nodes) not in (4, 5, 6, 8, 10, 15, 20):
            raise ValueError("A solid element with {} nodes cannot be created.".format(len(nodes)))

    @property
    @no_units
    def jobdata(self):
        try:
            return getattr(
                self,
                "_" + self.implementation[:4].lower() if not (self._heat) else "_" + self.implementation[:5].lower(),
            )()  # BUG cannot reach c3d10
        except:  # noqa: E722
            raise ValueError("{} is not a valid implementation.".format(self._implementation))

    @no_units
    def _r3d4(self):
        return _jobdata(self)

    @no_units
    def _c3d4(self):
        return _jobdata(self)

    @no_units
    def _dc3d4(self):
        return _jobdata(self)

    @no_units
    def _c3d10(self):
        raise NotImplementedError


class AbaqusHexahedronElement(HexahedronElement):
    """Abaqus implementation of :class:`HexahedronElement`

    Note
    ----
    For more information check here:

        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-c-solidcont.htm?contextscope=cloud&id=4ca54694ed664f459b7603ca652f5b7a
        - https://help.3ds.com/2022x/English/DSDoc/SIMA3DXELMRefMap/simaelm-r-3delem.htm?contextscope=cloud&id=ef2239f0cc404c199127f51c39a2834f

    """

    __doc__ = __doc__ or ""
    __doc__ += HexahedronElement.__doc__ or ""
    __doc__ += """
    Additional Parameters
    ---------------------
    reduced : bool, optional
        Reduce the integration points, by default ``False``.
    hybrid : bool, optional
        Use hybrid formulation, by default ``False``.
    optional : str, optional
        String with additional optional parameters, by default `None`.
    implementation : str, optional
        Name of the implementation model to be used, by default `None`. This can
        be used alternatively to the `type`, `reduced`, `optional` and `warping parameters
        to directly define the model to be used. If both are specified, the
        `implementation` overwrites the others.

    """

    def __init__(
        self,
        nodes,
        section=None,
        type="C3D",
        reduced=False,
        hybrid=False,
        optional=None,
        implementation=None,
        rigid=False,
        **kwargs,
    ):
        super(AbaqusHexahedronElement, self).__init__(
            nodes=nodes,
            section=section,
            implementation=implementation
            or "".join(
                [
                    type,
                    str(len(nodes)),
                    "R" if reduced else "",
                    "H" if hybrid else "",
                    optional or "",
                ]
            ),
            rigid=rigid,
            **kwargs,
        )
        self._type = type.upper()
        self._reduced = reduced
        self._hybrid = hybrid
        self._optional = optional
        if len(self._nodes) not in (4, 5, 6, 8, 10, 15, 20):
            raise ValueError("A solid element with {} nodes cannot be created.".format(len(nodes)))

    @property
    @no_units
    def jobdata(self):
        try:
            return getattr(self, "_" + self.implementation[:4].lower())()
        except:  # noqa: E722
            raise ValueError("{} is not a valid implementation.".format(self._implementation))

    @no_units
    def _c3d4(self):
        return _jobdata(self)
