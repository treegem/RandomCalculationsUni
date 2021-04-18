import random

import matplotlib.pylab as pylab
import numpy as np

from Diamondscomparision import tum_jet
from Diamondscomparision.make_t2_comparison import extract_t2_and_average, random_x_values, rename_without_oxidation

if __name__ == '__main__':

    random.seed(40)
    arialfont = {'fontname': 'Arial'}
    directory = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/Georg/Documentation/170612_4_images_paper/Diamondscomparision/'
    files = [directory + '020']
    t2s, avgs = extract_t2_and_average(files=files)
    xs = random_x_values()
    rename_without_oxidation(files=files)

    fig = pylab.figure(figsize=(2.1, 1.8))
    medians_old = []
    max_old = []
    color_index = 6
    color = (tum_jet.tum_raw[color_index][0] / 255., tum_jet.tum_raw[color_index][1] / 255., tum_jet.tum_raw[color_index][2] / 255.)
    for i, t2 in enumerate(t2s):
        pylab.plot(xs[i][:], t2[:], '.k', alpha=0.7)
        medians_old.append(np.median(t2))
        max_old.append(t2.max())
        pylab.boxplot(t2[:], positions=[i + 1], widths=0.65, patch_artist=True, boxprops={'color': color, 'facecolor': color, 'alpha': 0.2},
                      whiskerprops={'color': color}, capprops={'color': color}, showfliers=False,
                      medianprops={'color': (tum_jet.tum_raw[5][0] / 255., tum_jet.tum_raw[5][1] / 255.,
                                             tum_jet.tum_raw[5][2] / 255.), 'linewidth': 2})
    # pylab.text(0.4, 45, 'acid \ncleaned', fontsize=10, bbox={'boxstyle': 'square', 'facecolor': 'white', 'alpha': 0.0},
    #            **arialfont)
    pylab.ylabel('$T_2$ (µs)', fontsize=10, **arialfont)
    pylab.yticks(fontsize=10, **arialfont)

    pylab.xlim([0.1, len(files) + 0.9])
    pylab.yticks([10, 20, 30, 40, 50], [10, 20, 30, 40, 50])
    pylab.xticks([])
    pylab.tight_layout()
    fig.savefig('single_box.png', dpi=1000)
