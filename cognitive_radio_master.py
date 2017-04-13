#!/usr/bin/env python
from spectrum_sensing.cognitive_sense import sense as get_free_channels
from burst_comm.burst_transmitter import burst_transmitter
from burst_comm.burst_receiver import burst_receiver
from burst_comm.udp_send import send
from burst_comm.udp_receive import receive
from random import randrange
import numpy as np
import time

class CognitiveRadio:
  
  def __init__(self):
    self.freq = 0.0
    self.msg = None
    self.free_channels = []
    self.i = 20
  
  def send_burst(self, MESSAGE):
    for i in range(10):
      send(MESSAGE)
      time.sleep(0.1)
  
  def send_frequency(self):
    while self.msg == None:
      self.transmitter = burst_transmitter(1241e6)
      self.transmitter.start()
      print 'sending channel frequency:', str(self.freq), '...'
      self.send_burst(str(self.freq))
      self.transmitter.stop()
      self.transmitter.wait()
      del self.transmitter
      time.sleep(1)
      self.receiver = burst_receiver(1241e6)
      self.receiver.start()
      print 'waiting for ack...'
      self.msg = receive(10)
      self.receiver.stop() 
      self.receiver.wait()
      del self.receiver
      time.sleep(6)
      print 'received:', self.msg
      
  def get_freq(self):
    r = randrange(len(self.free_channels))
    self.freq = self.free_channels.pop(r)
    self.freq = round((self.freq[0] + self.freq[1])/2000.)
    self.send_frequency()
  
  def talk(self):
    self.transmitter = burst_transmitter(self.freq*1000)
    self.transmitter.start()
    print 'operating at', str(self.freq) + 'kHz'
    print 'sending PDU...'
    self.send_burst(self.f[self.i])
    self.transmitter.stop()
    self.transmitter.wait()
    del self.transmitter
    time.sleep(1)
    self.receiver = burst_receiver(self.freq*1000)
    self.receiver.start()
    self.msg = receive(10)
    self.receiver.stop()
    self.receiver.wait()
    del self.receiver
    time.sleep(6)
    print self.msg
    if self.msg == None:
      self.get_freq()
    else:
      self.i += 1
  
  def start_op(self):    
    print 'determining free channels'
    self.free_channels = get_free_channels(1240e6, 1300e6, -95)
    print 'free_channels found:', str(len(self.free_channels))
    self.get_freq()
    self.send_frequency()
    while True:
      self.talk()

def main():
  cr = CognitiveRadio()
  cr.f = open('alice.txt', 'r').readlines()
  cr.start_op()

if __name__ == '__main__':
  main()
