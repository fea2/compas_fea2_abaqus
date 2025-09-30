from compas_fea2.problem import ScalarLoad
from compas_fea2.problem import VectorLoad

# from compas_fea2.units import no_units

# from typing import Iterable

dofs = ["x", "y", "z", "xx", "yy", "zz"]

scalar_load_types = {}

class AbaqusVectorLoad(VectorLoad):
    """Abaqus implementation of :class:`VectorLoad`.\n"""
    __doc__ += VectorLoad.__doc__
    """ 
    Additional Parameters
    ---------------------
    modify : str, optional
         If `MOD`, if there are loads applied at the same location in previous
         steps, these are deleted, otherwise add the displacement to the previous.
         If `NEW`, all the loads (of the same type) applied in previous steps are
         deleted.
         If `None`, the loads are added to the ones of previous steps.
         By defult is `None`.
     follow : bool, optional
         if `True` the load follows the deformation of the element.

     Additional Attributes
     ---------------------
     op : bool
         If ``True``, change previous displacements applied at the same location, otherwise
         add the displacement to the previous.
     follow : bool
         if `True` the load follows the deformation of the element.

     Note
     ----
     The default behavior for abaqus when adding new loads in different steps at
     the same locatio is to `modify` the loads with the new value (`OP=MOD`). In
     abaqus CAE it is possible to `propagate` the loads: this means that internally
     the software adds up the loads and create a new load which combines the previous.
"""

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes="global", modify=False, follow=False,**kwargs):
        super().__init__(x, y, z, xx, yy, zz, axes, **kwargs)
        self._modify=f", OP={modify}" if modify else ", OP=MOD"  # In abaqus the default is MOD
        self._follow=", follower" if follow else ""

    @property
    def modify(self):
        return self._modify
    
    @property
    def follow(self):
        return self._follow
    
    @property
    def vectorload_types(self):
        return {"CLoad":"Concentrated Force"}
    
    def jobdata(self, nodes, type):
        
        data_section = [
            f"** Name: {self.name} Type: {self.vectorload_types[type]}",
            f"*{type}{self._modify}{self._follow}"
        ]
        if not isinstance(nodes, Iterable):
            nodes = [nodes]
        for node in nodes:
            for comp, dof in enumerate(dofs, 1):
                if getattr(self, dof):
                    data_section += ["{}-1.{}, {}, {}".format(node.part.name, node.key, comp, self.components[dof])]
        return "\n".join(data_section)


class AbaqusScalarLoad(ScalarLoad):
    """Abaqus implementation of :class:`ScalarLoad`.\n"""
    __doc__ += ScalarLoad.__doc__
    """ 
    Additional Parameters
    ---------------------
    modify : str, optional
         If `MOD`, if there are loads applied at the same location in previous
         steps, these are deleted, otherwise add the displacement to the previous.
         If `NEW`, all the loads (of the same type) applied in previous steps are
         deleted.
         If `None`, the loads are added to the ones of previous steps.
         By defult is `None`.
     follow : bool, optional
         if `True` the load follows the deformation of the element.

     Additional Attributes
     ---------------------
     op : bool
         If ``True``, change previous displacements applied at the same location, otherwise
         add the displacement to the previous.
     follow : bool
         if `True` the load follows the deformation of the element.

     Note
     ----
     The default behavior for abaqus when adding new loads in different steps at
     the same locatio is to `modify` the loads with the new value (`OP=MOD`). In
     abaqus CAE it is possible to `propagate` the loads: this means that internally
     the software adds up the loads and create a new load which combines the previous.
"""

    def __init__(self, scalar_load, modify=False, follow=False,**kwargs):
        super().__init__(scalar_load, **kwargs)
        self._modify=f", OP={modify}" if modify else ", OP=MOD"  # In abaqus the default is MOD
        self._follow=", follower" if follow else ""

    @property
    def modify(self):
        return self._modify
    
    @property
    def follow(self):
        return self._follow
    
    @property
    def scalarload_types(self):
        return {}
    
    def jobdata(self, nodes, type):
        raise NotImplementedError

# class AbaqusHeatFluxLoad(HeatFluxLoad):
#     """Abaqus implementation of :class:`HeatFluxLoad`.\n"""

#     __doc__ += HeatFluxLoad.__doc__

#     def __init__(self, q, **kwargs):
#         super().__init__(q, **kwargs)

#     def jobdata(self, surface):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).

#         """
#         data_section = []
#         data_section.append(f"** Name: {self.name} Type: Surface heat flux")
#         data_section.append("*Dsflux")
#         if self.heatflux.amplitude:
#             data_section[-1] += f", amplitude={self.heatflux.amplitude}"
#         data_section.append(f"{surface.part.name}-1.{surface.element.key}, {surface.tag}, S, {self.q}")
#         return "\n".join(data_section)

#         # data_section = []
#         # data_section.app= ['** Name: {} Type: Surface heat flux'.format(self.name),
#         #                 '*Dsflux',
#         #                 '{}, HF, {}'.format(.name, self.q)]
#         # return '\n'.join(data_section)
