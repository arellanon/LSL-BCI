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
from wurlitzer import pipes

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

class DataThread (threading.Thread):
    
    def __init__ (self):
        threading.Thread.__init__ (self)
        self.keep_alive = True
        self.total_data = None
        self.lista_ts = None
        self.index = 0
    
    def run (self):
        streams = resolve_stream('type', 'EEG')
        inlet = StreamInlet(streams[0])
        while self.keep_alive:
            try:
                sample, timestamp = inlet.pull_sample()
                print("ts: ", datetime.fromtimestamp(timestamp) ,'-',  datetime.fromtimestamp(local_clock())  )
                #print(*a, file=sys.stdout)
                data = np.array([sample])
                #print(data.shape)
                data = data.transpose()
                #print(data.shape)
                ts = np.array(timestamp)
                self.index = self.index + 1
                if self.total_data is None:
                    self.total_data = data
                    self.lista_ts = ts
                else:
                    self.total_data =  np.append(self.total_data, data, axis=1)
                    self.lista_ts = np.append(self.lista_ts, ts)
                    #print(self.lista_ts.shape)
            except Exception as e:
                print("Error")
                sys.exit()
        print("Final")        

def save(config_calibration, data, lista_ts, labels):
    path = config_calibration['path']
    posiciones = None
    print(data)
    print(type(data))
    #convertir de uV -> V
    data = data / 1000000
    raw = loadDatos(data, 'ch_names.txt')
    montage = make_standard_montage('standard_1020')
    raw.set_montage(montage)
    print(raw)
    
    raw.save(path + "/data_eeg.fif", overwrite=True)
    np.save(path + '/lista_ts.npy', lista_ts)
    np.save(path + '/labels.npy', labels)
    print(lista_ts)
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
    

def test(salida, config_calibration):
    time_initial = config_calibration['time_initial']
    run_n = config_calibration['run_n']
    trial_per_run = config_calibration['trial_per_run']    
    time_trial = config_calibration['time_trial']
    time_pause = config_calibration['time_pause']
    time_pause_per_run = config_calibration['time_pause_per_run']
    
    #run_n = 1
    #trial_per_run = 40
    #run_n = 1
    #trial_per_run = 4
    #time_trial = 4<class 'NoneType'>

    #time_pause = 4
    #time_pause_per_run = 20
    
    time_fixation = 3
    
    labels=None
    
    #variables para sonido beep
    duration = 1  # seconds
    freq = 440  # Hz pitido
    
    for i in range(run_n):
        print('\nCorrida N#: ', i)
        #Se crea lista de stack
        stack = []
        left  = [0] * (trial_per_run // 2)
        rigth = [1] * (trial_per_run // 2)    
        stack = left + rigth
        print(stack)
        random.shuffle(stack)
        #print(stack)
        #time pause per run
        time.sleep(time_pause_per_run)
        for x in stack:
            #time fixation
            for j in range(time_fixation):
                #print('.', end="")
                time.sleep(1)
            #time beep
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq)) #beep
            #ts = time.time()
            ts = local_clock()
            print()
            print(x, ' ', ts, '-', type(ts), ' - ', datetime.fromtimestamp(ts))
            label=np.array( [ [ts], [x] ] )
            if labels is None:
                labels = label
            else:
                labels = np.append(labels, label, axis=1)
            
            salida.write('\n')
            for j in range(time_trial):
                if x == 0:
                    #print('+', end="")
                    salida.write('+')
                else:
                    #print('>', end="")
                    salida.write('>')
                time.sleep(1)
            time.sleep(time_pause)
    
    labels=labels.transpose() #realizamos la traspuesta ts x event
    return labels

def main(salida):
    print("Inicio...")
    config_calibration = loadConfig("config.ini", "CALIBRATION")
    try:
        signal.signal(signal.SIGINT, keyboardInterrupt_handler)
        print('Resolving a Control stream...')
        data_thead = DataThread()
        data_thead.start()
        labels = test(salida, config_calibration)
        #time.sleep(1)
    except ServiceExit:
        data_thead.keep_alive = False
        data_thead.join()
        print("Fin...")
        sys.exit()
    finally:
        data_thead.keep_alive = False
        pos = data_thead.index
        total_data = data_thead.total_data
        lista_ts = data_thead.lista_ts
        data_thead.join()
        save(config_calibration, total_data, lista_ts, labels)
        print("pos final: ", pos)
        print("labels: ", labels)

if __name__ == "__main__":
    salida = sys.stdout
    sys.stdout = open("output.txt","w")
    main(salida)
    #Archivo de salida
    #fout=open("output.txt","a")
    #fout.write(sys.stdout)
    #fout.close()
