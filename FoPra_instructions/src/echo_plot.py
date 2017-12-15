import os
from scipy import signal

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from utility.image_utility import serif_font, merge_images_vertically
from utility.path_utility import TEMP_PATH
from utility.storage_utility import save_figure
from utility.tum_jet import tum_colors


def main():

    revival, decay, ts = compute_ramsey_graphs()
    create_ramsey_mes_plot(revival, decay, ts)

    latex_image_path = '//file/e24/Projects/ReinhardLab/Georg/Abstracts Anträge/F-Praktikum/Latexnew/images'
    image1 = os.path.join(latex_image_path, 'hahn_sequence.png')
    image2 = os.path.join(TEMP_PATH, 'revival.png')
    image3 = os.path.join(TEMP_PATH, 'decay.png')
    image_path_list = [image1, image2, image3]
    images = list(map(Image.open, image_path_list))

    resulting_image = merge_images_vertically(images)
    resulting_image.save(os.path.join(latex_image_path, 'hahn.png'))


def compute_ramsey_graphs():
    ts = np.linspace(0, 10, 500)
    revival = signal.gaussian(len(ts), 80)
    decay = np.zeros_like(ts)
    k = 0.25
    for i, t in enumerate(ts):
        decay[i] = np.exp(-t*k)
    return revival, decay, ts


def create_ramsey_mes_plot(revival, decay, ts):
    serif_font()
    plt.figure(figsize=(19 / 2.54, 6 / 2.54))

    create_revival_plot(path=os.path.join(TEMP_PATH, 'revival.png'), data=revival)

    plt.clf()

    plt.plot(ts, decay, color=tum_colors[0][1], label=r'$\tau = \tau_1 = \tau_2$')
    x0, x1 = plt.xlim()
    y0, y1 = plt.ylim()
    y0 = -0.04

    e_inv, t2 = plot_t2(decay, ts, x0, y0)

    format_plot(e_inv, t2, x0, x1, y0, y1)

    save_figure(path=os.path.join(TEMP_PATH, 'decay.png'))


def format_plot(e_inv, t2, x0, x1, y0, y1):
    decay_legend = plt.legend(handlelength=0, handletextpad=0)
    for item in decay_legend.legendHandles:
        item.set_visible(False)
    plt.ylabel(r'Spin $z$-component', fontsize=14)
    plt.xlabel(r'Free evolution time $\tau$', fontsize=14)
    plt.title('Echo decay')
    plt.xlim((x0, x1))
    plt.ylim((y0, y1))
    plt.yticks([0, e_inv, 1], ['0.0', r'$1/e$', '1.0'])
    plt.xticks([0, t2], ['0', r'$T_2$'])


def plot_t2(decay, ts, x0, y0):
    e_inv = np.exp(-1)
    t2_ind = np.where(decay <= e_inv)[0][0]
    t2 = ts[t2_ind]
    plt.plot([t2, t2], [y0, e_inv], '--', color='grey')
    plt.plot([x0, t2], [e_inv, e_inv], '--', color='grey')
    return e_inv, t2


def create_revival_plot(path, data):
    plt.plot(data, color=tum_colors[0][1])
    plt.ylabel(r'Spin $z$-component', fontsize=14)
    plt.xlabel(r'Free evolution time $\tau_2$', fontsize=14)
    plt.xticks([0, 250, 500], ['0', r'$\tau_1$', r'$2\tau_1$'])
    plt.title('Echo revival')
    plt.tight_layout()
    save_figure(path=path)


if __name__ == '__main__':
    main()
