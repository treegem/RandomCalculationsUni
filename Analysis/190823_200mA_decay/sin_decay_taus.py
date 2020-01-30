import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scopt


def sin(t, T, phi, A, C):
    return A * np.sin(t * 2 * np.pi / T + phi) + C


def main():
    folders =  ['50_150_0', '300_400_0', '600_700_0', '900_1000_0', '1200_1300_0', '1500_1600_0', '1800_1900_0',
               '2100_2200_0', '2400_2500_0', '2700_2800_0', '3000_3100_0']
    sin_amplitudes = []
    for i, folder in enumerate(folders):
        start_index = 10
        end_index = -5
        data = np.loadtxt('{}_tau_zs.txt'.format(folder))[start_index:end_index]
        taus = np.loadtxt('{}_taus.txt'.format(folder))[start_index:end_index]

        taus = taus - taus[0]

        if False:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[50, 0, 0.02, 0.88],
                                      bounds=[[30, -6, 0.005, 0.7], [80, 6, 0.1, 1.]])
        else:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[30, 0, 0.05, 0.95],
                                      bounds=[[10, -4, 0.005, 0.8], [50, 4, 0.1, 1.1]])
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
