import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scopt


def sin(t, T, phi, A, C):
    return A * np.sin(t * 2 * np.pi / T + phi) + C


def main():
    folders = ['50_250_0', '1000_1200_0', '2000_2200_0', '3000_3200_0', '4000_4200_0', '5000_5200_0', '6000_6200_0']
    sin_amplitudes = []
    for i, folder in enumerate(folders):
        start_index = 10
        end_index = -10
        data = np.loadtxt('{}_zs.txt'.format(folder))[start_index:end_index]
        taus = np.loadtxt('{}_taus.txt'.format(folder))[start_index:end_index + 1]
        taus = taus - taus[0]

        # if not i == 2:
        #     continue

        if False:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[53, 0, 0.04, 0.96],
                                      bounds=[[30, -4, 0.005, 0.8], [70, 4, 0.1, 1.]], )
        else:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[60, 0, 0.04, 0.95],
                                      bounds=[[30, -4, 0.005, 0.8], [160, 4, 0.1, 1.]])
        sin_amplitudes.append(popt[-2])

        print(popt)
        plt.close('all')
        plt.plot(taus, data)
        plt.plot(taus, sin(taus, *popt))
        # plt.plot(taus, sin(taus, 53, 0, 0.04, 0.96))
        plt.show()

    plt.close('all')
    plt.plot(sin_amplitudes)
    plt.show()
    np.savetxt('sin_decays_qff.txt', sin_amplitudes)


if __name__ == '__main__':
    main()
