#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from setuptools import setup, find_packages
import os

package_name = os.environ['PACKAGE_NAME']

my_packages = find_packages(where='src-gen/python', exclude=[])

setup (name = package_name,
       version = '0.2',
       author      = "pierre",
       description = """Simple swig example""",
       packages = my_packages,
       package_dir = {'': '.'}
       )
