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
from tkinter import Tk, IntVar, Label, Button

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

class DataThread(threading.Thread):
    
    def __init__ (self):
        threading.Thread.__init__ (self)
        self.keep_alive = True
        self.total_data = None
        self.times = None
        self.index = 0
    
    def run(self):
        streams = resolve_stream('type', 'EEG')
        inlet = StreamInlet(streams[0])
        while self.keep_alive:
            try:
                sample, timestamp = inlet.pull_sample()
                local = local_clock()
                print("ts: ", timestamp, ": ", datetime.fromtimestamp(timestamp) ,'-',  local, ": ", datetime.fromtimestamp(local), " - ", local -  timestamp)
                data = np.array([sample])
                data = data.transpose()
                ts = np.array(timestamp)
                self.index = self.index + 1
                if self.total_data is None:
                    self.total_data = data
                    self.times = ts
                else:
                    self.total_data =  np.append(self.total_data, data, axis=1)
                    self.times = np.append(self.times, ts)
            except Exception as e:
                print("Error")
                sys.exit()
        print("Final")

def save_data(path, data):
    #convertir de uV -> V
    data = data / 1000000
    raw = loadDatos(data, 'ch_names.txt')
    montage = make_standard_montage('standard_1020')
    raw.set_montage(montage)
    raw.save(path + "/data_eeg.fif", overwrite=True)
    return raw

def save_event(path, times, labels):
    np.save(path + '/times.npy', times)
    np.save(path + '/labels.npy', labels)
    #Buscamos posicion del evento por proximidad ts
    posiciones = None
    for x in labels:
        resta = abs(times - x[0])
        pos = np.where(min(resta) == resta)[0]
        if posiciones is None:
            posiciones = pos
        else:
            posiciones = np.append(posiciones, pos)
    #Con las posiciones creamos matriz de eventos pos x zero x event
    events = np.zeros((len(labels) , 3), int)
    events[:, 0] = posiciones.astype(int)
    events[:, 2] = labels[:,1].astype(int)
    mne.write_events(path + "/event.fif", events)
    return events


class Test(threading.Thread):
    def __init__ (self, ventana, salida, config_calibration):
        threading.Thread.__init__ (self)
        self.ventana = ventana
        self.etiqueta = Label(self.ventana, text="0")
        self.etiqueta.place(x=0, y=100)
        
        self.salida = salida
        self.time_initial = config_calibration['time_initial']
        self.run_n = config_calibration['run_n']
        self.trial_per_run = config_calibration['trial_per_run']    
        self.time_trial = config_calibration['time_trial']
        self.time_pause = config_calibration['time_pause']
        self.time_pause_per_run = config_calibration['time_pause_per_run']
        self.labels=None
              
    def run(self):    
        time_fixation = 3
        #variables para sonido beep
        duration = 1  # seconds
        freq = 440  # Hz pitido
        
        for i in range(self.run_n):
            print('\nCorrida N#: ', i)
            #Se crea lista de stack
            stack = []
            left  = [0] * (self.trial_per_run // 2)
            rigth = [1] * (self.trial_per_run // 2)    
            stack = left + rigth
            print(stack)
            random.shuffle(stack)
            #print(stack)
            #time pause per run
            time.sleep(self.time_pause_per_run)
            index=0
            for x in stack:
                #time fixation
                for j in range(time_fixation):
                    #print('.', end="")
                    time.sleep(1)
                #time beep
                os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq)) #beep
                #ts = time.time()
                ts = local_clock()
                print("#", index,": ", ts, ": ", datetime.fromtimestamp(ts), ' - ', x)
                index=index+1
                label=np.array( [ [ts], [x] ] )
                if self.labels is None:
                    self.labels = label
                else:
                    self.labels = np.append(self.labels, label, axis=1)
                
                self.salida.write('\n')
                for j in range(self.time_trial):
                    if x == 0:
                        #print('+', end="")
                        #salida.write('+')
                        #etiqueta = Label(self.ventana, text=">")
                        self.etiqueta["text"] = "pause"
                    else:
                        #print('>', end="")
                        #salida.write('>')
                        #etiqueta = Label(self.ventana, text=">")
                        self.etiqueta["text"] = "rigth"
                    time.sleep(1)
                self.etiqueta["text"] = ""
                time.sleep(self.time_pause)
                
        self.labels=self.labels.transpose() #realizamos la traspuesta ts x event
        self.ventana.destroy()

def main():
    print("Inicio...")
    config_calibration = loadConfig("config.ini", "CALIBRATION")
    path = config_calibration['path']
    salida = sys.stdout
    sys.stdout = open(path + "/stdout.txt","w")
    try:
        signal.signal(signal.SIGINT, keyboardInterrupt_handler)
        print('Resolving a Control stream...')
        data_thead = DataThread()
        data_thead.start()
        #labels = test(salida, config_calibration)
        ventana = Tk()
        testPlay = Test(ventana, salida, config_calibration)
        testPlay.start()
        ventana.mainloop()
        labels = testPlay.labels
    except ServiceExit:
         data_thead.keep_alive = False
         data_thead.join()
         print("Fin...")
         sys.exit()
    finally:
         data_thead.keep_alive = False
         pos = data_thead.index
         total_data = data_thead.total_data
         times = data_thead.times
         data_thead.join()
         raw = save_data(path, total_data)
         events = save_event(path, times, labels)
         raw.plot(scalings=None, n_channels=8, events=events)
         
if __name__ == "__main__":
    main()