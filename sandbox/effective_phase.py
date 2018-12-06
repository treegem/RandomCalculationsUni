import numpy as np
import matplotlib.pyplot as plt


def main():
    mus = np.linspace(0, 0.9, 100)
    eff_phases = effective_phase(mus)
    plt.plot(mus, eff_phases)
    plt.show()


def effective_phase(mu):
    phase = 1
    arccos = 1
    try:
        arccos = np.arccos(np.cos(phase) / np.sqrt(1 - np.square(mu)))
    except RuntimeWarning as e:
        print('haha')
    return arccos


if __name__ == '__main__':
    main()
