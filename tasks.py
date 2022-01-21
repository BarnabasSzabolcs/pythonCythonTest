"""
usage:  invoke build-pybind11
"""
import sys

import invoke
from invoke import task


@task
def build_pybind11(c):
    if sys.platform == 'darwin':
        extra_flags = "-undefined dynamic_lookup"
    elif sys.platform == 'linux':
        extra_flags = "-fPIC"
    else:
        raise NotImplementedError()

    for module in ['example', 'demo_package/prio_lexer']:
        invoke.run(
            f"c++ -O3 -Wall -shared -std=c++17 "
            f"{extra_flags} "
            f"`python3 -m pybind11 --includes` " 
            f"{module}.cpp "
            f"-o {module}`python3-config --extension-suffix`"
        )


@task
def build_cython(c):
    generated_cpp_extension = 'cxx'

    if sys.platform == 'darwin':
        extra_flags = "-undefined dynamic_lookup"
    elif sys.platform == 'linux':
        extra_flags = "-fPIC"
    else:
        raise NotImplementedError()

    print("\n*** compile code ***\n")
    for code in ['cppmult']:
        invoke.run(
            f"g++ -O3 -Wall -Werror -shared -std=c++17 {extra_flags} {code}.cpp "
            f"-o lib{code}.so "
        )

    print("\n*** Run cython on the pyx file to create a .cpp file ***\n")
    for wrapper in ['cython_wrapper']:
        invoke.run(f"cython --cplus -3 {wrapper}.pyx -o {wrapper}.{generated_cpp_extension}")

    print("\n*** Link the code and the cython wrapper\n")
    for wrapper, code in [('cython_wrapper', 'cppmult')]:
        invoke.run(
            f"c++ -O3 -Wall -shared -std=c++17 "
            f"{extra_flags} "
            f"`python3 -m pybind11 --includes` " 
            f"{wrapper}.{generated_cpp_extension} "
            f"-o {wrapper}`python3-config --extension-suffix` "
            f"-L. -l{code}"
        )


@task(build_pybind11, build_cython)
def all(c):
    """
    builds everything
    """
