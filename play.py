#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 16:22:49 2021

@author: nahuel
"""
from tkinter import Tk, IntVar, Label, Button
import threading
import time

class Test(threading.Thread):
    def __init__ (self, ventana):
        threading.Thread.__init__ (self)
        self.ventana = ventana
        self.etiqueta = Label(self.ventana, text="0")
        self.etiqueta.place(x=0, y=70)
        self.salida = "chau!!!"
              
    def run(self):
        listxt = ['hola', 'mundo', 'chau', 'mundo']
        for x in listxt:
            time.sleep(1)
            self.etiqueta["text"] = x
        self.ventana.destroy()
        #threading.Thread._stop
        #process.terminate() 

        
def main():
    ventana = Tk()   
    testPlay = Test(ventana)
    testPlay.start()
    ventana.mainloop()
    salida = testPlay.salida    
    #    testPlay.join()
    print(salida)
    
if __name__ == "__main__":
    main()