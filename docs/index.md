# Introduction

This site contains a collection of demos
on how MDSD can be applied to SW development.

We focus on 

 * Modeling data formats
 * Modeling algorithms in terms of black boxes with inputs, outputs, and parameters
 
## Single Source

From a single source we **generate code for different target languages** (like C++ or Python). Based on the
model information, data structures can be serialized and deserialized in different formats. 
Algorithms can be implemented in different languages to provide an **operative implementation**
(possibly highly optimized) and a **reference implementation**.
Generated algorithm control code allows to have a similar interface in
different languages. Our approach provides a detailed **algorithm documentation**,
which links a reference implementation to an optimized implementation and eases
the **validation and verification** of algorithm code. 


## Employed Tools

We employ the language workbench [textX](http://textx.github.io/textX/stable/) to implement the toolset for our
approach. A minimal set of dependencies is a major driver for this decision. Moreover, the high test coverage of
[textX](https://github.com/textX/textX) makes a possible patch in future times faisible (even for small teams).


We also show how to execute operative C++ code in environments like Python or MATLAB. For this we employ
[SWIG](http://www.swig.org/). This aspect is in principal indepenent of the generated code. The generated code is 
optimized to allow an easy processing with the SWIG tool. We also provide a configuration generator to make the
use of SWIG simpler.
