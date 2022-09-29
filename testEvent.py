#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 20:37:48 2022

@author: nahuel
"""
import signal
import sys
import matplotlib.pyplot as plt
from pylsl import resolve_stream, StreamInlet, local_clock
import threading
import time
import random
import os
import numpy as np
from datetime import datetime
from libb import *


def save(config_calibration, data, lista_ts, labels):
    #path = config_calibration['path']
    #posiciones = None
    #print(data)
    #print(type(data))
    #convertir de uV -> V
    #data = data / 1000000
    #raw = loadDatos(data, 'ch_names.txt')
    #montage = make_standard_montage('standard_1020')
    #raw.set_montage(montage)
    #print(raw)
    
    #Buscamos posicion del evento por proximidad ts
    for x in labels:
        resta = abs(lista_ts - x[0])
        pos = np.where(min(resta) == resta)[0]
        if posiciones is None:
            posiciones = pos
        else:
            posiciones = np.append(posiciones, pos)
            
    #Con las posiciones creamos matriz de eventos pos x zero x event
    events = np.zeros((len(labels) , 3), int)
    events[:, 0] = posiciones.astype(int)
    events[:, 2] = labels[:,1].astype(int)
    print(events)
    mne.write_events(path + "/event.fif", events)
    raw.plot(scalings=None, n_channels=8, events=events)
    
def main():
    print("Inicio...")
    config_calibration = loadConfig("config.ini", "CALIBRATION")
    path = config_calibration['path']
    #raw.save(path + "/data_eeg.fif")
    raw = mne.io.read_raw_fif(path + "/data_eeg.fif", preload=True)
    lista_ts = np.load(path + '/lista_ts.npy')
    labels = np.load(path + '/labels.npy')
    
    events = mne.read_events(path + "/event.fif")
    
    posiciones = events[:, 0]
    #print(events[:,0])
    
    i=0
    for x in posiciones:
        print( datetime.fromtimestamp(lista_ts[x]), '-', datetime.fromtimestamp( labels[i][0] ) )
        i = i+1
    #print( datetime.fromtimestamp(lista_ts[0])  )
    #print("lista_ts")
#    for i in lista_ts:
#        print( datetime.fromtimestamp(i)  )
    #print("labels")
    #for j in labels:
    #    print( datetime.fromtimestamp(j[0]) )
    
    #save(config_calibration, total_data, lista_ts, labels)
    
if __name__ == "__main__":
    main()    