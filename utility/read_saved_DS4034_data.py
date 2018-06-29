import numpy as np


def read_bytes_from_file(file_path):
    read_data = read_file(file_path)
    return bytearray(read_data)


def read_file(file_path):
    with open(file_path, 'r') as f:
        read_data = f.read()
    return read_data


def read_nd_from_file(file_path):
    b_array = read_bytes_from_file(file_path)
    return np.array(b_array)


def get_property(file_path, prop):
    read_data = read_file(file_path)
    split_data = read_data.split('\n')
    target_property = split_data[property_index(prop)]
    target_value = target_property.split(' = ')[1]
    return float(target_value)


def property_index(prop):
    properties = {
        'time_abs': 0,
        'wait_time': 1,
        'sampling_rate': 2,
        'scale_channel_1': 3,
        'scale_channel_2': 4
    }
    prop_index = properties[prop]
    return prop_index


def test():
    import os
    path = 'A:/data/zzz_incoming/current_pulses'
    data_file = '1_info.txt'
    full_path = os.path.join(path, data_file)

    prop = 'scale_channel_2'
    target_value = get_property(full_path, prop)
    print(target_value)


if __name__ == '__main__':
    test()
