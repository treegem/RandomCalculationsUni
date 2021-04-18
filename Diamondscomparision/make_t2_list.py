# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 18:00:51 2017

@author: Georg.Braunbeck
"""

import numpy
import matplotlib.pylab as pylab
from scipy.io import loadmat
from scipy.optimize import curve_fit
import os

path_0 = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/Data/170331_020_echo_after_implant/echo_'
path_1 = '001'
path = path_0+path_1 + '/'
name = '020'

nvlist = []

for file in os.listdir(path):
    if file.startswith("nv"):
        try:
            nvnumber = eval(file[2:5])
            nvlist.append(nvnumber)
        except:
            pass            

mes_data = loadmat(path + 'mes_pulsed.mat')
ws = mes_data['ws']
taus = mes_data['taus'][0]
nv_slots = mes_data['nv_slots']


nv_echoes = numpy.zeros((len(nvlist),len(taus)))

def fit_func(t, c, A , T):
    return c + A*numpy.exp(-t / T)


for i in range(len(nv_slots[0]) / 2):
    for j,nv in enumerate(nvlist):
        difference = nv_slots[j,2*i] - nv_slots[j, 2*i + 1]
        nv_echoes[j,i] = difference

t2s = numpy.zeros(len(nvlist)+1)

for i,nv_echo in enumerate(nv_echoes):
    popt = curve_fit(fit_func, taus, nv_echo, bounds = ([-20., 0., 1e3], [20., numpy.infty, 500e3]))[0]
    t2s[i] = popt[2]


summed = mes_data['result'][0]
summed_high = summed[::2]
summed_low = summed[1::2]
summed = summed_high - summed_low
popt = curve_fit(fit_func, taus, summed, bounds = ([-2e5, 0., 1e3], [2e5, 5e7, 500e3]))[0]
t2s[-1] = popt[2]

numpy.savetxt(name + '.txt', t2s)

