import textx
import textx.scoping.providers as scoping_providers
from textx import get_location
from textx.exceptions import TextXSemanticError


grammar = r"""
  reference item
  Model: imports*=Import dissector=Dissector;
  Dissector: 'dissector' name=ID '{'
    'parse' item=[item.Struct|FQN]
    'for' channels*=Channel
  '}';
  Channel: 
    (udp?='udp' port=INT)|
    (tcp?='tcp' port=INT)
  ;
  FQN: ID('.'ID)*;
  Import: 'import' importURI=STRING;
"""


@textx.language("dissector", "*.dissector")
def lang():
    mm = textx.metamodel_from_str(grammar)
    mm.register_scope_providers({"*.*": scoping_providers.FQNImportURI()})
    return mm
