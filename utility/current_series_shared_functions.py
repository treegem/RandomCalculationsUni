from matplotlib import pyplot as plt


def calc_vmin_vmax(zs_2d, min_index=10, max_index=20):
    vmin = zs_2d[:, min_index:max_index].min()
    vmax = zs_2d[:, min_index:max_index].max()
    return vmax, vmin


def plot_2d(name, vmax, vmin, zs_2d):
    plt.close('all')
    plt.imshow(zs_2d, vmin=vmin, vmax=vmax)
    plt.savefig(name, dpi=300)