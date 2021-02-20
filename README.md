# MDSD demo toolchain and examples ![badge](https://github.com/goto40/mdsd/actions/workflows/run_tests.yml/badge.svg)

Here, we present a simple item and algorithmic
interface specification tool among other aspects.

 * Items = data structures (like C structs)
 * Algorithms = functions to transform items into other items.

## Purpose

Provide a simple MDSD chain as a **proof of concept**. Many aspects are experimental
and not meant to be used for production.

The goal is to **generate 100% code for item specifications** 
(input/output data and parameters for algorithms) and to
**provide a homogeneous algorithm skeleton**.

The idea is that the algorithm is implemented in a reference
language (e.g., in Python with numpy) and a target language. We
then provide means to run tests in order to compare these
implementations.

**Question**: Why do we generate 100% of the item code,
but not the algorithm code?
**Answer**: We think that algorithm development deserves much
creativity. This makes it important to have two independent
implementations (together with some documentation, e.g. as python
notebook). A single source for such an algorithm would
obscure how the algorithm works. This is part of the
documentation, provided manually.

The **item code is stereotypical**. Here, we take full advantage of a 
clear specification language and single source.

## Read more...

```
./activate_env
makdocs serve
```
