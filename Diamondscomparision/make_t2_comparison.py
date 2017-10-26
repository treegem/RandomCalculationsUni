# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:41:35 2017

@author: Georg.Braunbeck
"""

import glob
import random

import matplotlib.pylab as pylab
import numpy
import tum_jet


def get_txt_files_without_oxidation():
    global files, file
    # get all files ending with txt info 'files'
    files = []
    for file in glob.glob("*.txt"):
        if file[0] != 'n':
            files.append(file.split('.')[0])


def reorder_files():
    global files
    new_order = [1, 8, 2, 6, 5, 7, 3, 9, 0, 4]
    files = [files[i] for i in new_order]


def extract_t2_and_average():
    global t2s, avgs, dia, t2
    t2s = []
    avgs = []
    upper_limit = 60
    for dia in files:
        t2 = numpy.loadtxt(dia + ".txt")
        t2 /= 1000
        avgs.append(t2[-1])
        t2[-1] = 0
        t2 *= (t2 < upper_limit)
        t2 *= (t2 > 1.500)

        t2 = numpy.trim_zeros(numpy.sort(t2))

        t2s.append(t2)


def random_x_values():
    global xs, i, t2, x, j, t
    xs = []
    for i, t2 in enumerate(t2s):
        x = numpy.zeros_like(t2) + (i + 1)
        for j, t in enumerate(x):
            x[j] = t + random.uniform(-0.25, 0.25)
        xs.append(x)


def rename_without_oxidation():
    global i
    for i, f in enumerate(files):
        if f == '01C':
            files[i] = 'Cmp1'
        if f == '03D':
            files[i] = 'Cmp2'
        if f == '01D':
            files[i] = 'Uv1'
        if f == '02D':
            files[i] = 'Uv2'
        if f == '02B':
            files[i] = 'Scf1'
        if f == '03C':
            files[i] = 'Scf2'
        if f == '020':
            files[i] = 'Std3'
        if f == '01Df':
            files[i] = 'Std1'
        if f == '03Df':
            files[i] = 'Std2'
        if f == '01B':
            files[i] = 'H1'


def box_plot_without_oxidation():
    global fig, i, t2, color
    medians_old = []
    maxs_old = []
    fig = pylab.figure(figsize=(7.48, 2.9))
    pylab.subplot(211)
    for i, t2 in enumerate(t2s):
        if i == 0:
            color = (tum_jet.tum_raw[0][0] / 255., tum_jet.tum_raw[0][1] / 255., tum_jet.tum_raw[0][2] / 255.)
        if i == 2:
            color = (tum_jet.tum_raw[2][0] / 255., tum_jet.tum_raw[2][1] / 255., tum_jet.tum_raw[2][2] / 255.)
        if i == 4:
            color = (tum_jet.tum_raw[4][0] / 255., tum_jet.tum_raw[4][1] / 255., tum_jet.tum_raw[4][2] / 255.)
        if i == 6:
            color = (tum_jet.tum_raw[1][0] / 255., tum_jet.tum_raw[1][1] / 255., tum_jet.tum_raw[1][2] / 255.)
        if i == 8:
            color = (tum_jet.tum_raw[6][0] / 255., tum_jet.tum_raw[6][1] / 255., tum_jet.tum_raw[6][2] / 255.)
        if i == 9:
            color = 'grey'
        pylab.plot(xs[i][:], t2[:], '.k', alpha=0.7)
        medians_old.append(numpy.median(t2))
        maxs_old.append(t2.max())
        pylab.boxplot(t2[:], positions=[i + 1], widths=0.65, patch_artist=True, boxprops={'color': color, 'alpha': 0.2},
                      whiskerprops={'color': color}, capprops={'color': color}, showfliers=False,
                      medianprops={'color': (tum_jet.tum_raw[5][0] / 255., tum_jet.tum_raw[5][1] / 255.,
                                             tum_jet.tum_raw[5][2] / 255.), 'linewidth': 2})
    pylab.text(0.4, 45, 'acid \ncleaned', fontsize=10, bbox={'boxstyle': 'square', 'facecolor': 'white', 'alpha': 0.0},
               **arialfont)
    pylab.ylabel('$T_2$ (µs)', fontsize=10, **arialfont)
    pylab.yticks(fontsize=10, **arialfont)

    pylab.xlim([0.1, len(files) + 0.9])
    pylab.yticks([10, 20, 30, 40, 50], [10, 20, 30, 40, 50])

    pylab.subplots_adjust(hspace=.001)
    return medians_old


def get_txt_files_with_oxidation():
    global nfiles, file
    # get all files ending with txt info 'files' after 520
    nfiles = []
    for file in glob.glob("*.txt"):
        if file[0] == 'n':
            nfiles.append(file.split('.')[0])


def reorder_nfiles():
    global i, nfiles
    nnew_order = [1, 8, 2, 6, 5, 7, 3, 9, 0, 4]
    nfiles = [nfiles[i] for i in nnew_order]


def extract_nt2_and_naverage():
    global nt2s, dia, t2
    nt2s = []
    navgs = []
    nupper_limit = 60
    for dia in nfiles:
        t2 = numpy.loadtxt(dia + ".txt")
        t2 /= 1000
        avgs.append(t2[-1])
        t2[-1] = 0
        t2 *= (t2 < nupper_limit)
        t2 *= (t2 > 1.500)

        t2 = numpy.trim_zeros(numpy.sort(t2))

        nt2s.append(t2)


def new_random_x_values():
    global xs, i, t2, x, j, t
    xs = []
    for i, t2 in enumerate(nt2s):
        x = numpy.zeros_like(t2) + (i + 1)
        for j, t in enumerate(x):
            x[j] = t + random.uniform(-0.25, 0.25)
        xs.append(x)


def box_plot_with_oxidation():
    global color, i, t2
    medians_new = []
    maxs_new = []
    pylab.subplot(212)
    color = 'blue'
    for i, t2 in enumerate(nt2s):
        if i == 0:
            color = (tum_jet.tum_raw[0][0] / 255., tum_jet.tum_raw[0][1] / 255., tum_jet.tum_raw[0][2] / 255.)
        if i == 2:
            color = (tum_jet.tum_raw[2][0] / 255., tum_jet.tum_raw[2][1] / 255., tum_jet.tum_raw[2][2] / 255.)
        if i == 4:
            color = (tum_jet.tum_raw[4][0] / 255., tum_jet.tum_raw[4][1] / 255., tum_jet.tum_raw[4][2] / 255.)
        if i == 6:
            color = (tum_jet.tum_raw[1][0] / 255., tum_jet.tum_raw[1][1] / 255., tum_jet.tum_raw[1][2] / 255.)
        if i == 8:
            color = (tum_jet.tum_raw[6][0] / 255., tum_jet.tum_raw[6][1] / 255., tum_jet.tum_raw[6][2] / 255.)
        if i == 9:
            color = 'grey'
        pylab.plot(xs[i][:], t2[:], '.k', alpha=0.7)
        medians_new.append(numpy.median(t2))
        maxs_new.append(t2.max())
        pylab.boxplot(t2[:], positions=[i + 1], widths=0.65, patch_artist=True, boxprops={'color': color, 'alpha': 0.2},
                      whiskerprops={'color': color}, capprops={'color': color}, showfliers=False,
                      medianprops={'color': (tum_jet.tum_raw[5][0] / 255., tum_jet.tum_raw[5][1] / 255.,
                                             tum_jet.tum_raw[5][2] / 255.), 'linewidth': 2})
    pylab.xlim([0.1, len(files) + 0.9])
    pylab.xticks(range(1, len(files) + 1), files, fontsize=10, **arialfont)
    pylab.ylim([0, 60])
    pylab.yticks([0, 10, 20, 30, 40, 50, ], [0, 10, 20, 30, 40, 50, ], fontsize=10, **arialfont)
    pylab.ylabel('$T_2$ (µs)', fontsize=10, **arialfont)
    pylab.text(0.4, 47, '520 °C', fontsize=10, bbox={'boxstyle': 'square', 'facecolor': 'white', 'alpha': 0.0},
               **arialfont)
    return medians_new


if __name__ == '__main__':

    random.seed(40)
    arialfont = {'fontname': 'Arial'}

    get_txt_files_without_oxidation()
    reorder_files()
    extract_t2_and_average()
    random_x_values()
    medians_old = box_plot_without_oxidation()
    rename_without_oxidation()

    get_txt_files_with_oxidation()
    reorder_nfiles()
    extract_nt2_and_naverage()
    new_random_x_values()
    medians_new = box_plot_with_oxidation()

    fig.savefig('t2comparisonquartil.png', dpi=1000)
