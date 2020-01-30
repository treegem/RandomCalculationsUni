import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scopt


def sin(t, T, phi, A, C):
    return A * np.sin(t * 2 * np.pi / T + phi) + C


def main():
    folders = ['50_250_0', '2000_2200_0', '4000_4200_0', '6000_6200_0', '8000_8200_0', '10000_10200_0']
    sin_amplitudes = []
    for i, folder in enumerate(folders):
        start_index = 10
        end_index = -5
        data = np.loadtxt('{}_tau_zs.txt'.format(folder))[start_index:end_index]
        taus = np.loadtxt('{}_taus.txt'.format(folder))[start_index:end_index]

        if i == 0:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[50, 0, 0.02, 0.88],
                                      bounds=[[30, -6, 0.005, 0.7], [70, 6, 0.1, 1.]])
        else:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[35, 0, 0.02, 0.88],
                                      bounds=[[20, -10, 0.005, 0.7], [60, 10, 0.1, 1.]])
        sin_amplitudes.append(popt[-2])

        print(popt)
        plt.close('all')
        plt.plot(taus, data)
        plt.plot(taus, sin(taus, *popt))
        # plt.plot(taus, sin(taus, 50, 0, 0.02, 0.88))
        plt.show()

    plt.close('all')
    plt.plot(sin_amplitudes)
    plt.show()
    np.savetxt('sin_decays_taus.txt', sin_amplitudes)


if __name__ == '__main__':
    main()
