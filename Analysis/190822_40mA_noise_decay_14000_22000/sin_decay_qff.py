import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scopt


def sin(t, T, phi, A, C):
    return A * np.sin(t * 2 * np.pi / T + phi) + C


def main():
    folders = ['14000_14400', '16000_16400', '18000_18400', '20000_20400', '22000_22400']
    sin_amplitudes = []
    for i, folder in enumerate(folders):
        start_index = 10
        end_index = -2
        data = np.loadtxt('{}_zs.txt'.format(folder))[start_index:end_index]
        taus = np.loadtxt('{}_taus.txt'.format(folder))[start_index:end_index + 1]
        taus = taus - taus[0]

        # if not i == 3:
        #     continue

        if i == 3:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[110, 0, 0.02, 0.92],
                                      bounds=[[30, -4, 0.005, 0.8], [150, 4, 0.1, 1.]])
        else:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[80, 0, 0.02, 0.91],
                                      bounds=[[30, -4, 0.005, 0.8], [300, 4, 0.1, 1.]])
        sin_amplitudes.append(popt[-2])

        print(popt)
        plt.close('all')
        plt.plot(taus, data)
        plt.plot(taus, sin(taus, *popt))
        # plt.plot(taus, sin(taus, 110, 0, 0.02, 0.92))
        plt.show()

    plt.close('all')
    plt.plot(sin_amplitudes)
    plt.show()
    np.savetxt('sin_decays_qff.txt', sin_amplitudes)


if __name__ == '__main__':
    main()
