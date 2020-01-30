import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def fit_func(t, T, A):
    return A * np.sin(2 * np.pi * t / 1.09363845e-08 + 2.28997972e-01) * np.exp(-(t / T)**2) + 0.5


def main():
    zs = load_zs()[:-20]
    taus = np.linspace(10e-9, 500e-9, len(zs))

    p0 = [1.5e-6, 0.15]
    popt, pcov = curve_fit(fit_func, taus, zs, p0=p0, bounds=([0.7e-6, 0.1], [20e-6, 0.2]))
    perr = np.sqrt(np.diag(pcov))

    print(popt)
    print('T2: {:e}'.format(popt[0]))
    print('dT2: {:e}'.format(perr[0]))

    plt.plot(taus, zs)
    plt.plot(taus, fit_func(taus, *popt), '.')
    plt.show()


def load_zs():
    zs = np.loadtxt('fast_zs.txt')
    return zs


if __name__ == '__main__':
    main()
