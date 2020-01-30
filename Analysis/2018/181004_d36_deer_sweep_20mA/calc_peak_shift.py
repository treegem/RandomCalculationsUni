import matplotlib.pyplot as plt
import numpy as np


def main():
    peaks_noc = np.loadtxt('no_current_peaks.txt')
    peaks_20ma = np.loadtxt('20mA_current_peaks.txt')
    difference = (peaks_noc - peaks_20ma) * -1
    plt.plot(range(1, len(difference) + 1), difference * 1e-6, '.')
    plt.plot([1, 13], [-2.8, -2.8], 'r--')
    plt.plot([1, 13], [2.8, 2.8], 'r--')
    plt.axes().set_aspect(0.5)
    plt.xlabel('#peak')
    plt.ylabel(r'$f_{20mA} - f_0$' + ' (MHz)')
    plt.savefig('peak_shifts.png', dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    main()
