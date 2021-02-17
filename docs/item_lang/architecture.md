# Software Architecture

Here, we describe the rough architecture of the software

## Language

 * `item_lang` is a [textx](https://github.com/textX/textX) language.
 * `item_lang/__init__.py` defines the language (compare also `setup.py`).
 * A fixed base model is included (see `item_lang/__init__.py`)
   to define some basic types (like `built_in.uint32`).
 
## Grammar

 * The grammar is located in `item_lang/item_lang.tx`.

![image](images/item_lang.svg)


## Meta model classes

 * Metamodel classes are located in `item_lang/metamodel_classes.py`
   and `item_lang/metamodel_formula.py`.
 * All metamodel classes are made available by `item_lang.metamodel_classes.get_all_classes()`.


## Model Validation

 * All validation procedures are located in `item_lang/validation.py`.
 * All validation functions in the validation module must start with `check_` followed by
   the class name of the model element to be checked (e.g. `check_Attribute`).
 * All validation functions are included automatically by the metamodel (based on the function name).


## Code Generators

 * Generators are shipped separate python projects.
 * They make use of the core `item_lang` language and tools.
 * Common concept of "enhanced reflection", which fits into a visitor pattern.
 * Note: for the moment you find the generators embedded in this project...
