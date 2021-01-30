#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from setuptools import setup, Extension #, find_packages
import os

swig_module_name = os.environ['SWIG_PACKAGE_NAME']

extra_compile_args = ["-std=c++17", "-Wall", "-Wextra", "-Weffc++"]
swig_module = Extension('_{}'.format(swig_module_name),
                           sources=['wrapper.cpp'.format(swig_module_name)],
                           include_dirs=['../cpp', '../../src/cpp'],
                           extra_compile_args=extra_compile_args,
                           language='c++17',
                           libraries=['stdc++']
                           )

setup (name = swig_module_name,
       version = '0.2',
       author      = "pierre",
       description = """Simple swig example""",
       ext_modules = [swig_module],
       py_modules = [swig_module_name]
       )
