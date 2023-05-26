#******************************* Importations : ********************************

# Built-in modules :
import inspect
import typing


#******************************** Fonctions : **********************************

def _get_name_of_type(ty):
    tyName = str(ty).split()
    return tyName[1][1:-2]   if( tyName[0] == '<class' )else   tyName[0]


def _check_type (obj , ty) :

    """
    ROLE :
        Vérifie qu'un objet 'obj' soit d'un certain type 'ty'.

    NOTE :
        _check_type() devrait être sensé supporter tout les types même les types créés à l'aide de typing.
        Mais pour l'instant je n'ai implémenté que la gestion de l'union de types.

        Néanmoins pour les version de python supérieur ou égale à python 3.11 il n'est plus nécessaire de gérer ce cas
        depuis que la PEP 604 ait été accéptée dans Python (rend isinstance() et issubclass() compatible avec les unions de types). 

        J'en implémenterai d'autre si besoin.

        Pourquoi j'en ai besoin :
            J'utilise très souvent les types optionels or : Optional[int] = Union[int , None]
    """

    try :
        return isinstance(obj , ty)
    except TypeError :

        # Cas : Union
        if issubclass(type(ty) , (type(typing.Union[int,float]))) :
            return any(_check_type(obj , t) for t in ty.__args__)

        # Autres Cas :
        raise NotImplementedError


def statically_typed_function(func:callable):    # REMARQUE : les noms ne sont pas définitifs
    """ Ce décorateur permet d'empécher qu'un argument ait un type différent de celui déclaré dans le ** TypeHint **. """


    def new_func(*args , **kwargs):

        sig = inspect.signature(func)

        arguments_of_func = sig.bind(*args , **kwargs)
        arguments_of_func.apply_defaults()
        arguments_of_func = arguments_of_func.arguments

        func_annotations = func.__annotations__

        L = ( ( arguments_of_func[param], func_annotations[param], str(sig.parameters[param].kind)   if(str(sig.parameters[param].kind) in {'VAR_POSITIONAL', 'VAR_KEYWORD'})else   None ) for param in func_annotations if param != "return" )

        for argValue , argType , argKind in L :
            if argKind :
                if argKind == 'VAR_POSITIONAL' :
                    for av in argValue :
                        None   if(_check_type(av , argType))else   exec(f"raise TypeError('{av} is not {_get_name_of_type(argType)}')")
                else : # argKind == 'VAR_KEYWORD' 
                    for av in argValue.items() :
                        None   if(_check_type(av , argType))else   exec(f"raise TypeError('{av} is not {_get_name_of_type(argType)}')")
            else :
                None   if(_check_type(argValue , argType))else   exec(f"raise TypeError('{argValue} is not {_get_name_of_type(argType)}')")

        returnValue = func(*args , **kwargs)
        try :
            returnType = func_annotations["return"]
            return returnValue   if(_check_type(returnValue , returnType))else  exec(f"raise TypeError('{func.__name__} did not return {_get_name_of_type(returnType)} object')")
        except KeyError :
            return returnValue


    return new_func