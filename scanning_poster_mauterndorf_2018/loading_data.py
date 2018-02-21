import os

import matplotlib.pylab as plt
import numpy

import utility.tum_jet as tum


#################################################################
# Loading saved (.gz) image_list, position_list (and save .png) #
#################################################################


def load_image_list(data_path, id_str, number_of_images=None):
    if number_of_images is None:
        position_list_loaded = numpy.loadtxt(data_path + '\\' + 'position_list' + id_str + '.gz')
        number_of_images = int(position_list_loaded.shape[0])
    image_list_loaded = []
    for i in range(number_of_images):
        image_path = data_path + '\\' + 'image_list' + id_str + '_' + str(i) + '.gz'
        if os.path.isfile(image_path):
            temporary_image = numpy.loadtxt(image_path)
            image_list_loaded.append(temporary_image)
    return image_list_loaded


def save_images_from_list(image_list_loaded, data_path, id_str, save_increment=1, name='image', vmin=0, vmax=64000):
    for i in range(len(image_list_loaded)):
        if i % save_increment == 0:
            plt.clf()
            plt.imshow(image_list_loaded[i], vmin=vmin, vmax=vmax, cmap=tum.tum_jet)
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            filename = name + id_str + '_' + str(i)
            plt.savefig(data_path + '\\' + filename, dpi=500)
