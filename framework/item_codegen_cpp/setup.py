#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="item_codegen_cpp",
    version="0.0.3",
    description="item mdsd tool",
    author="Pierre Bayerl",
    author_email="pierre DOT bayerl AT googlemail DOT com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    package_data={'': ['*.tx']},
    install_requires=["textX", "item_lang"],
    entry_points={
        "textx_generators": ["item_cpp = item_codegen_cpp.codegen_cpp:generate_cpp",
                            ],
    },
)
