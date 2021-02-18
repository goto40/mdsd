# Introduction

This site contains a collection of demos on **M**odel **D**riven **S**oftware **D**esign (MDSD). MDSD implies that code is derived (generated) from model data.
MDSD fosters **single source** (the model) and **consistency** (in the generated artifacts).

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
