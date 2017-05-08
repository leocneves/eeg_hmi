#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EEG HMI JUDITH.

Usage:
  experiment.py subject <name> mooth <state>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import os
import time

class Experiment():
  def __init__(self, arguments):
    self.args = arguments
    self.path = ''
    self.time = 0
    # Experiment variables
    self.init_time = 10
    self.clip_time = 240
    self.questions_time = 40
    self.step = 0
    self.rest_time = 10
    self.num_clips = 1
    self.count = 0

    if self.args['mooth']:
      if (self.args['<state>'] == 'happiness'):
        self.path = "~/Documents/eeg_hmi/dataset/happiness"
      elif (self.args['<state>'] == 'sadness'):
        self.path = "~/Documents/eeg_hmi/dataset/sadness"
      elif (self.args['<state>'] == 'neutral'):
        self.path = "~/Documents/eeg_hmi/dataset/neutral"
    else:
      pass

  def main(self):
    with Emotiv(display_output=False, verbose=False, write=True, output_path="~/Documents/eeg_hmi/signals") as emotiv:
      while emotiv.running:
            try:
                packet = emotiv.dequeue()
                self.time = time.time()

                if (self.time == 0):
                  os.system("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/black.jpg &")

                if (self.time == self.init_time+self.step):
                  os.system("cvlc --fullscreen "+self.path+"/"+str(self.count)+".mp4 &")

                if (self.time == (self.init_time+self.clip_time)+self.step):
                  os.system("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/SAM.png &")

                if (self.time == (self.init_time+self.clip_time+self.questions_time)+self.step):
                  os.system("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/black.jpg &")

                if (self.time == (self.init_time+self.clip_time+self.questions_time+self.rest_time)+self.step):
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
    except:
      print "ERROR"