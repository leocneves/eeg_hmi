#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EEG HMI JUDITH.

Usage:
  experiment.py subject <name> mooth <state>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from emokit.emotiv import Emotiv
from docopt import docopt
import os
import time
import numpy as np
import subprocess

class Experiment():
  def __init__(self, arguments):
    self.args = arguments
    self.path = "~/Documents/eeg_hmi/dataset/happiness"
    self.time = 0
    # Experiment variables
    self.init_time = 10
    self.clip_time = 240
    self.questions_time = 40
    self.step = 0
    self.rest_time = 10
    self.num_clips = 1
    self.count = 0
    self.c = 0

    if self.args['mooth']:
      if (self.args['<state>'] == 'happiness'):
        self.path = "~/Documents/eeg_hmi/dataset/happiness"
      elif (self.args['<state>'] == 'sadness'):
        self.path = "~/Documents/eeg_hmi/dataset/sadness"
      elif (self.args['<state>'] == 'neutral'):
        self.path = "~/Documents/eeg_hmi/dataset/neutral"
    else:
        print "default mooth: happiness setted!"
        pass

  def main(self):
    with Emotiv(display_output=False, verbose=False, write=True, output_path="/home/leonardo/Documents/eeg_hmi/signals") as emotiv:
      self.time = time.time()
      while emotiv.running:
            try:
                packet = emotiv.dequeue()
                print np.round((time.time()-self.time),0)
                if (np.round((time.time()-self.time),2) == 0 and self.c == 0):
                  # os.system("gnome-terminal -e 'bash -c \"cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/black.jpg &; exec bash\"'")
                  # os.system("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/black.jpg &")
                  subprocess.Popen("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/black.jpg &", shell=True)

                if ((np.round((time.time()-self.time),0) == self.init_time+self.step)and self.c == 1):
                  # os.system("gnome-terminal -e 'bash -c \"cvlc --fullscreen "+self.path+"/"+str(self.count)+".mp4 &; exec bash\"'")
                  # os.system("cvlc --fullscreen "+self.path+"/"+str(self.count)+".mp4 &")
                  subprocess.Popen("cvlc --fullscreen "+self.path+"/"+str(self.count)+".mp4 &", shell=True)

                if ((np.round((time.time()-self.time),0) == (self.init_time+self.clip_time)+self.step) and self.c == 2):
                  os.system("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/SAM.png &")

                if ((np.round((time.time()-self.time),0) == (self.init_time+self.clip_time+self.questions_time)+self.step)and self.c == 3):
                  os.system("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/black.jpg &")

                if ((np.round((time.time()-self.time),0) == (self.init_time+self.clip_time+self.questions_time+self.rest_time)+self.step)and self.c == 4):
                  if (self.count < self.num_clips):
                    self.count+=1
                    self.step = self.step + (self.init_time+self.clip_time+self.questions_time+self.rest_time)
                  else:
                    os.system("pkill -f vlc &")
                    emotiv.stop() #stop experiment

            except Exception:
                emotiv.stop()
            time.sleep(0.001)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='EEG HMI JUDITH 1.0')
    try:
      exp = Experiment(arguments)
      exp.main()
    except Exception as e:
      print e