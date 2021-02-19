import textx
import textx.scoping.providers as scoping_providers
from textx import get_location
from textx.scoping import ModelRepository
from textx.exceptions import TextXSemanticError
import item_lang.metamodel_formula as f
from os.path import dirname, join, abspath
import os
import item_lang.metamodel_classes as mmc
import item_lang.validation as v
from item_lang.properties import get_property_set, get_default_property_set


@textx.language("item", "*." + os.getenv("ITEM_LANG_FILE_SUFFIX", "item"))
def lang():
    this_folder = dirname(abspath(__file__))
    fn = join(this_folder, "item_lang.tx")
    mm = textx.metamodel_from_file(
        fn, builtin_models=ModelRepository(), classes=mmc.get_all_classes()
    )
    modeltext = """
    package built_in
    property_set default_properties {
        property optional applicable for rawtype minValue : ATTRTYPE
        property optional applicable for rawtype maxValue : ATTRTYPE
        property optional applicable for rawtype constValue : ATTRTYPE
        property optional applicable for rawtype, enum defaultValue : ATTRTYPE
        property optional applicable for rawtype(char) defaultStringValue : STRING
        property optional description : STRING
        property optional applicable for scalar breakTimesPerMessage : BOOL
        property optional applicable for scalar is_message_id_field : BOOL { 0 to 1 times per message }
        property optional applicable for scalar is_message_length_field : BOOL { 0 to 1 times per message }
    }
    rawtype double FLOAT 64
    rawtype float64 FLOAT 64
    rawtype float FLOAT 32
    rawtype float32 FLOAT 32
    rawtype bool BOOL 1
    rawtype char INT 8
    """
    for b in range(1, 65):
        modeltext += "rawtype uint{} UINT {}\n".format(b, b)
    for b in range(2, 65):
        modeltext += "rawtype int{} INT {}\n".format(b, b)
        modeltext += "rawtype sint{} INT {}\n".format(b, b)

    mm.builtin_models.add_model(mm.model_from_str(modeltext))

    def prop_scope(refItem, attr, attr_ref):
        ps = get_property_set(refItem)
        defaultPropertySet = get_default_property_set(textx.get_metamodel(refItem))
        if isinstance(ps, textx.scoping.Postponed):
            return ps
        while ps is not None:
            for pd in ps.property_definitions:
                if pd.name == attr_ref.obj_name:
                    return pd
            if ps.extends is None and ps is not defaultPropertySet:
                ps = defaultPropertySet
            else:
                ps = ps.extends
        return None

    search_path = os.getenv("ITEM_LANG_SEARCH_PATH", None)
    if search_path is not None:
        search_path = search_path.split(os.pathsep)
        search_path = list(filter(lambda x: len(x) > 0, search_path))
        if len(search_path) == 0:
            search_path = None

    mm.register_scope_providers(
        {
            "*.*": scoping_providers.FQNImportURI(search_path=search_path),
            "Property.definition": prop_scope,
        }
    )

    def text2bool(value):
        if value == "true":
            return 1
        if value == "false":
            return 0
        raise Exception("unexpected/impossible")

    object_processors = {"HexNumber": lambda x: int(x, 16), "BoolNumber": text2bool}
    checks = v.get_all_checks_as_map()
    for c in checks:
        if c not in mm:
            raise Exception(f"unexpected check found for unknown class {c}")
    object_processors.update(checks)

    mm.register_obj_processors(object_processors)
    return mm
