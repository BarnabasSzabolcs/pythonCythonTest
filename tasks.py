"""
usage:  invoke build-pybind11
"""
import sys

import invoke
from tqdm import tqdm
from invoke import task


@task
def build_pybind11(c):
    if sys.platform == 'darwin':
        extra_flags = "-undefined dynamic_lookup"
    elif sys.platform == 'linux':
        extra_flags = "-fPIC"
    else:
        raise NotImplementedError()

    print("\n*** Compile pybind11 related .cpp files ***\n")
    for module in tqdm(['example', 'demo_package/prio_lexer']):
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
        # --cplus tells that we want c++ code instead of c
        # -3 tells that we want to work with python3
        # it's not really worth the hustle to put the generated c++ file to a separate build directory
        # so we just assign a different c++ extension to generated cpp files so they can be easily cleaned later.
        invoke.run(f"cython --cplus -3 {wrapper}.pyx -o {wrapper}.{generated_cpp_extension}")

    print("\n*** Link the code and the cython wrapper\n")
    for wrapper, codes in [('cython_wrapper', ['cppmult'])]:
        code_libs = ' '.join(f'-l{lib}' for lib in codes)
        invoke.run(
            f"c++ -O3 -Wall -shared -std=c++17 "
            f"{extra_flags} "
            f"`python3 -m pybind11 --includes` " 
            f"{wrapper}.{generated_cpp_extension} "
            f"-o {wrapper}`python3-config --extension-suffix` "
            f"-L. {code_libs}"
        )


@task(build_pybind11, build_cython)
def build_all(c):
    """
    builds everything
    """
