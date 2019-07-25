import matplotlib.pyplot as plt
import numpy as np


def main():
    index = '011'
    fft_data = np.loadtxt('fft_data_pulsed.{}.txt'.format(index))
    fft_freq = np.loadtxt('fft_freq_pulsed.{}.txt'.format(index))
    tau_freqs = np.loadtxt('freqs_pulsed.{}.txt'.format(index))

    gyro = 2.8e6

    bs = tau_freqs / gyro

    plt.close('all')
    plt.plot(fft_freq, fft_data)
    plt.show()

    plt.close('all')
    plt.plot(bs, fft_data)
    plt.show()


if __name__ == '__main__':
    main()
