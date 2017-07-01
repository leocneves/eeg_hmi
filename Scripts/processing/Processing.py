#!/usr/bin/env python
import pandas as pd
import numpy as np
import time
import datetime
from scipy import signal

# USAGE
# from processing.Processing import Processing
# import pandas as pd
# df = pd.read_csv('/home/leonardo/Documents/eeg_hmi/signals/<file.csv>')
# x = Processing()
# w = x.epoch(df,0,2,1,1,['Time (s)','AF4 Value'])

# import matplotlib.pyplot as plt
# plt.plot(w[0][:,0],w[0][:,1])
# plt.show()


class Processing:
    """docstring for Processing"""
    def __init__(self):
        data = 0

    def epoch(self,data,init_time,end,epoch,offset,chanels):
        time_col = list()
        reset_time = int(data['Timestamp'][0].split(' ')[1].split(':')[1])*60 + float(data['Timestamp'][0].split(' ')[1].split(':')[2])
        for t in data['Timestamp']:
            time_col.append((int(t.split(' ')[1].split(':')[1])*60 + float(t.split(' ')[1].split(':')[2])) - reset_time)
            # time_col.append(time.strptime(t.split(' ')[1].split('.')[0],'%H:%M:%S'))
        data['Time (s)'] = time_col

        # Def to slice a data frame into epochs
        self.window = data[(data['Time (s)']>=init_time) & (data['Time (s)']<=end)]  #making a epoch
        # print self.window
        self.names = list(data.keys())
        index = list()
        for x in chanels:
            index.append(self.names.index(x))

        aux = 0
        sla = list()
        if ((end - init_time)%epoch) != 0:
            return "OFFSET ERROR"
        else:
            for x in range(1,(int(np.round(max(self.window['Time (s)'])-init_time,1))+1),1):
                sla.append(self.window[(self.window['Time (s)']>=init_time+aux) & (self.window['Time (s)']<init_time+x)].ix[:,index].values)
                aux = x
            return sla

    def rms(self, a):
        return np.sqrt(np.mean(np.square(a)))

    def filter(self, x, lowcut, highcut, btype='bandpass', sampling_rate=512, order=4):
        nyq = 0.5 * sampling_rate
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype=btype)
        return signal.filtfilt(b, a, x)

    def ZeroCrossing(self, data, channel=1):
        feature = list()
        D=0
        X1=0
        X2=0
        for x in data:
            for z in range(2,len(x)):
                if (x[z][channel] >= 0):
                    X2 = 1
                else:
                    X2 = 0
                if (x[z-1][channel]>= 0):
                    X1 = 1
                else:
                    X1 = 0
                D += np.square(X2 - X1)
            feature.append(D)
            D = 0
        return feature
