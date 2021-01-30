# MDSD demo toolchain and examples

Here, we present a simple item and algorithmic
interface specification tool among other aspects.

## Purpose

Provide a simple MDSD chain as a proof of concept.

The goal is to generate 100% code for item specififcations 
(input/output data and parameters for algorithms) and to
provide a homogeneous algorithm skeleton.

The idea is that the algorithm is implemented in a reference
language (e.g. Python with numpy) and a target language. We
then provide means to run tests in order to compare these
implementations.

**Question**: Why do we generate 100% of the item code,
but not the algorithm code?
**Answer**: We think that algothm development deserves much
creativiy. This makes it important to have two independent
implementations (together with some docu, e.g. as python
notebook). A single source for such an algorithm would
hinder a free development of that algorithm and would **not**
make it clearer **what** the algothm does. This is part of the
docu, provided manually.

The item code is stereotypical. Here, we take full advantage of a 
clear specification language and single source.

## Technologies employed

 * `textx`: a MDSD tool to allow modeling, validation and easy code generation.
 * `python`, `C++`: general purpose languages.
 * `swig`: a simple wrapper generator (allowing to call `C++` from `python`). 

## How to use

TODO

## Features

TODO

## How to run tests / develop

 * Command line:
   * ./activate_env
   * sh run_tests.sh
 * pycharm
   * ...

## Limitations

 * SWIG does not map namespaces (in C++) to modules (e.g. in Python).
   This may lead to name collisions (objects can be renamed for SWIG only,
   if required; see SWIG docu).
