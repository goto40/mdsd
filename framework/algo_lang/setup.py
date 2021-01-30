#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="algo_lang",
    version="0.0.2",
    description="algo mdsd tool",
    author="Pierre Bayerl",
    author_email="pierre DOT bayerl AT googlemail DOT com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    install_requires=["textX"],
    entry_points={
        "textx_languages": ["algo = algo_lang:lang",],
        "textx_generators": [
            "algo_cpp = algo_lang.codegen_cpp:generate_cpp",
            "algo_python = algo_lang.codegen_python:generate_python",],
    },
)
