import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    path_res = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180704_hf_setup_deer_tests/' \
               '009_deer_echo_with_pi'
    names_res = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    res_differences = get_differences(names_res, path_res)[0]
    taus = get_taus(names_res, path_res)
    plt.close('all')
    plt.plot(taus, res_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('009_deer_echo_with_pi.png', dpi=300)

    path_nonres = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180704_hf_setup_deer_tests'
    names_nonres = ['pulsed.008.mat']
    nonres_differences = get_differences(names_nonres, path_nonres)[0]
    taus = get_taus(names_nonres, path_nonres)
    plt.close('all')
    plt.plot(taus, nonres_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('pulsed008_nonres.png', dpi=300)

    plt.close('all')
    plt.plot(taus, nonres_differences - res_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('009_008_deer_decay_difference.png', dpi=300)

    plt.close('all')
    plt.plot(taus, nonres_differences, label='nonres')
    plt.plot(taus, res_differences, label='res')
    plt.xlabel('tau in sequence (ns)')
    plt.legend()
    plt.savefig('009_008_both_decays.png', dpi=300)


if __name__ == '__main__':
    main()
