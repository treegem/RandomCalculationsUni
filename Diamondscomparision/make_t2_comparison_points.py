# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:41:35 2017

@author: Georg.Braunbeck
"""

import glob
import numpy
import matplotlib.pylab as pylab
import random

# get all files ending with txt info 'files'
files = []
directory = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/Georg/Documentation/170612_4_images_paper/AFM/'
for file in glob.glob(directory + "*.txt"):
    if file[0] != 'n':
        files.append(file.split('.')[0])

new_order = [1, 8, 2, 6, 5, 7, 3, 9, 0, 4]
files = [files[i] for i in new_order]

t2s = []
avgs = []

upper_limit = 50

for dia in files:
    t2 = numpy.loadtxt(dia + ".txt")
    t2 /= 1000
    avgs.append(t2[-1])
    t2[-1] = 0
    t2 *= (t2 < upper_limit)
    t2 *= (t2 > 1.500)

    t2 = numpy.trim_zeros(numpy.sort(t2))

    t2s.append(t2)

xs = []

for i, t2 in enumerate(t2s):
    x = numpy.zeros_like(t2) + (i + 1)
    for j, t in enumerate(x):
        x[j] = t + random.uniform(-0.25, 0.25)
    xs.append(x)

fig = pylab.figure()
pylab.subplot(211)
for i, t2 in enumerate(t2s):
    pylab.plot(xs[i][:-1], t2[:-1], '.b')

for i, f in enumerate(files):
    if f == '01C':
        files[i] = f + '\n              (Williams)'
    if f == '01D':
        files[i] = f + '\n            (Touge)'
    if f == '02B':
        files[i] = f + '\n            (Almax)'
    if f == '020':
        files[i] = f + '\n(d2tec)'
    if f == '01Df':
        files[i] = f + '\n           (e6)'
    if f == '01B':
        files[i] = f + '\n(H)'

pylab.ylabel('T2 (um)')

for x in numpy.arange(0.5, 9, 2):
    pylab.plot((x, x), (1, 49), 'k--', linewidth=1.5)

pylab.plot((9.5, 9.5), (1, 49), 'k--', linewidth=1.5)

pylab.xlim([0.1, len(files) + 0.9])

pylab.subplots_adjust(hspace=.001)

# get all files ending with txt info 'files' after 520
nfiles = []
for file in glob.glob("*.txt"):
    if file[0] == 'n':
        nfiles.append(file.split('.')[0])

nnew_order = [1, 8, 2, 6, 5, 7, 3, 9, 0, 4]
nfiles = [nfiles[i] for i in nnew_order]

nt2s = []
navgs = []

nupper_limit = 50

for dia in nfiles:
    t2 = numpy.loadtxt(dia + ".txt")
    t2 /= 1000
    avgs.append(t2[-1])
    t2[-1] = 0
    t2 *= (t2 < upper_limit)
    t2 *= (t2 > 1.500)

    t2 = numpy.trim_zeros(numpy.sort(t2))

    nt2s.append(t2)

xs = []

for i, t2 in enumerate(nt2s):
    x = numpy.zeros_like(t2) + (i + 1)
    for j, t in enumerate(x):
        x[j] = t + random.uniform(-0.25, 0.25)
    xs.append(x)

pylab.subplot(212)
for i, t2 in enumerate(nt2s):
    pylab.plot(xs[i][:-1], t2[:-1], '.b')

pylab.xlim([0.1, len(files) + 0.9])
pylab.xticks(range(1, len(files) + 1), files)

for x in numpy.arange(0.5, 9, 2):
    pylab.plot((x, x), (1, 49), 'k--', linewidth=1.5)

pylab.plot((9.5, 9.5), (1, 49), 'k--', linewidth=1.5)

pylab.savefig('t2comparison.jpg', dpi=500)
