from PIL import Image
from matplotlib import rcParams, pyplot as plt

from utility.tum_jet import tum_jet


def serif_font():
    rcParams['font.family'] = 'serif'
    rcParams['mathtext.fontset'] = 'dejavuserif'


def merge_images_vertically(images):
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    total_height = sum(heights)
    resulting_image = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for im in images:
        resulting_image.paste(im, (0, y_offset))
        y_offset += im.size[1]
    return resulting_image


def plot_borderless(array, name, vmin=None, vmax=None, dpi=500):
    fig = plt.figure(frameon=False)
    fig.set_size_inches(1, 1)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(array, vmin=vmin, vmax=vmax, cmap=tum_jet)
    fig.savefig('{}.png'.format(name), dpi=1000)
