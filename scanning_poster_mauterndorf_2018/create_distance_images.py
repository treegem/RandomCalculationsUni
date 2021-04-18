import scanning_poster_mauterndorf_2018.loading_data as ld


def main():
    data_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/group_members/Stefan Ernst/Posters/Mauterndorf Poster/For Mauterndorf/' \
                'DistanceExpData'
    id_str = '143'

    images = ld.load_image_list(data_path=data_path, id_str=id_str, number_of_images=131)
    resize_images(images, x0=30, width=250, y0=65, height=250)
    ld.save_images_from_list(images, data_path, id_str, name='test', vmin=0, vmax=45000)


def resize_images(images, x0, width, y0, height):
    for i, image in enumerate(images):
        images[i] = image[y0:y0 + height, x0:x0 + width]


if __name__ == '__main__':
    main()
