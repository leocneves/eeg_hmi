#!/usr/bin/env python
import pandas as pd
import numpy as np

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

# USAGE
# from processing.Processing import Processing
# import pandas as pd
# df = pd.read_csv('/home/leonardo/Documents/eeg_hmi/signals/leo')
# x = Processing()
# w = x.epoch(df,10,250,1,1,'true')

#plot
# import matplotlib.pyplot as plt
# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')
# plt.show()

# import matplotlib.pyplot as plt
# plt.plot([1,2],[1,2])
# plt.show()
# plt.plot(w[0][:,0],w[0][:,1])
# plt.show()
# plt.plot(w[1][:,0],w[1][:,1])
# plt.show()
