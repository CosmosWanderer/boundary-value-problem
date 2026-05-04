#pragma once
#include <vector>
#include <tuple>

class Solver final
{
private:
    Solver() {}

    // Input
    double h = 1.0;

    // Main task, var 4
    double ksi = 0.5;
    double mu1 = 0.0;
    double mu2 = 0.0;

    double k1(double x);
    double k2(double x);
    double q1(double x);
    double q2(double x);
    double f1(double x);
    double f2(double x);

    // Get coords
    double get_x(unsigned i);
    double get_half_step_plus(unsigned i);
    double get_half_step_minus(unsigned i);

    // Rectangle method
    double find_a_rect(unsigned i);
    double find_d_rect(unsigned i);
    double find_phi_rect(unsigned i);

    // Get parameters for tridiagonal matrix algorithm
    double get_A(unsigned i);
    double get_B(unsigned i);
    double get_C(unsigned i);

public:
    std::vector<double> SolveBVP(unsigned n);

};