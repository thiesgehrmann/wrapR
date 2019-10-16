import collections

from .loader import loadExternalModule

rpy2 = loadExternalModule('rpy2')
np   = loadExternalModule('numpy')

##################################################################################

def _try_rpy2py(obj):
    """
    Attempt to convert an rpy2 object to a python object
    parameters:
    -----------
    obj: an rpy2 object

    returns:
    --------
    o: A converted object, if it was possible to convert, otherwise obj, the unconverted object
    """
    try:
        return rpy2.robjects.conversion.rpy2py.dispatch(type(obj))(obj)
    except Exception as e:
        print(e)
        return obj
    #etry
#edef

##################################################################################

def _try_py2rpy(obj):
    """
    Attempt to convert a python object to a rpy2 object
    parameters:
    -----------
    obj: an rpy2 object

    returns:
    --------
    o: A converted object, if it was possible to convert, otherwise obj, the unconverted object
    """
    print(type(obj))
    try:
        return rpy2.robjects.conversion.py2rpy.dispatch(type(obj))(obj)
    except Exception as e:
        return obj
    #etry
#edef


##################################################################################

@rpy2.robjects.conversion.py2rpy.register(dict)
def dict2listvector(D):
    """
    Convert a dictionary to an R ListVector
    """
    if not isinstance(D, dict):
        raise ValueError("Expected dict. Got '%s'." % str(type(D)))
    #fi
    return rpy2.robjects.ListVector(D)
#edef

##################################################################################

@rpy2.robjects.conversion.rpy2py.register(rpy2.robjects.ListVector)
def listvector2dict(D):
    """
    Convert a StrVector to a dictionary
    Note, that this conversion is not the inverse of dict2ri, as R values are always lists...
    Thus, ri2dict(dict2ri({'a': 1})) -> { 'a': [1]}
    """
    
    return { k : _try_rpy2py(v) for (k,v) in D.items() }
#edef

@rpy2.robjects.conversion.rpy2py.register(rpy2.robjects.vectors.ListVector)
def vectorlistvector2dict(D):
    """
    Convert a StrVector to a dictionary
    Note, that this conversion is not the inverse of dict2ri, as R values are always lists...
    Thus, ri2dict(dict2ri({'a': 1})) -> { 'a': [1]}
    """
    
    return { k : _try_rpy2py(v) for (k,v) in D.items() }
#edef

##################################################################################

@rpy2.robjects.conversion.py2rpy.register(tuple)
def tuple2array(T):
    """
    Convert a tuple to an array.
    It is first converted to a numpy array, and then, based on that to an R array
    """
    if not isinstance(T, tuple):
        raise ValueError("Expected tuple. Got '%s'." % str(type(T)))
    #fi
    
    return rpy2.robjects.numpy2ri.numpy2rpy(np.array(T))
#edef

##################################################################################

@rpy2.robjects.conversion.py2rpy.register(type(None))
def none2null(N):
    """
    Convert a None type to NULL
    """
    return rpy2.robjects.NULL
#edef

##################################################################################

def activate():
    original_converter = rpy2.robjects.conversion.converter
    new_converter = rpy2.robjects.conversion.Converter('wrapR conversion',
                                         template=original_converter)

    for k, v in rpy2.robjects.conversion.py2rpy.registry.items():
        if k is object:
            continue
        #fi
        new_converter.py2rpy.register(k, v)
    #efor

    for k, v in rpy2.robjects.conversion.rpy2py.registry.items():
        if k is object:
            continue
        #fi
        new_converter.rpy2py.register(k, v)
    #efor

    rpy2.robjects.conversion.set_conversion(new_converter)
#edef

##################################################################################