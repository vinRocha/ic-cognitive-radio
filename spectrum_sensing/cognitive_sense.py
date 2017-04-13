#!/usr/bin/env python
from usrp_sense import usrpSense
import numpy as np
import time

#def get_y(y): return y[1]
#def get_x(x): return x[0]

average = 10
def avg(x): return x/average
def add(x, y): return x + y

samp_rate = 5e6
fft_size = 4096
fft_last = int(np.ceil(fft_size/2*0.7))
freq_step = samp_rate/fft_size

def sense(freq, stop_freq, thr):
  freq = freq + (fft_last-1)*freq_step
  stop_freq = stop_freq- fft_last*freq_step
  dev1 = usrpSense(samp_rate, freq, fft_size)
  dev1.start()
  
  spec = ()
  free_channels = []
  ham = [0.] * fft_size
  power = [0.] * fft_size
  
  underThr = False
  channel_size = 0
  while freq < stop_freq:
      time.sleep(0.01)
      for i in range(average):
          ham[:] = dev1.get_spec()
          power = map(add, ham, power)
          time.sleep(0.01)

      ham = map(avg, power)
      power = ham[-fft_last+1:fft_size]
      power = power + ham[0:fft_last+1]
      #power[fft_last-1] = (power[fft_last-2] + power[fft_last])/2
  
      for m in range(len(power)):
          spec = spec + ((round((m-fft_last+1)*freq_step+freq), power[m]),)
          if power[m] <= thr:
            underThr = True
            channel_size += 1
          else:
            underThr = False
            channel_size = 0
          if underThr and channel_size == 1: 
            f_0 = round((m-fft_last+1)*freq_step+freq)
          elif underThr and channel_size == 360:
            free_channels = free_channels + [(f_0, round((m-fft_last+1)*freq_step+freq))]
            channel_size = 0
      
      freq = freq + 2*fft_last*freq_step
      power = [0.] * fft_size
      dev1.set_freq(freq)
  
  dev1.stop()
  dev1.wait()
  del dev1
  return free_channels

'''
import matplotlib.pyplot as plt
plt.ion()
plt.plot(map(get_x, spec), map(get_y, spec))
plt.axis([88e6-1e6, 108e6+1e6, -120, -20])
plt.grid(True)
'''
