import os

class MyOVBox(OVBox):
  def __init__(self):
    OVBox.__init__(self)
  def initialize(self):
    self.time = 0
    self.path=""
    self.count = 1
    self.step = 0

    # Getting params from openvibe box
    stim_label1 = self.setting['Stim']
    self.num_clips = int(self.setting['Number of clips'])
    self.type_clips = (self.setting['Type of Emotion'])
    self.init_time = int(self.setting['Start Time'])
    self.clip_time = int(self.setting['Video Clip Time'])
    self.questions_time = int(self.setting['Questions Time'])
    self.rest_time = int(self.setting['Rest Time'])

    #### Stimulations ####
    #stop experiment
    self.stim_stop = OpenViBE_stimulation[stim_label1]
    #target stim
    self.stim_target = OpenViBE_stimulation['OVTK_StimulationId_Target']
    #non target stim
    self.stim_nontarget = OpenViBE_stimulation['OVTK_StimulationId_NonTarget']

    self.output[0].append(OVStimulationHeader(0., 0.))

    if (self.type_clips == 'happiness'):
      self.path = "~/Documents/eeg_hmi/dataset/happiness"
    elif (self.type_clips == 'sadness'):
      self.path = "~/Documents/eeg_hmi/dataset/sadness"
    elif (self.type_clips == 'neutral'):
      self.path = "~/Documents/eeg_hmi/dataset/neutral"

  def process(self):
        self.time = self.getCurrentTime()
        print self.time
        stimSet_stop = OVStimulationSet(self.getCurrentTime(),self.getCurrentTime()+1./self.getClock())
        stimSet_target = OVStimulationSet(self.getCurrentTime(),self.getCurrentTime()+1./self.getClock())
        stimSet_nontarget = OVStimulationSet(self.getCurrentTime(),self.getCurrentTime()+1./self.getClock())

        if (self.time == 0):
          stimSet_nontarget.append(OVStimulation(self.stim_nontarget, self.getCurrentTime(), 0.))
          self.output[0].append(stimSet_nontarget)
          os.system("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/black.jpg &")

        if (self.time == self.init_time+self.step):
          stimSet_target.append(OVStimulation(self.stim_target, self.getCurrentTime(), 0.))
          self.output[0].append(stimSet_target)
          os.system("cvlc --fullscreen "+self.path+"/"+str(self.count)+".mp4 &")

        if (self.time == (self.init_time+self.clip_time)+self.step):
          stimSet_nontarget.append(OVStimulation(self.stim_nontarget, self.getCurrentTime(), 0.))
          self.output[0].append(stimSet_nontarget)
          os.system("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/SAM.png &")
        if (self.time == (self.init_time+self.clip_time+self.questions_time)+self.step):
          os.system("cvlc --fullscreen --loop ~/Documents/eeg_hmi/dataset/black.jpg &")

        if (self.time == (self.init_time+self.clip_time+self.questions_time+self.rest_time)+self.step):
          if (self.count < self.num_clips):
            self.count+=1
            self.step = self.step + (self.init_time+self.clip_time+self.questions_time+self.rest_time)
          else:
            stimSet_stop.append(OVStimulation(self.stim_stop, self.getCurrentTime(), 0.))
            self.output[0].append(stimSet_stop)
            os.system("pkill -f vlc &")

box = MyOVBox()