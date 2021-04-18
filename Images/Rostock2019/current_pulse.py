import matplotlib.pyplot as plt
import numpy as np

from utility import tum_jet


def main():
    # current_file = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190304_d06_gradient_sweeps_new_nv/' \
    #                'current_pulses_001/analogue_data_ch1_0.txt'
    current_file = 'currents.txt'
    currents = np.loadtxt(current_file)[-4096:]
    currents = 0.5 * currents / 8192
    offset = np.average(currents[:100])
    print(offset)
    currents = currents - offset
    fig = plt.figure(figsize=(6, 4))
    plt.plot([2. * i / 1000 for i in range(len(currents[:3000]))], currents[:3000] / 50. * 1000, color=tum_color(0))
    plt.xlabel(r'$t$ ($\mu$s)')
    plt.ylabel(r'Current (mA)')
    plt.tight_layout()
    plt.savefig('current_pulse.png', dpi=300)


def tum_color(index):
    color = tum_jet.tum_raw[index]
    norm_color = (color[0] / 256, color[1] / 256, color[2] / 256)
    return norm_color


if __name__ == '__main__':
    main()
