import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from utility.tum_jet import tum_color


def stretched(t, T2, n, A, const):
    return A * np.exp(-np.power(t / T2, n)) + const


def main():
    qff = np.loadtxt('decays_qff.txt')
    tau = np.loadtxt('decays_tau.txt')

    qff = qff / qff[0]
    tau = tau / tau[0]

    xs = list(range(len(qff)))
    popt_qff, _ = curve_fit(stretched, xdata=xs, ydata=qff, p0=[1, 1.5, 1, 0], bounds=[[0, 1., 0.8, -0.2], [2, 2., 1.2, 0.2]])
    popt_tau, _ = curve_fit(stretched, xdata=xs, ydata=tau, p0=[1, 1.5, 1, 0], bounds=[[0, 1., 0.8, -0.2], [2, 2., 1.2, 0.2]])

    plt.close('all')
    plt.plot(tau, label='no_qff, T2={:.1f}, n={:.1f}'.format(*popt_tau), color=tum_color(5))
    plt.plot(stretched(xs, *popt_tau), '.', color=tum_color(5))
    plt.plot(qff, label='qff, T2={:.1f}, n={:.1f}'.format(*popt_qff), color=tum_color(0))
    plt.plot(stretched(xs, *popt_qff), '.', color=tum_color(0))
    plt.legend()
    plt.savefig('decays_comparison.jpg', dpi=300)


if __name__ == '__main__':
    main()
