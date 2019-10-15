import os
from .loader import loadExternalModule

rpy2 = loadExternalModule('rpy2')
np   = loadExternalModule('numpy')
pd   = loadExternalModule('pandas')

class R(object):
    """
    A wrapper for rpy2, which somewhat mimics the ipython magic functions.
    Basically, it handles the automatic conversion of some python objects to R objects.
    Further, it allows you to automatically push python objects, call code and get converted objects back to python.
    
    Example usage:
    --------------
    
    r = biu.R()
    x = pd.DataFrame([[1,2,3],[4,5,6]])
    r.push(x=x)
    r('y = x * 2')
    y = r.get('y')
    
    Or, altogether:
    ---------------
    y = r('y=x*2', push=dict(x=x), get='y')
    
    Doing a lot at the same time:
    -----------------------------
    
    y, z = r('''
        y = x * 2
        z = x + 2
        ''', push=dict(x=x), get=['y', 'z'])
    
    
    """
    _converter = None
    
    def __init__(self, debug=False):
        """
        Initialize the rpy2 wrapper

        parameters:
        -----------
        debug: bool
            When true, provide additional debugging mentions

        """
        self._debug      = debug
        from rpy2.robjects import numpy2ri
        from rpy2.robjects import pandas2ri
        from . import converter as converter
        numpy2ri.activate()
        pandas2ri.activate()
        converter.activate()
        #self._converter  = converter()
    #edef
    
    #def add_converter(self, obj_type, convert_func):
    #    """
    #    Add a converter to the object, if there is one missing.
    #    
    #    parameters:
    #    -----------
    #    obj_type: the type of the object that this converter relates to
    #    convert_func: function. The function that should be applied
    #    """
    #
    #    self._converter.py2rpy.register(obj_type, convert_func)
    ##edef
        
    def push(self, **kwargs):
        """
        Push values to R, based on the current converter
        
        parameters:
        -----------
        kwargs: Dictionary of values
        
        Example usage:
        --------------
        
        r.push(x=10, y='pool', ages=[10, 50, 100])
        """
        
        if kwargs is None:
            return None
        #fi
        
        for (k,v) in kwargs.items():
            rpy2.robjects.r.assign(k, v)
        #efor
    #edef
        
    def get(self, name, *pargs):
        """
        Get a value from R, based on the current converter
        
        parameters:
        -----------
        name: return this variable from the R instance
        *pargs, if specified, return a tuple of name + those in pargs
        
        returns:
        --------
        Either a converted R object, or
        if pargs is specified, then a tuple of values
        """

        if len(pargs)  == 0:
            return rpy2.robjects.globalenv.find(name)
        else:
            return [ rpy2.robjects.globalenv.find(n) for n in ([name] + list(pargs)) ]
        #fi
            
    #edef
    
    def exec(self, cmd, push=None, get=True):
        """
        Call R code, pushing values, and returning values if necessary
        
        parameters:
        -----------
        cmd: The R code you want to execute
        push: Dictionary of name:value pairs that you want to introduce to R session
        get: List of R object values that you want to get back
        
        returns:
        ---------
        if get is False, it returns nothing.
        If get is True, it returns the returned value from the R code.
        if get is not None, it returns a value, as specified by the get() function.
        """
        if push is None:
            push = {}
        #fi
        
        self.push(**push)
        
        try:
            res = rpy2.robjects.r(cmd)
        except Exception as e:
            print(e)
            if self._debug:
                raise e
            #fi
            return None
        #etry
        
        if isinstance(get, bool) and get:
            return rpy2.robjects.conversion.rpy2py(res)
        elif isinstance(get, bool) and (not get):
            return None
        elif isinstance(get, str):
            return self.get(get)
        else:
            return self.get(*get)
        #fi
    #edef
    
    def __call__(self, cmd, push=None, get=True):
        """
        Call R code, pushing values, and returning values if necessary
        
        parameters:
        -----------
        cmd: The R code you want to execute
        push: Dictionary of name:value pairs that you want to introduce to R session
        get: List of R object values that you want to get back
        
        returns:
        ---------
        if get is False, it returns nothing.
        If get is True, it returns the returned value from the R code.
        if get is not None, it returns a value, as specified by the get() function.
        """
        return self.exec(cmd, push, get)
    #edef
#eclass