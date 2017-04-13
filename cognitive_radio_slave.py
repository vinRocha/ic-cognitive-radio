#!/usr/bin/env python
from burst_comm.burst_transmitter import burst_transmitter
from burst_comm.burst_receiver import burst_receiver
from burst_comm.udp_send import send
from burst_comm.udp_receive import receive
import time

class CognitiveRadio:
  
  def __init__(self):
    self.freq = 0.0
    self.msg = None
  
  def send_burst(self, MESSAGE):
    for i in range(10):
      send(MESSAGE)
      time.sleep(0.5)
  
  def get_frequency(self):
    self.receiver = burst_receiver(1241e6)
    self.receiver.start()
    print 'waiting for frequency...'
    while self.msg == None:
      self.msg = receive(10)
      print 'received freq[kHz]:', self.msg
    self.receiver.stop()
    self.receiver.wait()
    del self.receiver
    time.sleep(3)
    self.freq = float(self.msg)
    self.transmitter = burst_transmitter(1241e6)
    self.transmitter.start()
    print 'sending ack...'
    self.send_burst('ACK_FREQ')
    self.transmitter.stop()
    self.transmitter.wait()
    del self.transmitter
    time.sleep(1)
  
  def listen(self):
    self.receiver = burst_receiver(self.freq*1000)
    self.receiver.start()
    print 'operating at', str(self.freq) + 'kHz'
    print 'waiting for PDU...'
    self.msg = receive(10)
    self.receiver.stop()
    self.receiver.wait()
    del self.receiver
    time.sleep(3)
    print 'received:', self.msg
    if self.msg == None: 
      self.get_frequency()
    else:
      self.transmitter = burst_transmitter(self.freq*1000)
      self.transmitter.start()
      print 'sending ack...'
      self.send_burst('ACK_PDU')
      self.transmitter.stop()
      self.transmitter.wait()
      del self.transmitter
      time.sleep(1)
  
  def start_op(self):
    self.get_frequency()
    while True:
      self.listen()

def main():
  cr = CognitiveRadio()
  cr.start_op()

if __name__ == '__main__':
  main()
