import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from utility.tum_jet import tum_color


def stretched(t, T2, n, A, cons):
    return A * np.exp(-np.power(t / T2, n)) + cons


def main():
    qff = np.loadtxt('sin_decays_qff.txt')
    tau = np.loadtxt('sin_decays_taus.txt')

    # tau_min = 50
    # tau_max = 25000

    # qff = qff / qff[0]
    # tau = tau / tau[0]

    xs = list(range(len(qff)))
    popt_qff, _ = curve_fit(stretched, xdata=xs, ydata=qff, p0=[1, 1.75, 1, 0],
                            bounds=[[0, 1.0, 0, 0], [15, 2., 1.2, 0.005]])
    popt_tau, _ = curve_fit(stretched, xdata=xs, ydata=tau, p0=[1, 1.6, 1, 0],
                            bounds=[[0, 1.0, 0, 0], [15, 2., 1.2, 0.005]])

    plt.close('all')
    plt.plot(tau, label='no_qff, T2={:.1f}, n={:.1f}'.format(*popt_tau), color=tum_color(5))
    plt.plot(stretched(xs, *popt_tau), '.', color=tum_color(5))
    plt.plot(qff, label='qff, T2={:.1f}, n={:.1f}'.format(*popt_qff), color=tum_color(0))
    plt.plot(stretched(xs, *popt_qff), '.', color=tum_color(0))
    plt.legend()
    plt.savefig('sin_decays_comparison.jpg', dpi=300)


if __name__ == '__main__':
    main()
