import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from utility.image_utility import serif_font
from utility.path_utility import TEMP_PATH
from utility.storage_utility import save_figure
from utility.tum_jet import tum_colors


def main():
    rabi_fast, rabi_slow, ts = compute_rabi_graphs()

    serif_font()
    plt.figure(figsize=(19 / 2.54, 10 / 2.54))
    plt.plot(ts, rabi_slow, color=tum_colors[0][1], label=r'$B_1$')
    plt.plot(ts, rabi_fast, '--', color=tum_colors[5][1], label=r'$B_1^* > B_1$')
    plt.ylabel(r'Spin $z$-component', fontsize=14)
    plt.xlabel(r'Pulse length $T_\mathregular{p}$', fontsize=14)
    plt.xticks(np.arange(0, 10, np.pi / 2), ['0', r'$T_{\pi / 2}$', r'$T_{\pi}$', r'$T_{3 \pi / 2}$', r'$T_{2 \pi}$',
                                             r'$T_{5 \pi / 2}$', r'$T_{3 \pi}$'])
    plt.legend()
    plt.tight_layout()
    save_figure()

    image2 = os.path.join(TEMP_PATH, 'figure.png')
    latex_image_path = '//file/e24/Projects/ReinhardLab/Georg/Abstracts Anträge/F-Praktikum/Latexnew/images'
    image1 = os.path.join(latex_image_path, 'rabi_sequence.png')
    image_list = [image1, image2]
    images = list(map(Image.open, image_list))
    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    total_height = sum(heights)

    resulting_image = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for im in images:
        resulting_image.paste(im, (0, y_offset))
        y_offset += im.size[1]

    resulting_image.save(os.path.join(latex_image_path, 'rabi.png'))


def compute_rabi_graphs():
    ts = np.linspace(0, 10, 500)
    rabi_slow = np.zeros_like(ts)
    rabi_fast = np.zeros_like(ts)
    b1 = 1
    b2 = np.sqrt(2) * b1
    for i, t in enumerate(ts):
        rabi_slow[i] = np.cos(t * b1)
        rabi_fast[i] = np.cos(t * b2)
    return rabi_fast, rabi_slow, ts


if __name__ == '__main__':
    main()
