# we use numpy to compute the mean of an array of values
#import numpy
import socket

# let's define a new box class that inherits from OVBox
class MyOVBox(OVBox):
   def __init__(self):
      OVBox.__init__(self)
      # we add a new member to save the signal header information we will receive
      self.signalHeader = None
      self.time = 0
      print "FOI"
      self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      #host = socket.gethostname()
      self.host = '10.0.2.2'
      self.port = 31000
      self.msg = "neutral"
      self.s.connect((self.host, self.port))
      # The process method will be called by openvibe on every clock tick
   def process(self):
      # we iterate over all the input chunks in the input buffer
      for chunkIndex in range( len(self.input[0]) ):
         # if it's a header we save it and send the output header (same as input, except it has only one channel named 'Mean'
         if(type(self.input[0][chunkIndex]) == OVStreamedMatrixHeader):
            self.signalHeader = self.input[0].pop()
            if self.signalHeader >= 0.7:
              print "ok"
              try:
                 print "entrou try"
                 self.s.send(self.msg)
                 #data = s.recv(1024)
                 #s.close()
              except ValueError:
                 print "ROS Connection Error"
   def unitialize(self):
      self.s.close()
# Finally, we notify openvibe that the box instance 'box' is now an instance of MyOVBox.
# Don't forget that step !!
box = MyOVBox()
