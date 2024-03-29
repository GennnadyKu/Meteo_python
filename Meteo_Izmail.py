from tkinter import *
#from tkinter.filedialog import FileDialog
import requests
import numpy as np
import pandas as pd
from io import StringIO


# extract values ​​from the data of any field
def extract_data(field):
    temp_dict = r_field(field)
    #print(temp_dict)
    #r_data_all = temp_dict.values()
    #print(r_data_all)
    r_data = str(list(temp_dict.values())[47])
    return r_data

def extract_data_all(field):
    temp_dict = r_field(field)
    #print(temp_dict)
    #r_data_all = temp_dict.values()
    #print(r_data_all)
    #r_data = str(list(temp_dict.values())[:23])
    r_data = [max(list(temp_dict.values())[:47]), min(list(temp_dict.values())[:47])]
    return r_data

#Read data from single field of channel with HTTP GET
def r_field(field):
    s_field = str(field) 
    #s_results = str(results)

    #thingspeak_m = f"https://api.thingspeak.com/channels/1283823/fields/{s_field}.csv?results=1&timezone=Europe/Kiev"  
    thingspeak_m = f"https://api.thingspeak.com/channels/1283823/fields/{s_field}.csv?results=48&timezone=Europe/Kiev"  
    response = requests.get(thingspeak_m)
    #response2 = requests.get("https://api.thingspeak.com/channels/1283823/fields/1.csv?results=1&timezone=Europe/Kiev")
    my_data = StringIO(response.text) #
    data_6 = pd.read_csv(my_data, sep=",") # cannel data as csv
    #print(data_6)
    data_6n = data_6.to_numpy() # csv tu numpy array
    row = 0
    temp1mass = np.zeros((48))
    ret_dict = {}
    for i in range(len(data_6)):
        #if (data_6n[i,2] < 0) or (data_6n[i,2] >0) :
        temp1mass[row] = data_6n[i,2]
        ret_dict.update({data_6n[i,0]: temp1mass[row]})
        row = row+1
    #print(ret_dict)
    return(ret_dict) # return a dictionary in the form date-time : value   

# extract time from field1 data
def extract_time():
    temp_dict = r_field(1)
    time_read = list(temp_dict.keys())[47] # extract time
    tmr = time_read.split()[1]
    return(tmr)



class MeteoLabel:
    def __init__(self, master, parameter, name):
        self.parameter = parameter
        self.lab = Label(master, width=30,
                         bg='lavender')
        self.name = name 
        self.lab.pack()
        self.update_data()

    def update_data(self):
        text = self.name + ': ' + self.parameter.get()
        self.lab.configure(text=text)
        self.lab.after(600000, self.update_data)

class MeteoGraph:
    def __init__(self, master, parameter, name):
        self.parameter = parameter
        self.lab = Label(master, width=30,
                         bg='lavender')
        self.name = name 
        self.lab.pack()
        self.update_data()

    def update_data(self):
        text_all = self.name +': ' + str((extract_data_all(1))[0]) + '/' + str((extract_data_all(1))[1]) +' C'
                        

        print (text_all) 
        #text = self.name + ': ' + self.parameter.get()
        self.lab.configure(text=text_all)
        self.lab.after(600000, self.update_data)



class Temperature:
    def get(self):
        return extract_data(1) + ' C' # returns '34 C'

class Humidity:
    def get(self):
        return extract_data(2) + ' %' # returns '100 %'

class Pressure:
    def get(self):
        return extract_data(3) + ' hP' # returns '1000  hP'    

class TimeLabel:
    def __init__(self, master):
        self.lab = Label(master, width=30,
                         bg='lavender')
        self.lab.pack()
        self.update_data()

    def update_data(self):
        self.lab['bg'] = 'mistyrose'
        self.lab.configure(text='Time: ' + extract_time())
        self.lab.after(600000, self.update_data)


root = Tk()
root.title("Meteo Izmail now")
root.wm_attributes("-topmost", 1)


MeteoLabel(root, Temperature(), 'Temperature')
MeteoLabel(root, Humidity(), 'Humidity')
MeteoLabel(root, Pressure(), 'Pressure')
TimeLabel(root)
MeteoGraph(root, Temperature(), 'Temperature max/min')

root.mainloop()