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

std::vector<double> pySolveMixedTestFunction(FuncType k1_, FuncType k2_, 
                                     FuncType q1_, FuncType q2_, 
                                     FuncType f1_, FuncType f2_, 
                                     double ksi_, unsigned n,
                                     double gamma_1_, double gamma_2_,
                                     double theta_1_, double theta_2_) 
{
    Solver solver;
    return solver.SolveBVPMixedTestFunction(k1_, k2_, q1_, q2_, f1_, f2_, ksi_, n, gamma_1_, gamma_2_, theta_1_, theta_2_);
    return solver.SolveBVPMixedTestFunction(k1_, k2_, q1_, q2_, f1_, f2_, ksi_, n, gamma_1_, gamma_2_, theta_1_, theta_2_);
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

        m.def("solve_bvp_mixed_test_function", &pySolveMixedTestFunction,
        pybind11::arg("k1_func"), pybind11::arg("k2_func"),
        pybind11::arg("q1_func"), pybind11::arg("q2_func"),
        pybind11::arg("f1_func"), pybind11::arg("f2_func"),
        pybind11::arg("ksi"), pybind11::arg("n"),
        pybind11::arg("gamma_1_"), pybind11::arg("gamma_2_"),
        pybind11::arg("theta_1_"), pybind11::arg("theta_2_")
    );
}