from scipy import optimize as sopt
import numpy as np


def gauss_decay(t, T, f, phi, A, C):
    return np.exp(-np.power(t / T, 2)) * np.sin(2 * np.pi * f * t + phi) * A + C


def fit_parameters(func, signal, taus, p0=None, bounds=(-np.inf, np.inf)):
    fitted_params, rest = sopt.curve_fit(func, taus, signal, p0=p0, bounds=bounds)
    return fitted_params


def linear(x, m, t):
    return x * m + t


if __name__ == '__main__':
    print('testing begins')
    import matplotlib.pyplot as plt

    ts = np.linspace(0, 50, 100)
    ys = linear(ts, 0.01, -3) + (2 * np.random.random(len(ts)) - 1) * 3
    fitted_params = fit_parameters(linear, ys, ts)
    plt.plot(ts, ys)
    plt.plot(ts, linear(ts, *fitted_params))
    plt.show()
    print('testing ended')
