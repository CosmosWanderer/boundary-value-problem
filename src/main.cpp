#include <iostream>
#include "solver.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

// Create the pybind11 module
PYBIND11_MODULE(splinesolver, m) {
    m.doc() = "Solves boundary value problem";
    
    m.def("solve_bvp", &Solver::SolveBVP,
        pybind11::arg("n")    
    );
}

int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}