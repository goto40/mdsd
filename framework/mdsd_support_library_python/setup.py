#!/usr/bin/env python

from setuptools import setup #, find_packages
import os

package_name = 'mdsd_support_library'

my_packages = [package_name] #find_packages(where='src-gen/swig', exclude=[])

setup (name = package_name,
       version = '0.2',
       author      = "pierre",
       description = """Simple swig example""",
       packages = my_packages,
       package_dir = {'': '.'}
       )
