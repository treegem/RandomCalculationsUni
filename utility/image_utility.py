from PIL import Image
from matplotlib import rcParams


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