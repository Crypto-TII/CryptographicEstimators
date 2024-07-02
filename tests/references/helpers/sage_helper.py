import inspect
import os
import types

import sage.all

from tests.references.helpers.constants import (
    DOCKER_LIBRARY_PATH,
)


def sage_import(modpath, fromlist=None):
    """
    Import a .sage module from the filename <modname>.sage

    Returns the resulting Python module.  If ``fromlist`` is given, returns
    just those members of the module into the global namespace where the
    function was called, or the given namespace.

    Based on: https://ask.sagemath.org/question/7867/importing-sage-files/?answer=48947#post-id-48947
    """

    if fromlist is None:
        raise ValueError(
            "You must declare what sage functions/variables you want to import with the 'fromList' parameter."
        )

    if "." in modpath:
        path_list = modpath.split(".")
    else:
        path_list = modpath

    modname = path_list[-1]
    path_list[-1] += ".sage"

    absolute_filepath = os.path.join(*DOCKER_LIBRARY_PATH, *path_list)

    with open(absolute_filepath) as sage_file:
        code = sage.all.preparse(sage_file.read())
        # This creates a new, dynamic module
        mod = types.ModuleType(modname)
        mod.__file__ = absolute_filepath
        # Fill with all the default Sage globals
        # We could just do a dict.update but we want to exclude dunder
        # and private attributes I guess
        for k, v in sage.all.__dict__.items():
            if not k.startswith("_"):
                mod.__dict__[k] = v

        # We run all the preparsed code into the new module
        exec(code, mod.__dict__)

    # We get the globals defined in the file that imports this function
    namespace = inspect.currentframe().f_back.f_globals

    # First check that each name in fromlist exists before adding
    # any of them to the given namespace.
    for name in fromlist:
        if name not in mod.__dict__:
            raise ImportError(f"Can not import {name} from {modname}.")

    for name in fromlist:
        namespace[name] = mod.__dict__[name]
