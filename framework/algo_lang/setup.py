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
    install_requires=["textX", "item_lang"],
    entry_points={
        "textx_languages": ["algo = algo_lang:lang",],
    },
)
