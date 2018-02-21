import matplotlib.pylab as plt
import numpy


# datapath = '??'  # path to folder out of which data is loaded and path to folder where it is saved.

#################################################################
# Loading saved (.gz) image_list, position_list (and save .png) #
#################################################################

# runIDnumberStr = '??'  # specify what data to load in current folder (datapath)


def load_image_list(data_path, run_id):
    position_list_loaded = numpy.loadtxt(data_path + '\\' + 'position_list' + run_id + '.gz')
    number_of_images = int(position_list_loaded.shape[0])
    image_list_loaded = []
    for i in range(number_of_images):
        temporary_image = numpy.loadtxt(data_path + '\\' + 'image_list' + run_id + '_' + str(i) + '.gz')
        image_list_loaded.append(temporary_image)
    return image_list_loaded


def save_images_from_list(image_list_loaded, data_path, run_id, save_increment=1):
    for i in range(len(image_list_loaded)):
        if i % save_increment == 0:
            plt.clf()
            plt.imshow(image_list_loaded[i], vmin=0, vmax=64000)  # change dependent on image data!!!
            plt.colorbar()
            filename = 'image' + run_id + '_' + str(i)
            plt.savefig(data_path + '\\' + filename, dpi=80)
