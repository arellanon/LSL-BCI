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

        #trials = ["T1","T2","T3","T6","T11","T12","T13"]
        trials = ["T1","T2","T3","T4","T5","T6","T7"]
        epochs = []
        
        for trial in trials:
            path= pathData + trial
            raw = mne.io.read_raw_fif(path + "/data_eeg.fif", preload=True)
            events = mne.read_events(path + "/data-eve.fif")
            print(events)
            #print(len(event_new))
            #Se genera las epocas con los datos crudos y los eventos
            epoch = mne.Epochs(raw, events=events, event_id=event_id, tmin=tmin, tmax=tmax, baseline=None, preload=True, verbose=False)
            epochs.append(epoch)
        epoch_final=mne.concatenate_epochs(epochs, add_offset=True, on_mismatch='raise', verbose=None)
        print(epoch_final)
        epoch_final.save(pathEpoch + 'Experiment-epo.fif', overwrite=True)

def main():
    print("Inicio...")
    generate = GenerateEpoch()
    generate.run()
    print("Fin...")

if __name__ == "__main__":
    main()