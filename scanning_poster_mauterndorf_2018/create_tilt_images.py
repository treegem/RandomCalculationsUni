import scanning_poster_mauterndorf_2018.loading_data as ld


def main():
    id_str = '145'
    name = 'untilted'
    data_path = '//file/e24/Projects/ReinhardLab/group_members/Stefan Ernst/Posters/Mauterndorf Poster/For Mauterndorf/' \
                'TiltExpData'

    images = ld.load_image_list(data_path=data_path, id_str=id_str, number_of_images=10)
    resize_images(images, x0=130, width=270, y0=243, height=270)
    ld.save_images_from_list(images, data_path, id_str, name=name, vmin=0, vmax=25000)

    id_str = '147'
    name = 'tilted'

    images = ld.load_image_list(data_path=data_path, id_str=id_str, number_of_images=10)
    resize_images(images, x0=130, width=270, y0=243, height=270)
    ld.save_images_from_list(images, data_path, id_str, name=name, vmin=0, vmax=25000)


def resize_images(images, x0, width, y0, height):
    for i, image in enumerate(images):
        images[i] = image[y0:y0 + height, x0:x0 + width]


if __name__ == '__main__':
    main()
