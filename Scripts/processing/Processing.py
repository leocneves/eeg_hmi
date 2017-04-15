#!/usr/bin/env python
import pandas as pd
import numpy as np
from scipy import signal


class Processing:
    """docstring for Processing"""
    def __init__(self):
        data = 0

    def epoch(self,data,init_time,end,epoch,offset,time):
        # Def to slice a data frame into epochs
        self.window = data[(data['Time (s)']>=init_time) & (data['Time (s)']<=end)]  #making a epoch
        # print self.window
        self.names = data.keys()
        aux = 0
        sla = list()
        if ((end - init_time)%epoch) != 0:
            return "OFFSET ERROR"
        else:
            for x in range(1,(int(max(self.window['Time (s)'])-init_time)+1),1):
                if time == 'false':
                    sla.append(self.window[(self.window['Time (s)']>=init_time+aux) & (self.window['Time (s)']<init_time+x)].ix[:,[1,2,3,4]].values)
                else:
                    sla.append(self.window[(self.window['Time (s)']>=init_time+aux) & (self.window['Time (s)']<init_time+x)].ix[:,[0,1,2,3,4]].values)
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

# USAGE
# from processing.Processing import Processing
# import pandas as pd
# df = pd.read_csv('/home/leonardo/Documents/eeg_hmi/signals/leo')
# x = Processing()
# w = x.epoch(df,10,250,1,1,'true')

# plot
# import matplotlib.pyplot as plt
# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')
# plt.show()

# import matplotlib.pyplot as plt
# plt.plot(w[0][:,0],w[0][:,1])
# plt.show()
