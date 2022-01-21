#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <iostream>
#include <vector>

namespace py = pybind11;

// This line makes pybind11 work *slower* but it enables to modify python vectors from c++.
// (Usually it is better to make a new vector in c++ and return it to python)
PYBIND11_MAKE_OPAQUE(std::vector<std::string>);

int add(int i, int j) {
    return i + j;
}

std::string greet(const std::string& name) {
    return std::string("Hello, ") + name + std::string("!");
}

void changes(std::vector<std::string>& v) {
    v.push_back("more");
}

PYBIND11_MODULE(example, m) {
    py::bind_vector<std::vector<std::string> >(m, "VectorStr");

    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function which adds two numbers");
    m.def("greet", &greet, "Returns 'Hello!");
    m.def("changes", &changes, "Adds ++ to the end of the string");
}