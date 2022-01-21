# pythonCythonTest

This is a demonstration project for binding C++ with (opaque) STL classes to python using pybind11,
and binding via .pyx wrappers using Cython.    

The project is based on 
1. [Python Bindings: Calling C or C++ From Python](https://realpython.com/python-bindings-overview/#python-bindings-overview).
It is a nice starting point where the ideas are good but the code is incomplete and it does't work.
2. [Cython Tutorial - Bridging between Python and C/C++ for performance gains (YouTube video)](https://www.youtube.com/watch?v=mXuEoqK4bEc)
This does not go into writing c++ but it nicely demonstrates how cython works.

The project is tested on MacOS Catalina (with std=c++17).    

# Compile:
```
invoke build-all
```
# Run:
After successful compilation, run `cython_test.py` and `pybind11_test.py` normally.
