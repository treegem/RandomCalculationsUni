import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate


def main():
    grid_source_path = 'gradient_sweep'
    probed_xs = create_grid_x(grid_source_path, 'integrated_currents_ch1_{:03}.txt', 1, 100)
    probed_ys = create_grid_y(grid_source_path, probed_xs, 'ch2_currents.txt')
    zs = create_zs_matrix(grid_source_path, probed_xs, 1, 'difference_interp_currents_{}.txt')

    points = (probed_xs.flatten(), probed_ys.flatten())
    grid_y, grid_x = np.mgrid[
                     np.average(probed_ys[0, :]):np.average(probed_ys[-1, :]):probed_ys.shape[0] * 1j,
                     np.average(probed_xs[:, 0]):np.average(probed_xs[:, -1]):probed_xs.shape[0] * 1j
                     ]
    zs_interp = scipy.interpolate.griddata(points=points, values=zs.flatten(), xi=(grid_x, grid_y), method='cubic',
                                           fill_value=0)

    plt.close('all')
    plt.imshow(zs_interp, extent=(np.average(probed_xs[:, 0]), np.average(probed_xs[:, -1]),
                                  np.average(probed_ys[0, :]), np.average(probed_ys[-1, :])))
    plt.savefig('2d_interpolations/only_interpolated.png', dpi=300)

    fft2 = np.fft.rfft2(zs_interp)

    plt.close('all')
    plt.imshow(abs(fft2), vmax=1)
    plt.colorbar()
    plt.savefig('2d_interpolations/only_interpolated_fft.png', dpi=300)

    for angle in np.arange(0, 90 + 1, 5):
        if angle == 0:
            continue
        print('angle: ', angle)
        new_xs, new_ys = rotate(probed_ys, angle=angle)
        xs = probed_xs + new_xs
        ys = new_ys
        points = (xs.flatten(), ys.flatten())
        grid_y, grid_x = np.mgrid[ys.min():ys.max():ys.shape[0] * 1j, xs.min():xs.max():xs.shape[0] * 1j]
        zs_interp = scipy.interpolate.griddata(points=points, values=zs.flatten(), xi=(grid_x, grid_y), method='cubic',
                                               fill_value=0)
        plt.close('all')
        plt.imshow(zs_interp, vmin=-0.02, vmax=0.02, extent=(xs.min(), xs.max(), ys.min(), ys.max()), aspect='auto')
        plt.colorbar()
        plt.savefig('2d_interpolations/interp_{}.png'.format(angle), dpi=300)

        fft2 = np.fft.rfft2(zs_interp)

        plt.close('all')
        plt.imshow(abs(fft2[1:, :]))
        plt.colorbar()
        plt.savefig('2d_interpolations/interp_{}_fft.png'.format(angle), dpi=300)


def rotate(xs, angle):
    angle = angle / 180 * np.pi
    ys = np.zeros_like(xs)
    new_xs = xs * np.cos(angle) - ys * np.sin(angle)
    new_ys = xs * np.sin(angle) + ys * np.cos(angle)
    return new_xs, new_ys


def create_zs_matrix(probe_source_path, probed_xs, start_index, zs_name_skelleton):
    zs = np.zeros_like(probed_xs)
    for i in range(zs.shape[0]):
        zs_data = np.loadtxt(os.path.join(probe_source_path, zs_name_skelleton.format(i + start_index)))
        zs[i] = zs_data
    return zs


def create_grid_y(probed_source_path, probed_xs, probed_y_source_file):
    grid_y_currents = np.loadtxt(os.path.join(probed_source_path, probed_y_source_file))
    grid_y = np.zeros_like(probed_xs)
    for i in range(grid_y.shape[0]):
        grid_y[i, :] = np.zeros(grid_y.shape[1]) + grid_y_currents[i]
    return grid_y


def create_grid_x(probed_source_path, probed_x_file_skelleton, start_index, end_index):
    for i in range(start_index, end_index + 1):
        data = np.loadtxt(os.path.join(probed_source_path, probed_x_file_skelleton.format(i)))

        if i == start_index:
            grid_x = np.zeros((end_index - start_index + 1, len(data)))

        grid_x[i - start_index] = data
    return grid_x


if __name__ == '__main__':
    main()
    # rotate(np.array([1, 1]), 90)
