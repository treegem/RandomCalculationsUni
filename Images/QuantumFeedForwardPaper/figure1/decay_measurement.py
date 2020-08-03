import matplotlib.pyplot as plt
import numpy as np

import utility.tum_jet as tum_jet
from utility.imperial_to_metric import cm_to_inch


def main():
    xs = np.linspace(0, 1, 200)
    plt.figure(figsize=(cm_to_inch(1 * 8.6), cm_to_inch(4.2)))
    plt.plot(xs, gaussian_decay(xs, .1) / 2 + 0.5, label='uncorrected', color=tum_jet.tum_color(0))
    plt.plot(xs, gaussian_decay(xs, 0.5) * lorentzian_decay(xs) / 2 + 0.5, label='corrected',
             color=tum_jet.tum_color(5))
    plt.xlabel(r'$\tau$ (arb. u.)')
    plt.ylabel(r'$\left\langle S_z \right\rangle$')
    plt.legend()
    plt.tight_layout(pad=0.5)
    plt.savefig('decays_with_and_without_correction.png', dpi=500)


def gaussian_decay(x, t2):
    return np.exp(-(x / t2) ** 2)


def lorentzian_decay(x):
    return 1 - 1 / (1 + 2000 * (x - 0.4) ** 2)


if __name__ == '__main__':
    main()
