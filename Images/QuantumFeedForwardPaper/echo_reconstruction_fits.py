import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def fit_func(x, T, C, A, n):
    return A * np.exp(-(x / T) ** n) + C


def main():
    filtered = load_filtered_results()
    pure = np.loadtxt('pure.txt')
    regular = np.loadtxt('regular.txt')
    taus = np.loadtxt('x_taus.txt')

    popt_filtered, pcov_filtered = curve_fit(fit_func, taus, filtered, bounds=([0, 0, 0, 1], [500, 1, 1, 2]))
    popt_pure, pcov_pure = curve_fit(fit_func, taus, pure, bounds=([0, 0, 0, 1], [500, 1, 1, 2]))
    popt_regular, pcov_regular = curve_fit(fit_func, taus, regular, bounds=([0, 0, 0, 1], [500, 1, 1, 1.1]))

    make_plots(filtered, pure, regular, taus, popt_filtered, popt_pure, popt_regular)

    print('pure: ', popt_pure[0], np.sqrt(pcov_filtered[0, 0]))
    print('regular: ', popt_regular[0], np.sqrt(pcov_regular[0, 0]))
    print('filtered: ', popt_filtered[0], np.sqrt(pcov_filtered[0, 0]))


def make_plots(filtered, pure, regular, taus, popt_filtered, popt_pure, popt_regular):
    plt.close('all')
    plt.plot(taus, pure, 'b.')
    plt.plot(taus, regular, 'r.')
    plt.plot(taus, filtered, 'g.')
    plt.plot(taus, fit_func(taus, *popt_pure), 'b')
    plt.plot(taus, fit_func(taus, *popt_regular), 'r')
    plt.plot(taus, fit_func(taus, *popt_filtered), 'g')
    plt.show()


def load_filtered_results():
    xs = np.loadtxt('x.txt')
    ys = np.loadtxt('y.txt')
    filtered = np.zeros_like(xs)
    for i, x in enumerate(xs):
        if i == 0:
            filtered[i] = x
            continue
        filtered[i] = np.average([x, ys[i - 1]])
    return filtered


if __name__ == '__main__':
    main()
