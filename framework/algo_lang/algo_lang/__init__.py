import textx
import textx.scoping.providers as scoping_providers
from textx import get_location
from textx.exceptions import TextXSemanticError


grammar = r"""
  reference item
  Model: imports*=Import package=Package;
  NestedPackage: '.' name=ID (package=NestedPackage|algos+=Algo);
  Package: 'package' name=ID (package=NestedPackage|algos+=Algo);
  Algo: 'algo' name=ID '{'
    'parameters' '{' parameters*=Data '}'
    'inputs' '{' inputs*=Data '}'
    'outputs' '{' outputs*=Data '}'
  '}';
  Data: name=ID ':' type=[item.Struct|FQN] ('('datatype=DataType')')?;
  Import: 'import' importURI=STRING;
  FQN: ID('.'ID)*;
  Comment: /\/\/.*$/;
  DataType: "shared_ptr";
"""


@textx.language("algo", "*.algo")
def lang():
    mm = textx.metamodel_from_str(grammar)
    mm.register_scope_providers({"*.*": scoping_providers.FQNImportURI()})

    def algo_check(a):
        for p in a.parameters:
            if p.datatype is not None:
                raise TextXSemanticError(
                    "parameter is not allowed to have {} flag".format(p.datatype),
                    **get_location(p)
                )

    mm.register_obj_processors({"Algo": algo_check})
    return mm
