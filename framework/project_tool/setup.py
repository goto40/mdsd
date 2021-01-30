#!/usr/bin/env python

from setuptools import setup
import os

setup (
    name = 'project_tool',
    version = '0.0',
    author      = "pierre",
    description = """a project file generator""",
    packages = ['project_tool'],
    install_requires=["click"],
    entry_points={
        'console_scripts': [
            'projecttool=project_tool.cli:swig_tool',
        ],
    },
)
