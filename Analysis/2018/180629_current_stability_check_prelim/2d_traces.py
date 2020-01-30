import os

import numpy as np
import matplotlib.pyplot as plt

import utility.ds4034_utility as ds
from utility.ds4034_utility import filter_relevant_files, sampling_times, scale_data


def main():
    global ts
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180629_current_stability_check_prelim/current_pulses'
    offset = -0.4  # Volts
    full_points = 2 ** 8  # 8 bit oscilloscope

    ch1_files, info_files = filter_relevant_files(path)
    save_dir = 'single_traces'

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    traces = []

    for i in range(1, len(ch1_files)):
        if i % 20 == 0:
            print('{} / {}'.format(i, len(ch1_files) - 1))
        data = ds.nd_from_file(ch1_files[i])
        data = scale_data(data, full_points, info_files, offset, i)
        ts = sampling_times(data, info_files)

        traces.append(data)

        plt.close('all')
        plt.plot(ts * 1e9, data)
        plt.savefig('{}/trace_{}.png'.format(save_dir, i), dpi=300)

    traces = np.array(traces)
    np.savetxt('traces.txt', traces)

    plt.close('all')
    plt.imshow(traces)
    plt.savefig('2dtraces.png', dpi=300)


if __name__ == '__main__':
    main()
