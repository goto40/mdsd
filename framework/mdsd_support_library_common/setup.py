#!/usr/bin/env python

from setuptools import setup, find_packages
import os

package_name = 'mdsd-common-srcgen'

my_packages = find_packages(where='src-gen', exclude=[])

setup (name = package_name,
       version = '0.2',
       author      = "pierre",
       description = """srcgen example""",
       packages = my_packages,
       package_dir = {'': 'src-gen'}
       )
