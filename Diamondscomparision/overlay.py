# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:29:47 2017

@author: Georg.Braunbeck
"""

import numpy
import scipy.io as sio
import matplotlib.pylab as pylab
import tum_jet_blue_red as tum


path = '//file/e24/Projects/ReinhardLab/Data/170316_echoes_proem_03C/echo_004/'

mes_obj = sio.loadmat(path + 'mes_pulsed.mat')

origin = mes_obj['origin']
nvlist = mes_obj['nvlist'][0]
t2s = numpy.loadtxt('03C.txt')[:-1]/1000.
t2s = t2s * (t2s > 1.5)
ws = mes_obj['ws']

t2map = numpy.zeros_like(ws)
for i,nv in enumerate(nvlist):
    t2map = t2map + (ws == nv) * t2s[i]


pylab.imshow(origin, cmap= 'bone')
masked = numpy.ma.masked_where(t2map == 0., t2map)
pylab.imshow(masked, cmap = tum.tum_jet)
cbar = pylab.colorbar()
cbar.set_label('T2 (us)', size = 18)
pylab.savefig('t2overlay.jpg', dpi = 500)