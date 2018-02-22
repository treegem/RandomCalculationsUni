import os

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from utility import tum_jet as tum


def main():
    dir_path = '//file/e24/Projects/ReinhardLab/group_members/Stefan Ernst/Posters/Mauterndorf Poster/' \
               'For Mauterndorf/DistanceExpData'

    positions_name = 'image_list143_positions_new_txt.txt'
    intensities_name = 'image_list143_summedInt_new_txt.txt'

    intensities, positions = load_files(dir_path, intensities_name, positions_name)

    plot_graph(intensities, positions, dir_path)


def plot_graph(intensities, positions, dir_path, fontsize=25, linewidth=2.0, tickwidth=2):
    rc('axes', linewidth=tickwidth)
    plt.plot(positions, intensities, color=tum.tum_colors[0][1], linewidth=linewidth)
    plt.plot([0, 0], [0, 100], '--', color=tum.tum_colors[5][1], linewidth=linewidth)
    plt.tick_params(direction='in', right=True, top=True, width=tickwidth, length=3*tickwidth)
    plt.xlabel('Air gap thickness [nm]', fontsize=fontsize)
    plt.ylabel('Intensity [%]', fontsize=fontsize)
    ticks = [0, 100, 200]
    plt.xticks(ticks, ticks, fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.tight_layout()
    plt.savefig(os.path.join(dir_path, 'distance_graph.jpg'), dpi=300)


def load_files(dir_path, intensities_name, positions_name):
    positions = np.loadtxt(os.path.join(dir_path, positions_name))
    positions -= positions[129]
    intensities = np.loadtxt(os.path.join(dir_path, intensities_name))
    return intensities, positions


if __name__ == '__main__':
    main()
