import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def stretched(t, T2, n, A):
    return A * np.exp(-np.power(t / T2, n))


def main():
    qff = np.loadtxt('decays_qff.txt')
    tau = np.loadtxt('decays_tau.txt')

    qff = qff / max(qff)
    tau = tau / max(tau)

    xs = np.array(list(range(len(qff))))
    xs = xs / xs.max()
    xs *= 60
    popt_qff, _ = curve_fit(stretched, xdata=xs, ydata=qff, p0=[2, 1, 1], bounds=([0, 0, 0.5], [50, 2.5, 1.5]))
    popt_tau, _ = curve_fit(stretched, xdata=xs, ydata=tau, p0=[2, 1, 1], bounds=([0, 0, 0.5], [50, 2.5, 1.5]))

    plt.close('all')
    plt.plot(tau, 'r', label='no_qff, T2={:.1f}, n={:.1f}'.format(*popt_tau))
    plt.plot(stretched(xs, *popt_tau), 'rx')
    plt.plot(qff, 'b', label='qff, T2={:.1f}, n={:.1f}'.format(*popt_qff))
    plt.plot(stretched(xs, *popt_qff), 'bx')
    plt.legend()
    plt.savefig('decays_comparison.jpg', dpi=300)


if __name__ == '__main__':
    main()
