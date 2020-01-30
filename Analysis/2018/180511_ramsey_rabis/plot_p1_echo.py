import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180511_ramsey_correlations_rabi/' \
           '007_ramsey_corr_echo_ramsey'
    names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    differences = get_differences(names, path)[0]

    # both graphs
    taus = get_taus(names, path)
    plt.close('all')
    plt.plot(taus, differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('p1_echo.png', dpi=300)


if __name__ == '__main__':
    main()
