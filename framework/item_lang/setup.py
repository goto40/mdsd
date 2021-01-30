#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="item_lang",
    version="0.0.3",
    description="item mdsd tool",
    author="Pierre Bayerl",
    author_email="pierre DOT bayerl AT googlemail DOT com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    package_data={'': ['*.tx']},
    install_requires=["textX"],
    entry_points={
        "textx_languages": ["item = item_lang:lang",],
    },
)
