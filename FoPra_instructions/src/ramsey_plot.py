import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from utility.image_utility import serif_font, merge_images_vertically
from utility.path_utility import TEMP_PATH
from utility.storage_utility import save_figure
from utility.tum_jet import tum_colors


def main():

    low_detuning, high_detuning, ts = compute_ramsey_graphs()
    create_ramsey_mes_plot(low_detuning, high_detuning, ts)

    latex_image_path = '//file/e24/Projects/ReinhardLab/Georg/Abstracts Anträge/F-Praktikum/Latexnew/images'
    image1 = os.path.join(latex_image_path, 'ramsey_sequence.png')
    image2 = os.path.join(TEMP_PATH, 'figure.png')
    image_path_list = [image1, image2]
    images = list(map(Image.open, image_path_list))

    resulting_image = merge_images_vertically(images)
    resulting_image.save(os.path.join(latex_image_path, 'ramsey.png'))


def compute_ramsey_graphs():
    ts = np.linspace(0, 10, 500)
    low_detuning = np.zeros_like(ts)
    high_detuning = np.zeros_like(ts)
    dw1 = 1
    dw2 = np.pi * dw1 / 2
    for i, t in enumerate(ts):
        low_detuning[i] = -np.cos(t * dw1)
        high_detuning[i] = -np.cos(t * dw2)
    return low_detuning, high_detuning, ts


def create_ramsey_mes_plot(low_detuning, high_detuning, ts):
    serif_font()
    plt.figure(figsize=(19 / 2.54, 10 / 2.54))
    plt.plot(ts, high_detuning, color=tum_colors[0][1], label=r'$\Delta \omega_1 > 0$')
    plt.plot(ts, low_detuning, '--', color=tum_colors[5][1], label=r'$\Delta \omega_2 < \Delta \omega_1$')
    plt.ylabel(r'Spin $z$-component', fontsize=14)
    plt.xlabel(r'Free evolution time $\tau$', fontsize=14)
    plt.xticks(np.arange(0, 11, 4), ['0', r'$\tau_{2\pi}$', r'2$\tau_{2\pi}$', r'3$\tau_{2\pi}$'])
    plt.legend()
    plt.tight_layout()
    save_figure()


if __name__ == '__main__':
    main()
