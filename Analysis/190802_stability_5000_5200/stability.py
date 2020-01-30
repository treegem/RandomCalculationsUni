import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


def main():
    base_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190802_stability_5000_5200'
    stability_check(base_path, '000_5000_5200_series')


def stability_check(base_path, folder):
    print('\n\nfolder:', folder)
    full_path = os.path.join(base_path, folder)
    sub_folders = os.listdir(full_path)
    for i, sub_folder in enumerate(sub_folders):
        print('\nsubfolder:', sub_folder)
        zs = np.loadtxt(os.path.join(full_path, sub_folder, 'zs.txt'))
        if i == 0:
            zs_2d = np.zeros((len(sub_folders), len(zs)))
            zs_taus_2d = np.zeros((len(sub_folders), len(zs)))
        zs_2d[i] = zs

        zs_taus = average_z_of_mat_files(full_path, sub_folder, zs_taus_2d)
        zs_taus_2d[i] = zs_taus

    if not os.path.isdir(folder):
        os.makedirs(folder)

    save_txts(folder, zs_2d, zs_taus_2d)

    save_plots(folder, zs_2d, zs_taus_2d)


def average_z_of_mat_files(full_path, sub_folder, zs_taus_2d):
    index = 0
    zs_taus = np.zeros(zs_taus_2d.shape[1])
    while os.path.isfile(mat_file_name(full_path, index, sub_folder)):
        if index % 10 == 0:
            print('\rmatfile: {}     '.format(index), end='')
        data = sio.loadmat(mat_file_name(full_path, index, sub_folder))
        zs = data['z'][0]
        zs_taus += zs
        index += 1
    zs_taus /= index
    return zs_taus


def save_plots(folder, zs_2d, zs_taus_2d):
    plt.close('all')
    plt.imshow(zs_2d, vmin=max(0.8, zs_2d[:, 10:-10].min()), vmax=min(1.1, zs_2d[:, 10:-10].max()))
    plt.colorbar()
    plt.savefig('{}/{}.png'.format(folder, folder), dpi=300)
    plt.close('all')
    plt.imshow(zs_taus_2d, vmin=max(0.8, zs_2d[:, 10:-10].min()), vmax=min(1.1, zs_taus_2d[:, 10:-10].max()))
    plt.colorbar()
    plt.savefig('{}/{}_taus.png'.format(folder, folder), dpi=300)


def save_txts(folder, zs_2d, zs_taus_2d):
    np.savetxt('{}/{}.txt'.format(folder, folder), zs_2d)
    np.savetxt('{}/{}_taus.txt'.format(folder, folder), zs_taus_2d)


def mat_file_name(full_path, index, sub_folder):
    return os.path.join(full_path, sub_folder, 'pulsed.{:03d}.mat'.format(index))


if __name__ == '__main__':
    main()
