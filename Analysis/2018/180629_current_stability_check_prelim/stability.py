import os

import numpy as np

import utility.ds4034_utility as ds
from utility.ds4034_utility import filter_relevant_files, sampling_times, scale_data


def main():
    global ts
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180629_current_stability_check_prelim/current_pulses'
    offset = -0.4  # Volts
    full_points = 2 ** 8  # 8 bit oscilloscope

    ch1_files, info_files = filter_relevant_files(path)

    save_dir = 'stability'
    ensure_save_dir(save_dir)

    traces_stability_txt = 'traces_stability.txt'
    if not stability_file_exists(traces_stability_txt):
        calculate_traces(ch1_files, full_points, info_files, offset, traces_stability_txt)

    print('loading traces')
    traces = np.loadtxt(traces_stability_txt)
    traces_average = np.average(traces, axis=0)
    trace_deviations = np.std(traces, axis=0) / traces_average
    deviation_average = np.average(trace_deviations)

    print(deviation_average)


def stability_file_exists(traces_stability_txt):
    return os.path.isfile(traces_stability_txt)


def ensure_save_dir(save_dir):
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)


def calculate_traces(ch1_files, full_points, info_files, offset, traces_stability_txt):
    global ts
    traces = []
    for i in range(1, len(ch1_files)):
        if i % 20 == 0:
            print('{} / {}'.format(i, len(ch1_files) - 1))
        data = ds.nd_from_file(ch1_files[i])
        data = scale_data(data, full_points, info_files, offset, i)
        ts = sampling_times(data, info_files)

        if i == 1:
            first_index, last_index = outer_indexes_where_data_bigger_than_value(data)

        traces.append(data[first_index:last_index])
    traces = np.array(traces)
    np.savetxt(traces_stability_txt, traces)


def outer_indexes_where_data_bigger_than_value(data):
    indexesWhereDataBiggerThanValue = np.where(data > 0.5)[0]
    first_index = indexesWhereDataBiggerThanValue[0]
    last_index = indexesWhereDataBiggerThanValue[-1]
    return first_index, last_index


if __name__ == '__main__':
    main()
