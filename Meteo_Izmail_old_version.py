from tkinter import *
from tkinter.filedialog import FileDialog
import requests
import numpy as np
import pandas as pd
from io import StringIO


class Meteo_st:
    def __init__(self, master, parameter):
        self.parameter = parameter
        self.lab = Label(master, width=20,
                         bg='lavender')
        self.lab.pack()
        self.update_data()
        
    # update all data after 10 minutes    
    def update_data(self): 
        if self.parameter == 'temperature':
            self.temperature()
        elif self.parameter == 'humidity':
            self.humidity()
        elif self.parameter == 'pressure':
            self.pressure()
        else:
            self.extract_time()
        self.lab.after(600000, self.update_data)
        
    def temperature(self): #form text for temperature (field 1)
        temper = 't grad C: ' + self.extract_data(1)
        self.lab.configure(text=temper) # change the label text
        
    def humidity(self): # field 2 Thingspeak
        hum = 'Humidity: ' + self.extract_data(2)
        self.lab.configure(text=hum)
        
    def pressure(self): # field 3  Thingspeak
        press = 'Pressure: ' + self.extract_data(3)
        self.lab.configure(text=press)    
    
    # extract time from field1 data
    def extract_time(self):
        temp_dict = self.r_field(1)
        time_read = list(temp_dict.keys())[0] # extract time
        tmr = "Measured at: " + time_read.split()[1]
        self.lab['bg'] = 'mistyrose'
        self.lab.configure(text=tmr) # change the label text
    
    # extract values ​​from the data of any field
    def extract_data(self, field):
        temp_dict = self.r_field(field)
        r_data = str(list(temp_dict.values())[0])
        return r_data

    #Read data from single field of channel with HTTP GET
    def r_field(self, field):
        s_field = str(field) 
        #thingspeak_m =  thingspeak_c1 + thingspeak_c2 + thingspeak_c3 # form URL(last result)  
        thingspeak_m = f"https://api.thingspeak.com/channels/1283823/fields/{s_field}.csv?results=1&timezone=Europe/Kiev"  
        response = requests.get(thingspeak_m)
        #response2 = requests.get("https://api.thingspeak.com/channels/1283823/fields/1.csv?results=1&timezone=Europe/Kiev")
        my_data = StringIO(response.text) #
        data_6 = pd.read_csv(my_data, sep=",") # cannel data as csv
        #print(data_6)
        data_6n = data_6.to_numpy() # csv tu numpy array
        temp1mass = np.zeros((1))
        temp1mass[0] = data_6n[0,2]
        ret_dict = {data_6n[0,0]: temp1mass[0]}
        return(ret_dict) # return a dictionary in the form date-time : value       
        
        

root = Tk()
root.title("Meteo Izmail now")

line_1 = Meteo_st(root, 'temperature')
line_2 = Meteo_st(root, 'humidity')
line_3 = Meteo_st(root, 'pressure')
line_4 = Meteo_st(root, 'time')
    
root.mainloop()