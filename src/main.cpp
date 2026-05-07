#include <iostream>
#include "solver.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include <pybind11/functional.h>


std::vector<double> pySolve(FuncType k1, FuncType k2, 
                            FuncType q1, FuncType q2, 
                            FuncType f1, FuncType f2, 
                            double ksi, unsigned n)
{
    Solver solver;
    return solver.SolveBVP(k1, k2, q1, q2, f1, f2, ksi, n);
}

// Create the pybind11 module
PYBIND11_MODULE(boundarysolver, m) {
    m.doc() = "Solves boundary value problem";
    
    m.def("solve_bvp", &pySolve,
        pybind11::arg("k1_func"), pybind11::arg("k2_func"),
        pybind11::arg("q1_func"), pybind11::arg("q2_func"),
        pybind11::arg("f1_func"), pybind11::arg("f2_func"),
        pybind11::arg("ksi"), pybind11::arg("n")
    );
}