import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def fit_function(t, T, A, off, phi):
    return A * np.sin(t * 2 * np.pi / T + phi) + off


def main():
    slow_zs = np.loadtxt('slow_zs.txt')
    taus = np.linspace(10e-9, 500e-9, len(slow_zs))

    popt, pcov = curve_fit(fit_function, taus, slow_zs, p0=[2e-7, 0.15, 0.5, 0])
    perr = np.sqrt(np.diag(pcov))

    plt.plot(taus, slow_zs)
    plt.plot(taus, fit_function(taus, *popt))
    plt.show()

    fitted_T, relative_err_T = calculate_relative_err_t(perr, popt)

    current_amplitude = 3.5e-3
    delta0 = 2 * np.pi / current_amplitude / fitted_T
    err_delta = relative_err_T * delta0

    print('delta 0: {:e}'.format(delta0))
    print('err_delta: {:e}'.format(err_delta))


def calculate_relative_err_t(perr, popt):
    fitted_T = popt[0]
    err_T = perr[0]
    relative_err_T = err_T / fitted_T
    return fitted_T, relative_err_T


if __name__ == '__main__':
    main()
