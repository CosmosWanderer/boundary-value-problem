#include "solver.h"
#include <cmath>
#include <numbers>

// Get coords
double Solver::get_x(unsigned i) {
    return i * h;
}
double Solver::get_half_step_minus(unsigned i) {
    return (i - 0.5) * h; 
}
double Solver::get_half_step_plus(unsigned i) {
    return (i + 0.5) * h; 
}
  
// Rectangle method
double Solver::find_a_rect(unsigned i) {
    if (get_x(i) <= ksi) {
        return k1(get_half_step_minus(i));
    }
    if (get_x(i - 1) >= ksi) {
        return k2(get_half_step_minus(i));
    }
    
    double sl1 = (ksi - get_x(i-1)) / (k1((get_x(i-1) + ksi) / 2));
    double sl2 = (get_x(i) - ksi) / (k2((get_x(i) + ksi) / 2));
    return h / (sl1 + sl2);

}
double Solver::find_d_rect(unsigned i) {
    if (ksi >= get_half_step_plus(i)) {
        double x = get_x(i);
        if (i == 0)
            x = 0.25 * h;
        return q1(x);
    }
    if (ksi <= get_half_step_minus(i)) {
        double x = get_x(i);
        if (i == n)
            x = h * (static_cast<double>(n) - 0.25);
        return q2(x);
    }

    double sl1 = (1 / h) * q1((ksi + get_half_step_minus(i)) / 2) * (ksi - get_half_step_minus(i));
    double sl2 = (1 / h) * q2((get_half_step_plus(i) + ksi) / 2) * (get_half_step_plus(i) - ksi);
    return sl1 + sl2;
} 
double Solver::find_phi_rect(unsigned i) {
    if (ksi >= get_half_step_plus(i)) {
        double x = get_x(i);
        if (i == 0)
            x = 0.25 * h;
        return f1(x);
    }
    if (ksi <= get_half_step_minus(i)) {
        double x = get_x(i);
        if (i == n)
            x = 1 - 0.25 * h;
        return f2(x);
    }

    double sl1 = (1 / h) * f1((ksi + get_half_step_minus(i)) / 2) * (ksi - get_half_step_minus(i));
    double sl2 = (1 / h) * f2((get_half_step_plus(i) + ksi) / 2) * (get_half_step_plus(i) - ksi);
    return sl1 + sl2;
}

// Get parameters for tridiagonal matrix algorithm
double Solver::get_A(unsigned i) {
    return find_a_rect(i) / (h * h);
}
double Solver::get_B(unsigned i) {
    return find_a_rect(i + 1) / (h * h);
}
double Solver::get_C(unsigned i) {
    return (find_a_rect(i) + find_a_rect(i + 1)) / (h * h) + find_d_rect(i);
}


std::vector<double> Solver::SolveBVP(FuncType k1_, FuncType k2_, 
                                     FuncType q1_, FuncType q2_, 
                                     FuncType f1_, FuncType f2_, 
                                     double ksi_, double mu1, double mu2,
                                     unsigned n_) 
{
    k1 = k1_;
    k2 = k2_;
    q1 = q1_;
    q2 = q2_;
    f1 = f1_;
    f2 = f2_;
    
    ksi = ksi_;

    n = n_;
    h = 1.0 / n;
    std::vector<double> V(n + 1);

    V[0] = mu1;
    V[n] = mu2;

    std::vector<double> alpha(n + 1);
    alpha[1] = 0;
    std::vector<double> beta(n + 1);
    beta[1] = mu1;

    // Forward pass
    for (int i = 2; i <= n; i++) {
        alpha[i] = get_B(i - 1) / (get_C(i - 1) - alpha[i - 1] * get_A(i - 1));
        beta[i] = (find_phi_rect(i - 1) + get_A(i - 1) * beta[i - 1]) / (get_C(i - 1) - alpha[i - 1] * get_A(i - 1));
    }

    // Backward pass
    for (int i = n - 1; i > 0; i--) {
        V[i] = alpha[i + 1] * V[i + 1] + beta[i + 1];
    }

    return V;
}

std::vector<double> Solver::SolveBVPMixedTestFunction(FuncType k1_, FuncType k2_, 
                                     FuncType q1_, FuncType q2_, 
                                     FuncType f1_, FuncType f2_, 
                                     double ksi_, unsigned n_,
                                     double gamma_1_, double gamma_2_,
                                     double theta_1_, double theta_2_) 
{
    k1 = k1_;
    k2 = k2_;
    q1 = q1_;
    q2 = q2_;
    f1 = f1_;
    f2 = f2_;
    gamma_1 = gamma_1_;
    gamma_2 = gamma_2_;
    theta_1 = theta_1_;
    theta_2 = theta_2_;
    
    ksi = ksi_;
    n = n_;
    h = 1.0 / n;
    std::vector<double> V(n + 1);

    double kappa_1 = k1(0.0) / (h * (gamma_1 + k1(0.0) * 1 / h));
    double kappa_2 = k2(1.0) / (h * (gamma_2 + k2(1.0) * 1 / h));
    double mu1 = gamma_1 * theta_1 / (gamma_1 + k1(0.0) * 1 / h);
    double mu2 = gamma_2 * theta_2 / (gamma_2 + k2(1.0) * 1 / h);

    std::vector<double> alpha(n + 1);
    alpha[1] = kappa_1;
    std::vector<double> beta(n + 1);
    beta[1] = mu1;

    // Forward pass
    for (int i = 2; i <= n; i++) {
        alpha[i] = get_B(i - 1) / (get_C(i - 1) - alpha[i - 1] * get_A(i - 1));
        beta[i] = (find_phi_rect(i - 1) + get_A(i - 1) * beta[i - 1]) / (get_C(i - 1) - alpha[i - 1] * get_A(i - 1));
    }

    V[n] = (mu2 + kappa_2 * beta[n]) / (1 - alpha[n] * kappa_2);

    // Backward pass
    for (int i = n - 1; i >= 0; i--) {
        V[i] = alpha[i + 1] * V[i + 1] + beta[i + 1];
    }

    return V;
}

std::vector<double> Solver::SolveBVPMixedAdvancedApproximation( FuncType k1_, FuncType k2_, 
                                                                FuncType q1_, FuncType q2_, 
                                                                FuncType f1_, FuncType f2_, 
                                                                double ksi_, unsigned n_,
                                                                double gamma_1_, double gamma_2_,
                                                                double theta_1_, double theta_2_) 
{
    k1 = k1_;
    k2 = k2_;
    q1 = q1_;
    q2 = q2_;
    f1 = f1_;
    f2 = f2_;
    gamma_1 = gamma_1_;
    gamma_2 = gamma_2_;
    theta_1 = theta_1_;
    theta_2 = theta_2_;
    
    ksi = ksi_;
    n = n_;
    h = 1.0 / n;
    std::vector<double> V(n + 1);

    double a_1 = find_a_rect(1);
    double a_n = find_a_rect(n);
    double kappa_1 = a_1 / (a_1 + h * gamma_1 + h * h * 0.5 * find_d_rect(0));
    double kappa_2 = a_n / (a_n + h * gamma_2 + h * h * 0.5 * find_d_rect(n));
    double mu1 = (gamma_1 * theta_1 + h * 0.5 * find_phi_rect(0)) / (find_a_rect(1) / h + gamma_1 + h * 0.5 * find_d_rect(0));
    double mu2 = (gamma_2 * theta_2 + h * 0.5 * find_phi_rect(n)) / (find_a_rect(n) / h + gamma_2 + h * 0.5 * find_d_rect(n));

    std::vector<double> alpha(n + 1);
    alpha[1] = kappa_1;
    std::vector<double> beta(n + 1);
    beta[1] = mu1;

    // Forward pass
    for (int i = 2; i <= n; i++) {
        alpha[i] = get_B(i - 1) / (get_C(i - 1) - alpha[i - 1] * get_A(i - 1));
        beta[i] = (find_phi_rect(i - 1) + get_A(i - 1) * beta[i - 1]) / (get_C(i - 1) - alpha[i - 1] * get_A(i - 1));
    }

    V[n] = (mu2 + kappa_2 * beta[n]) / (1 - alpha[n] * kappa_2);

    // Backward pass
    for (int i = n - 1; i >= 0; i--) {
        V[i] = alpha[i + 1] * V[i + 1] + beta[i + 1];
    }

    return V;
}
