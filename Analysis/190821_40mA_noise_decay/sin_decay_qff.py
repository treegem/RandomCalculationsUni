import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scopt


def sin(t, T, phi, A, C):
    return A * np.sin(t * 2 * np.pi / T + phi) + C


def main():
    folders = ['50_450_0', '2000_2400_0', '4000_4400_0', '6000_6400_0', '8000_8400_0', '10000_10400_0', '12000_12400_0']
    sin_amplitudes = []
    for i, folder in enumerate(folders):
        start_index = 10
        end_index = -2
        data = np.loadtxt('{}_zs.txt'.format(folder))[start_index:end_index]
        taus = np.loadtxt('{}_taus.txt'.format(folder))[start_index:end_index + 1]
        taus = taus - taus[0]

        # if not i == 4:
        #     continue

        if i == 5:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[120, 1, 0.03, 0.96],
                                      bounds=[[30, -4, 0.005, 0.8], [150, 4, 0.1, 1.]])
        elif i == 4:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[200, 0, 0.05, 0.95],
                                      bounds=[[30, -4, 0.025, 0.8], [300, 4, 0.1, 1.]])
        elif i == 6:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[60, 1, 0.03, 0.96],
                                      bounds=[[30, -4, 0.005, 0.8], [300, 4, 0.1, 1.]])
        else:
            popt, _ = scopt.curve_fit(sin, taus, data, p0=[200, 0, 0.05, 0.95],
                                      bounds=[[30, -4, 0.005, 0.8], [300, 4, 0.1, 1.]])
        sin_amplitudes.append(popt[-2])

        print(popt)
        plt.close('all')
        plt.plot(taus, data)
        plt.plot(taus, sin(taus, *popt))
        # plt.plot(taus, sin(taus, 80, 1, 0.03, 0.96))
        plt.show()

    plt.close('all')
    plt.plot(sin_amplitudes)
    plt.show()
    np.savetxt('sin_decays_qff.txt', sin_amplitudes)


if __name__ == '__main__':
    main()
