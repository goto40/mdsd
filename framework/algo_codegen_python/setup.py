#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="algo_codegen_python",
    version="0.0.2",
    description="algo mdsd tool (python)",
    author="Pierre Bayerl",
    author_email="pierre DOT bayerl AT googlemail DOT com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    install_requires=["textX", "algo_lang", "item_lang", "item_codegen_python"],
    entry_points={
        "textx_generators": [
            "algo_python = algo_codegen_python.codegen_python:generate_python",
        ]
    },
)
