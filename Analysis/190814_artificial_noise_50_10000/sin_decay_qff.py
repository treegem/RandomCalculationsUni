import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scopt


def sin(t, T, phi, A, C):
    return A * np.sin(t * 2 * np.pi / T + phi) + C


def main():
    folders = ['50_250_0', '2000_2200_0', '4000_4200_0', '6000_6200_0', '8000_8200_0', '10000_10200_0']
    sin_amplitudes = []
    for i, folder in enumerate(folders):
        start_index = 5
        end_index = -18
        data = np.loadtxt('{}_zs.txt'.format(folder))[start_index:end_index]
        taus = np.loadtxt('{}_taus.txt'.format(folder))[start_index:end_index + 1]

        # if not i == 5:
        #     continue

        if i == 0:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[50, 0, 0.04, 0.95],
                                      bounds=[[30, -6, 0.005, 0.8], [70, 6, 0.1, 1.]])
        elif i == 2:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[40, -1, 0.01, 0.935],
                                      bounds=[[30, -6, 0.005, 0.8], [70, 6, 0.1, 1.]])
        elif i == 3:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[40, -1, 0.01, 0.95],
                                      bounds=[[30, -6, 0.005, 0.8], [70, 6, 0.1, 1.]])
        elif i == 4:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[40, -2, 0.02, 0.93],
                                      bounds=[[30, -6, 0.005, 0.8], [70, 6, 0.1, 1.]])
        elif i == 5:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[40, 0, 0.015, 0.945],
                                      bounds=[[30, -6, 0.005, 0.8], [70, 6, 0.1, 1.]])
        else:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[50, 0, 0.04, 0.95],
                                      bounds=[[20, -4, 0.005, 0.8], [60, 4, 0.1, 1.]])
        sin_amplitudes.append(popt[-2])

        print(popt)
        plt.close('all')
        plt.plot(taus, data)
        plt.plot(taus, sin(taus, *popt))
        # plt.plot(taus, sin(taus, 40, 0, 0.015, 0.945))
        plt.show()

    plt.close('all')
    plt.plot(sin_amplitudes)
    plt.show()
    np.savetxt('sin_decays_qff.txt', sin_amplitudes)


if __name__ == '__main__':
    main()
