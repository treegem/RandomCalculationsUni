import os

from matplotlib import pyplot as plt

from utility.path_utility import TEMP_PATH


def save_figure(path=None):
    if path is None:
        path = os.path.join(TEMP_PATH, 'figure.png')
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    plt.savefig(path, dpi=300)
