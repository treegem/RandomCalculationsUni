import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    path_res = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180525_d35_xy8_decay_series/' \
               '000_xy8_decay_series_res'
    path_nonres = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180525_d35_xy8_decay_series/' \
                  '001_xy8_decay_series_nonres'
    index_res = 0
    index_nonres = 0
    order = 1

    while index_res < 5:

        create_plots(index_nonres, index_res, order, path_nonres, path_res)
        index_nonres, index_res = index_nonres + 1, index_res + 1
        order = order * 2


def create_plots(index_nonres, index_res, order, path_nonres, path_res):
    plot_names = {'res': '000_order{}_res.png'.format(order), 'nonres': '001_order{}_nonres.png'.format(order),
                  'diff': '000_001_order{}_diff.png'.format(order), 'both': '000_001_order{}_both.png'.format(order)}
    names_res = relevant_filenames(name='mes_{:03}.mat', ind_min=index_res, ind_max=index_res)
    res_differences = get_differences(names_res, path_res)[0]
    taus = get_taus(names_res, path_res)
    plt.close('all')
    plt.plot(taus, res_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig(plot_names['res'], dpi=300)
    names_nonres = relevant_filenames(name='mes_{:03}.mat', ind_min=index_nonres, ind_max=index_nonres)
    nonres_differences = get_differences(names_nonres, path_nonres)[0]
    taus = get_taus(names_nonres, path_nonres)
    plt.close('all')
    plt.plot(taus, nonres_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig(plot_names['nonres'], dpi=300)
    plt.close('all')
    plt.plot(taus, nonres_differences - res_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig(plot_names['diff'], dpi=300)
    plt.close('all')
    plt.plot(taus, nonres_differences, label='nonres')
    plt.plot(taus, res_differences, label='res')
    plt.xlabel('tau in sequence (ns)')
    plt.legend()
    plt.savefig(plot_names['both'], dpi=300)


if __name__ == '__main__':
    main()
