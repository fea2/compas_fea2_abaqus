"""Entry-point registration for the Abaqus backend.

- Builds a mapping {compas_fea2 base -> Abaqus implementation} by introspection.
- Exposes ``load_backend(register=None)`` as the entry-point callable expected by compas_fea2.
- Classes whose names start with '_' are ignored during registration.
"""

import logging
import sys
import inspect
import importlib
import pkgutil

PLUGIN_NAME = "abaqus"
logger = logging.getLogger(__name__)


def build_backend_mapping():
    """Build and return the backend class mapping.

    Returns
    -------
    dict
        Mapping of compas_fea2 abstract base classes to Abaqus concrete classes.

    Notes
    -----
    - Scans this package and all submodules for classes.
    - If a class defines ``__implements__`` (a class or iterable of classes), those
      bases are used. Otherwise, the first compas_fea2 base found in the MRO is used.
    - Submodules that fail to import are skipped and reported at debug level.
    """
    mapping = {}

    package_name = __name__.rsplit(".", 1)[0]  # compas_fea2_calculix
    package_module = sys.modules[package_name]

    imported_modules = []
    if hasattr(package_module, "__path__"):
        for _finder, modname, _ispkg in pkgutil.walk_packages(package_module.__path__, prefix=package_name + "."):
            try:
                m = importlib.import_module(modname)
                imported_modules.append(m)
            except Exception as e:
                logger.debug("[abaqus] Skipped importing %s: %s", modname, e)

    def iter_plugin_classes():
        for module in [package_module] + imported_modules:
            for obj in vars(module).values():
                if (
                    inspect.isclass(obj)
                    and getattr(obj, "__module__", "").startswith(package_name)
                    and not getattr(obj, "__name__", "").startswith("_")
                ):
                    yield obj

    def compas_bases_for(cls):
        implements = getattr(cls, "__implements__", None)
        if implements:
            if not isinstance(implements, (tuple, list)):
                implements = (implements,)
            return [b for b in implements if inspect.isclass(b)]
        for base in cls.__mro__[1:]:
            mod = getattr(base, "__module__", "")
            if mod.startswith("compas_fea2.") and not mod.startswith(package_name + "."):
                return [base]
        return []

    for cls in iter_plugin_classes():
        for base in compas_bases_for(cls):
            prev = mapping.get(base)
            if prev and prev is not cls:
                logger.warning("[abaqus] Overriding mapping for %s: %s -> %s", base, prev, cls)
            mapping[base] = cls

    logger.info("Abaqus backend mapping built (%d bindings).", len(mapping))
    return mapping


def load_backend(register=None):
    """Entry-point loader for the Abaqus backend.

    Parameters
    ----------
    register : callable or None, optional
        If provided, it will be called as ``register(mapping, backend_name=PLUGIN_NAME)``.
        If not provided, the mapping is returned to the caller.

    Returns
    -------
    dict or None
        The mapping when no register function is given; otherwise ``None``.

    Raises
    ------
    Exception
        Propagates any exception raised while building the mapping.
    """
    mapping = build_backend_mapping()
    if register is not None:
        register(mapping, backend_name=PLUGIN_NAME)
        return None
    return mapping
