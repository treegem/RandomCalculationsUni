import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scopt


def sin(t, T, phi, A, C):
    return A * np.sin(t * 2 * np.pi / T + phi) + C


def main():
    folders = ['50_250_0', '5000_5200_0', '10000_10200_0', '15000_15200_0', '20000_20200_0', '25000_25200_0']
    sin_amplitudes = []
    for i, folder in enumerate(folders):
        start_index = 10
        end_index = -5
        data = np.loadtxt('{}_zs.txt'.format(folder))[start_index:end_index]
        taus = np.loadtxt('{}_taus.txt'.format(folder))[start_index:end_index + 1]

        if i == 0:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[50, 0, 0.02, 0.95],
                                      bounds=[[30, -6, 0.005, 0.8], [70, 6, 0.1, 1.]])
        else:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[35, 0, 0.02, 0.95],
                                      bounds=[[20, -10, 0.005, 0.8], [60, 10, 0.1, 1.]])
        sin_amplitudes.append(popt[-2])

        print(popt)
        plt.close('all')
        plt.plot(taus, data)
        plt.plot(taus, sin(taus, *popt))
        plt.show()

    plt.close('all')
    plt.plot(sin_amplitudes)
    plt.show()
    np.savetxt('sin_decays_qff.txt', sin_amplitudes)


if __name__ == '__main__':
    main()
