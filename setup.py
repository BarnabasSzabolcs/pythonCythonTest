"""
build: python3 setup.py build_ext --inplace
ref.: https://www.youtube.com/watch?v=mXuEoqK4bEc
"""
from distutils.core import setup
from Cython.Build import cythonize

# currently unused
setup(ext_modules=cythonize('cython_example.pyx'))
