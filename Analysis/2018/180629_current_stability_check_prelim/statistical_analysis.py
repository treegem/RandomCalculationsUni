import numpy as np
import matplotlib.pyplot as plt
import utility.ds4034_utility as ds


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180629_current_stability_check_prelim/current_pulses'
    traces = np.loadtxt('traces.txt')
    avg = np.average(traces, axis=0)
    ts = get_taus(path)
    time_steps = ts[1] - ts[0]

    integrated_traces = integrate_traces(time_steps, traces)
    too_low = []
    for i, trace in enumerate(integrated_traces):
        if trace < 300e-9:
            too_low.append(i)
    too_low = np.array(too_low)
    np.savetxt('too_low.txt', too_low)
    average_integral = np.average(integrated_traces)
    standard_deviation = integral_standard_deviation(average_integral, integrated_traces)

    plt.close('all')
    plt.plot(integrated_traces * 1e9)
    plt.plot([0, len(integrated_traces)], [average_integral * 1e9, average_integral * 1e9], 'r--')
    plt.xlabel('traces')
    plt.ylabel('integral area (nVs)')
    sigma_string = 'sigma: {:.2f} nVs'.format(standard_deviation * 1e9)
    y_extent = integrated_traces.max() - integrated_traces.min()
    lowest = integrated_traces.min()
    plt.text(0.05 * len(integrated_traces), (lowest + 0.9 * y_extent) * 1e9, sigma_string)
    plt.savefig('integral_deviation.png', dpi=300)

    deviations = compute_deviations(avg, traces)
    plot_deviations_2d(deviations, ts)


def integral_standard_deviation(average_integral, integrated_traces):
    integral_deviations = average_integral - integrated_traces
    integral_deviations = np.square(integral_deviations)
    standard_deviation = np.sqrt(integral_deviations.sum()) / len(integral_deviations)
    return standard_deviation


def plot_deviations_2d(deviations, ts):
    plt.close('all')
    plt.imshow(deviations, aspect='auto', extent=[ts[0] * 1e9, ts[-1] * 1e9, 0, len(deviations)])
    plt.colorbar()
    plt.savefig('deviations.png')


def integrate_traces(time_steps, traces):
    integrals = []
    for trace in traces:
        summed_trace = trace.sum()
        integrated_trace = summed_trace * time_steps
        integrals.append(integrated_trace)
    integrals = np.array(integrals)
    return integrals


def compute_deviations(avg, traces):
    deviations = []
    for trace in traces:
        deviations.append(avg - trace)
    deviations = np.array(deviations)
    return deviations


def get_taus(path):
    ch1_files, info_files = ds.filter_relevant_files(path)
    data = ds.nd_from_file(ch1_files[1])
    ts = ds.sampling_times(data, info_files)
    return ts


if __name__ == '__main__':
    main()
