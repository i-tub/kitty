import functools
import importlib
import os
import sys

from kitty import constants

def munge_title(title, max_title_length):
    return title


@functools.lru_cache(maxsize=None)
def get_func(name, opts):
    val = getattr(opts, name, None)
    if val == 'None':
        func = globals().get(name)
        return func
    modfile, funcname = val.split('::')
    path = os.path.join(constants.config_dir, modfile)
    modname = 'kitty.userfunc.' + os.path.splitext(modfile)[0]
    module = sys.modules.get(modname)
    if module is None:
        # import module
        spec = importlib.util.spec_from_file_location(modname, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[modname] = module
        spec.loader.exec_module(module)
    return getattr(module, funcname)
