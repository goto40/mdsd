# Introduction

This site contains a collection of demos on **M**odel **D**riven **S**oftware **D**esign (MDSD). MDSD implies that code is derived (generated) from model data.
MDSD fosters **single source** (the model) and **consistency** (in the generated artifacts).

This collection is a **proof of concept**. Many aspects are experimental
and not meant to be used for production.

We focus on 

 * Modeling **data formats** (like C-structs).
 * Modeling **algorithms** in terms of black boxes with inputs, outputs, and parameters.
 
## Single Source

From a single source we **generate code for different target languages**
(like C++ or Python). Based on the
model information, data structures can be serialized and deserialized in
different formats (as well as other operations on data structures). 
Algorithms can be implemented in different languages to provide an **operative implementation**
(possibly highly optimized) and a **reference implementation**.
Generated algorithm control code allows to have a similar interface in
different languages. Our approach provides a detailed **algorithm documentation**,
which links a reference implementation to an optimized implementation and eases
the **validation and verification** of algorithm code. 

We think that algorithms shall be implemented manually and 
**quality is ensured through comparisons** of different implementations.

## Employed Tools

We employ the **language workbench [textX](http://textx.github.io/textX/stable/)** to implement the **modeling and code generation toolset** for our
approach. A minimal set of dependencies is a major driver for this decision. Moreover, the high test coverage of
[textX](https://github.com/textX/textX) makes a possible patch in future times faisible (even for small teams).


We also show **how to execute operative C++ code in environments like Python or MATLAB**.
For this, we employ **[SWIG](http://www.swig.org/)** and the serializaion/deserialization
capabilities of the generated code. This aspect is in principal indepenent of
the generated code. The generated code is optimized to allow an easy processing 
with the SWIG tool. We also provide a configuration generator to make the
use of SWIG simpler.

### Modelling tools

All textx languages are defined as individual python projects, as well as all code generators. This makes it easy to add new code generators or new languages using the existing ones.

Also you can define search paths to allow models to include models from other locations. This allows to easily create depdendent modules with item models (using environemt variables):

 - `ITEM_LANG_SEARCH_PATH`: additional search directories
 - `ITEM_LANG_FILE_SUFFIX`: model file suffix (default: `*.item`)

```
$ textx list-languages
textX (*.tx)                  textX[2.4.0.dev0]                       A meta-language for language definition
algo (*.algo)                 algo-lang[0.0.2]                        
item (*.item)                 item-lang[0.0.3]                        
$ textx list-generators
any -> dot                    textX[2.4.0.dev0]             Generating dot visualizations from arbitrary models
textX -> dot                  textX[2.4.0.dev0]             Generating dot visualizations from textX grammars
textX -> PlantUML             textX[2.4.0.dev0]             Generating PlantUML visualizations from textX grammars
item -> cpp                   item-codegen-cpp[0.0.3]       Generating c++ code from the item model
item -> python                item-codegen-python[0.0.4]    Generating c++ code from the item model
algo -> cpp                   algo-codegen-cpp[0.0.2]       Generating c++ code from the item model
algo -> python                algo-codegen-python[0.0.2]    Generating c++ code from the algo model
```