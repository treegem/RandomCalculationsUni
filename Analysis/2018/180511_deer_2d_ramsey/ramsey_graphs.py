import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    pure_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180511_deer_2d_plot_ramsey/deer_ramsey_without_pi_009'
    pure_names = relevant_filenames(name='mes_{:03}.mat', ind_min=10, ind_max=10)
    pure_differences = get_differences(pure_names, pure_path)[0]

    pi_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180511_deer_2d_plot_ramsey/deer_ramsey_with_pi_010'
    pi_names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    pi_differences = get_differences(pi_names, pi_path)[0]

    # both graphs
    taus = get_taus(pure_names, pure_path)
    plt.close('all')
    plt.plot(taus, pure_differences, label='pure')
    plt.plot(taus, pi_differences, label='with pi')
    plt.xlabel('tau in sequence (ns)')
    plt.legend()
    plt.savefig('ramsey_graphs.png', dpi=300)

    # difference
    plt.close('all')
    plt.plot(taus, pure_differences - pi_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('ramsey_graphs_difference.png', dpi=300)


if __name__ == '__main__':
    main()
