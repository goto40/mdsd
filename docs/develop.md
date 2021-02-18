# Develop and maintain the software

Here, we describe how to develop and maintain the software.
Also have a look at the [architecture](architecture.md).

## Setup/Install for maintainance

We provide a script `activate_env` to setup a virtual
environment for python and CMake projects (C++). All
software is installed in the `venv` directoroy created by
the script. use `mycmake` instead of cmake to install
any cmake project into the local environment.

You can alternatively also install any of the 
projects in your system (not recommended for development).

## Unittests

Execute `run_tests.sh` within the virtual environment (`activate_env`).
This executes all unittests for all projects in this repo.
All projects also have such a `run_tests.sh` script to
execute tests for one sub project.
