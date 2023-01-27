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


# A Python program to print all 
# combinations of a given length 
from itertools import combinations 
  

    

class TrainML:
    """
    def combinaciones(self, c, n):
        return [s for s in self.potencia(c) if len(s) == n]
    
    def potencia(self, c):
        if len(c) == 0:
            return [[]]
        r = self.potencia(c[:-1])
        return r + [s + [c[-1]] for s in r]
    
    def imprime_ordenado(self, c):
        for e in sorted(c, key=lambda s: (len(s), s)):
            print(e)
    """
    def run(self):
        #a = ['cereza', 'chocolate', 'fresa','nuez', 'vainilla']
        #a = np.arange(208)
        #a = np.random.permutation(200)
        #print(a)
        
        # Get all combinations of [1, 2, 3] 
        # and length 2 
        a = ["T1","T2","T3","T4","T5","T6","T7","T8","T9","T10"]
        comb = combinations(a, 4)
        
        print( (list(comb)) )
        # Print the obtained combinations 
        #for i in list(comb): 
        #    print (i)        
        """
        self.combinaciones(a, 100)
        #self.imprime_ordenado( self.combinaciones(a, 100) )
        
        path="DATA/Experiment_2/Models/"
        epochs=mne.read_epochs(path+"Experiment-epo.fif", proj=True, preload=True, verbose=None)
        #Se carga target (convierte 1 -> -1 y 2 -> 0 )
        #target = epochs.events[:, -1] - 2
        target = epochs.events[:, -1]
        #print(epochs.events[:, -1])
        epochs_data = epochs.get_data()
        print(epochs_data[207].shape)
        print(target[207])   

        """                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

def main():
    print("Inicio...")
    train = TrainML()
    train.run()
    print("Fin...")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
if __name__ == "__main__":
    main()
    
    
    
    