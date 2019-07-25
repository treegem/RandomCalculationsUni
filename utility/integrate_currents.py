import numpy as np


def subtract_baseline(array):
    baseline = np.average([np.average(array[:10]), np.average(array[-10:])])
    return array - baseline


def integrate_current(fname, sweeps, samples_per_sweep, outname):
    osci_data = np.loadtxt(fname) / sweeps
    print(osci_data[0])
    osci_data = subtract_baseline(osci_data)
    window_length = int(len(osci_data) / samples_per_sweep)
    integrated = np.zeros(samples_per_sweep)
    for i in range(samples_per_sweep):
        integrated[i] = np.sum(osci_data[i * window_length: (i + 1) * window_length])
    np.savetxt(outname, integrated)


if __name__ == '__main__':
    integrate_current(
        '//file/e24/Projects/ReinhardLab/data_setup_nv1/190520_sample_N/analogue_027/analogue_data_ch1.txt', 4, 500,
        'test.txt')
