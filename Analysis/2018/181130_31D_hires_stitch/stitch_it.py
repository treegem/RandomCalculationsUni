import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
from scipy.ndimage.filters import gaussian_filter

import utility.tum_jet as tum_jet


def main():
    dir = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181130_31D_hires_stitching'

    ll = read_scan_file(dir, 'scan.000.mat')
    lr = read_scan_file(dir, 'scan.001.mat')
    ul = read_scan_file(dir, 'scan.002.mat')
    ur = read_scan_file(dir, 'scan.003.mat')

    ulr = np.average(ur[:, 0:15]) / np.average(ul[:, -15:])
    print('Upper left-right: ', ulr)
    llr = np.average(lr[:, 0:15]) / np.average(ll[:, -15:])
    print('Lower left-right: ', llr)

    pix = 250
    final_image = np.zeros((2 * pix, 2 * pix))

    final_image[pix:2 * pix, 0:pix] = ll
    final_image[pix:2 * pix, pix:2 * pix] = lr
    final_image[0:pix, 0:pix] = ul
    final_image[0:pix, pix:2 * pix] = ur

    plt.close('all')
    plt.imshow(final_image, cmap=tum_jet.tum_jet)
    plt.colorbar()
    plt.savefig('uncorrected.png', dpi=600)
    np.savetxt('uncorrected.txt', final_image)

    final_image[pix:2 * pix, 0:pix] = ll
    final_image[pix:2 * pix, pix:2 * pix] = lr / llr
    final_image[0:pix, 0:pix] = ul
    final_image[0:pix, pix:2 * pix] = ur / ulr

    final_image[:, 0:20] = gaussian_filter(final_image[:, 0:20], sigma=0.8)
    final_image[:, 170:173] = gaussian_filter(final_image[:, 170:173], sigma=0.8)
    final_image[:, 245:255] = gaussian_filter(final_image[:, 245:255], sigma=1.2)

    plt.close('all')
    plt.imshow(final_image, cmap=tum_jet.tum_jet)
    plt.colorbar()
    plt.savefig('corrected.png', dpi=600)
    np.savetxt('corrected.txt', final_image)


def read_scan_file(dir, file_name):
    full_data = sio.loadmat(os.path.join(dir, file_name))
    result = full_data['result']
    return result


if __name__ == '__main__':
    main()
