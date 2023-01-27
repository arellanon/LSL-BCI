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


class TrainML:

    def run(self):       
        experiment="DATA/Experiment_4/"
        pathEpoch = experiment + "Epoch/"
        pathModels = experiment + "Models/"
        accurry_max = 0
        num_max = 0
        for num in range(1, 3432):
            epochs=mne.read_epochs(pathEpoch +"Epoch"+str(num)+"-epo.fif", proj=True, preload=True, verbose=None)
            #Se carga target (convierte 1 -> -1 y 2 -> 0 )
            #target = epochs.events[:, -1] - 2
            target = epochs.events[:, -1]
            #print(epochs.events[:, -1])
            print(target)
            
            #Lo convierte a matriz numpy
            epochs_data = epochs.get_data()
            print(epochs_data.shape)
            
            #Se crea set de de pruebas y test
            X_train, X_test, y_train, y_test = train_test_split(epochs_data, target, test_size=0.2, random_state=0)
                
            #Guardamos los set de datos
            """
            np.save(path + '/X_train.npy', X_train)
            np.save(path + '/y_train.npy', y_train)
            np.save(path + '/X_test.npy', X_test)
            np.save(path + '/y_test.npy', y_test)
            """
                    
            #Clasificadores del modelo
            csp = CSP(n_components=2, reg=None, log=True, norm_trace=False)
            lda = LinearDiscriminantAnalysis()
            
            #Modelo utiliza CSP y LDA
            model = Pipeline([('CSP', csp), ('LDA', lda)])    
            print(epochs_data.shape )
            #Entrenamiento del modelo
            model.fit(X_train, y_train)
            
            score = model.score(X_train, y_train)
            print("#:", num)
            print("Score entrenamiento: ", score)

            # plot CSP patterns estimated on full data for visualization
            #csp.fit_transform(epochs_data, target)
            #csp.plot_patterns(epochs.info, ch_type='eeg', size=1.5)
            
            #Resultados
            print(X_test.shape)
            result=model.predict(X_test)
            
            #Guardamos el modelo
            joblib.dump(model, pathModels + "/model"+str(num)+".pkl")
            
            #Variables report
            ts = time.time()
            matriz=met.confusion_matrix(y_test, result)
            report=met.classification_report(y_test, result)
            accurry=met.accuracy_score(y_test, result)
            if( accurry > accurry_max ):
                accurry_max = accurry
                num_max = num
            
            #raw.plot(scalings=None, n_channels=8,  events = events_from_file)
            print("Score entrenamiento: ", accurry)
            #Mostrar report
            print(ts, ' - ', datetime.fromtimestamp(ts))
            print(matriz)
            print(report)
                
            #Archivo de salida
            fout=open(pathModels + "/output.txt","a")
            fout.write("#:"+ str(num)+ "\n")
            fout.write("Score entrenamiento: " + str(score) + "\n")
            fout.write("Acurry: " + str(accurry) + "\n")
            fout.write(str(datetime.fromtimestamp(ts)) + "\n")
            fout.write(str(matriz) + "\n")
            fout.write(str( report))
            fout.write("\n")
            fout.close()
        print(num_max, " ", accurry_max )
        fout=open(pathModels + "/output.txt","a")
        fout.write("#"+ str(num_max)+ ":" + str(accurry_max) +"\n")
        fout.write("\n")
        fout.close()

def main():
    print("Inicio...")
    train = TrainML()
    train.run()
    print("Fin...")

if __name__ == "__main__":
    main()