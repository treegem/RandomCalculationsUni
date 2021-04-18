import matplotlib.pyplot as plt
import numpy as np


def main():
    taus = np.loadtxt('freqs_interp_currents.txt')
    data = np.loadtxt('fft_interp_currents.txt', dtype=str)
    converted = np.zeros_like(data, dtype=np.float)
    for i, point in enumerate(data):
        replaced = point.replace('+-', '-')
        converted[i] = np.abs(complex(replaced))
    plt.plot(taus, converted)
    plt.show()


if __name__ == '__main__':
    main()
