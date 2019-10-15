import importlib

def loadExternalModule(module, attr=None):
    """
    Load a python module. If the module does not exist, then the module is not loaded, and instead an AbsentModule object is returned, which raises an error when an attempt is made to use the module.
    This is essentially a protection to prevent the whole package from failing if a dependency is missing.
    Inputs:
    module : String. Name of the module to import
    attr: String. name of the attribute in the module to import (default None)

    Output:
    Imported Module

    This translates into the usual import utility:

    from modx import a as x  -> x = loadExternalModule('modx', 'a')
    import mody as mody      -> mody = loadExternalModule('mody')
    """

    class AbsentModule(object):
        def __init__(self, module, exception):
          self.__module = module
          self.__exception = exception
        #edef

        def __re__(self, *pargs, **kwargs):
          #msg.error("For this functionality, you need to install '%s'" % self.__module)
          raise ImportError from self.__exception
        #edef

        __getattr__ = __re__
        __getitem__ = __re__
        __call__    = __re__
    #eclass

    lmod = None
    try:
        lmod = importlib.import_module(module)
        if attr is not None:
            lmod = getattr(lmod, attr)
        #fi
    except ImportError as e:
        lmod = AbsentModule(module, e)
    #fi

    return lmod
#edef