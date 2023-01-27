#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 23:59:47 2020

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
from itertools import combinations


class GenerateEpoch:

    def run(self):
        tmin = 0.5
        tmax = 1.5
                
        print("tmin: ",tmin," - tmax: ", tmax )
        # event_id
        event_id = {'right': 1, 'left': 0}
        experiment = "DATA/Experiment_4/"
        pathData = experiment + "Data/"
        pathEpoch = experiment + "Epoch/"

        dataTrial = ["T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11","T2","T13","T14"]
        #dataTrial = ["T1","T2","T3","T4"]
        
        comb = combinations(dataTrial, 7)
        comb_list = [ list(t) for t in comb ]
        print(comb_list)
        num=1
        
        for trials in comb_list:
            print(trials)
            epochs = []
            for trial in trials:
                path= pathData + trial
                raw = mne.io.read_raw_fif(path + "/data_eeg.fif", preload=True, verbose=False)
                events = mne.read_events(path + "/data-eve.fif", verbose=False)
                #Se genera las epocas con los datos crudos y los eventos
                epoch = mne.Epochs(raw, events=events, event_id=event_id, tmin=tmin, tmax=tmax, baseline=None, preload=True, verbose=False)
                epochs.append(epoch)
            epoch_final=mne.concatenate_epochs(epochs, add_offset=True, on_mismatch='raise', verbose=None)
            print(epoch_final)
            epoch_final.save(pathEpoch + "Epoch"+str(num)+"-epo.fif", overwrite=True)
            num+=1

def main():
    print("Inicio...")
    generate = GenerateEpoch()
    generate.run()
    print("Fin...")

if __name__ == "__main__":
    main()