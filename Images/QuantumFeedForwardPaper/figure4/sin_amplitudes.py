import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def sin_func(x, w, A, phi, C):
    return A * np.sin(2 * np.pi * x / w + phi) + C


def main():
    sin_fit_taus()

    sin_fit_zs()


def sin_fit_zs():
    zs_data = np.loadtxt('002_phase_oscillation_5_5000_zs.txt')[5:55]
    xs = np.array(range(len(zs_data)))
    popt, _ = curve_fit(sin_func, xs, zs_data, p0=[7, 0.05, 3, 0.98],
                        bounds=([0.1, 0.001, -4, 0.5], [100, 0.2, 4, 1.5]))
    print(popt)
    plt.close('all')
    plt.plot(xs, zs_data)
    plt.plot(xs, sin_func(xs, *popt))
    # plt.plot(xs, sin_func(xs, 7, 0.05, 3, 0.98))
    plt.show()


def sin_fit_taus():
    tau_data = np.loadtxt('002_phase_oscillation_5_5000_tau_zs.txt')[:50]
    xs = np.array(range(len(tau_data)))
    popt, _ = curve_fit(sin_func, xs, tau_data, p0=[9, 0.1, 2, 1], bounds=([0.1, 0.001, -4, 0.5], [100, 0.2, 4, 1.5]))
    print(popt)
    plt.close('all')
    plt.plot(xs, tau_data)
    plt.plot(xs, sin_func(xs, *popt))
    # plt.plot(xs, sin_func(xs, 9, 0.1, 2, 1))
    plt.show()


if __name__ == '__main__':
    main()
