#pragma once
#include <vector>
#include <tuple>
#include <functional>

#define M_PI 3.14159

using FuncType = std::function<double(double)>;

class Solver final
{
public:
    Solver() {}

private:
    // Input
    double h = 1.0;

    // Main task, var 4
    double ksi = 0.5;
    double mu1 = 0.0;
    double mu2 = 0.0;

    FuncType k1, k2, q1, q2, f1, f2;

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
    std::vector<double> SolveBVP(   FuncType k1_, FuncType k2_, 
                                    FuncType q1_, FuncType q2_, 
                                    FuncType f1_, FuncType f2_, 
                                    double ksi_, unsigned n);

};