#!/usr/bin/env python

from setuptools import setup #, find_packages
import os

package_name = 'codegen_test_support'

my_packages = [package_name] #find_packages(where='src-gen/swig', exclude=[])

setup (name = package_name,
       version = '0.2',
       author      = "pierre",
       description = """codegen_test_support""",
       packages = my_packages,
       package_dir = {'': '.'}
       )
