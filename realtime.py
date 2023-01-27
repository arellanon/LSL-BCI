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
import joblib

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    # print("[EXCEPTION] exception raised", e)
    pass

## Keyboard Interrupt handler
def keyboardInterrupt_handler(signum, frame):
    print("  key board interrupt received...")
    print("----------------Recording stopped------------------------")
    raise ServiceExit
    
def main():
    print("Inicio...")
    path_raiz = 'DATA/Experiment_4/'
    #name_model = 'Models'
    name_model = 'Models/'
    num=2736
    #path modelo
    path_model = path_raiz + name_model
    #Cargamos modelo
    model = joblib.load(path_model + '/model' + str(num) +'.pkl')
    print(model)
    
    try:
        signal.signal(signal.SIGINT, keyboardInterrupt_handler)
        print('Resolving a Control stream...')
        streams = resolve_stream('type', 'EEG')
        inlet = StreamInlet(streams[0])
        keep_alive=True
        total_data = None
        lista_ts = None
        index = 0
        while keep_alive:
            try:
                sample, timestamp = inlet.pull_sample()
                data = np.array([sample])
                data = data.transpose()
                ts = np.array(timestamp)
                index = index + 1
                if total_data is None:
                    total_data = data
                    lista_ts = ts
                    #print("Firts ts: ", datetime.fromtimestamp(timestamp))
                else:
                    total_data =  np.append(total_data, data, axis=1)
                    lista_ts = np.append(lista_ts, ts)
                if (len(total_data[0]) >= 251 ):
                    #print(total_data.shape)
                    total_data = total_data / 1000000
                    raw = loadDatos(total_data, 'ch_names.txt')
                    montage = make_standard_montage('standard_1020')
                    raw.set_montage(montage)
                    #print(raw)
                    data_raw = raw.get_data(verbose='critical')
                    data_raw = np.array( [ data_raw ] )
                    #print(data_raw.shape)
                    result=model.predict(data_raw)
                    print(result)
                    total_data = None
            except Exception as e:
                print("Error")
                sys.exit()
    except ServiceExit:
        keep_alive = False
        print("Fin...")
        sys.exit()
        
if __name__ == "__main__":
    main()