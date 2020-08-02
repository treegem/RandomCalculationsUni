import matplotlib.pyplot as plt
import numpy as np

import utility.tum_jet as tum_jet
from utility.imperial_to_metric import cm_to_inch


def sensitivity(n):
    return np.sqrt(n) / np.sinc(1 / n)  # the sinc function automatically multiplies pi to the argument


if __name__ == '__main__':
    ns_continuous = np.linspace(1.8, 8.2, 150)
    ns_discrete = np.arange(2, 8.1, 2)

    fig = plt.figure(figsize=(cm_to_inch(1.0 * 8.6), cm_to_inch(7)))
    plt.plot(ns_continuous, sensitivity(ns_continuous) / sensitivity(ns_continuous).min(), '--',
             color=tum_jet.tum_color(0))
    plt.plot(ns_discrete, sensitivity(ns_discrete) / sensitivity(ns_continuous).min(), 'o', color=tum_jet.tum_color(0))
    plt.xlabel('number of sectors')
    plt.ylabel('sensitivity (arb. u.)')
    plt.tight_layout()
    plt.savefig('sensitivity_vs_sectors.png', dpi=500)
