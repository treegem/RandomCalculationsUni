import numpy as np
import os
import scanning_poster_mauterndorf_2018.loading_data as ld
dir = '//file/e24/Projects/ReinhardLab/group_members/Stefan Ernst/Posters/Mauterndorf Poster/For Mauterndorf/' \
                'DistanceExpData'

file_name = 'SiO2_image_data_contact_fullscreen_66ms_0.gz'

image = np.loadtxt(os.path.join(dir, file_name))[100:-330, 580:-680]
images = [image]
ld.save_images_from_list(images, dir, id_str='', name='microscope', vmax=45000)
