#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 16:22:49 2021

@author: nahuel
"""
#librerias
import numpy as np
import time
from datetime import datetime
#from loaddata import *

#sklearn
from sklearn.model_selection import ShuffleSplit, cross_val_score, cross_val_predict
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics as met
import joblib

#mne
import mne
from mne.decoding import CSP
from mne.channels import read_layout
from mne.channels import make_standard_montage
from mne.preprocessing import (create_eog_epochs, create_ecg_epochs,
                               compute_proj_ecg, compute_proj_eog)
from libb import *

from pylsl import resolve_stream, StreamInlet

def main():
    """        
    data = np.load('total_data.npy')
    #convertir de uV -> V
    data = data / 1000000
    print(data.shape)
    print(type(data))
    print(type(data[0][1]))
    
    raw = loadDatos(data, 'ch_names.txt')
    montage = make_standard_montage('standard_1020')
    raw.set_montage(montage)
    raw.plot(scalings=None, n_channels=8)
    
    print(raw)
    raw.save("eeg.fif", overwrite=True)
    #raw = mne.io.read_raw_fif("eeg.fif", preload=True)
    
    #print(type(raw))

    #raw.plot(scalings='auto', n_channels=1)
    """    

    #aw = mne.io.read_raw_fif("data_eeg.fif", preload=True)
    #raw.plot(scalings=None, n_channels=8)
    
    lista_ts = np.load('lista_ts.npy')
    labels = np.load('labels.npy')
    print(len(lista_ts))
    print(len(labels))
    
    posiciones = None
    for x in labels:
        resta = abs(lista_ts - x[0])
        pos = np.where(min(resta) == resta)[0]
        if (len(pos) > 1):
            pos = [pos[0]]
            print(pos, "-",  len(pos))
        if posiciones is None:
            posiciones = pos
        else:
            posiciones = np.append(posiciones, pos)
            
    events = np.zeros((len(labels) , 3), int)
    events[:, 0] = posiciones.astype(int)
    events[:, 2] = labels[:,1].astype(int)
    print(events)
    
    mne.write_events("event.fif", events)
    print(len(posiciones))
    print(lista_ts[254274])
    print(lista_ts[256483])
    
    print(datetime.fromtimestamp(lista_ts[254274]))
    print(datetime.fromtimestamp(lista_ts[256483]))
    
    #[254274 256483]
    #[258913 262809]
    #[267050 274575]
    
    #17104
    #print(lista_ts[14114])
    
    #streams = resolve_stream('type', 'EEG')
    #inlet = StreamInlet(streams[0])
    #inlet.time_correction()
    #print(datetime.fromtimestamp(lista_ts[14114]))
    #print(datetime.fromtimestamp(lista_ts[20676]))
    #print(datetime.fromtimestamp(lista_ts[27228]))
    #print(datetime.fromtimestamp(lista_ts[33573]))
    
    print("-----")
    #print(labels[:, 0])
    #print(labels[:, 1])
    
    arr = labels[:, 0]
    """
    for x in arr:
        print(datetime.fromtimestamp(x))
        """
    
if __name__ == "__main__":
    main()