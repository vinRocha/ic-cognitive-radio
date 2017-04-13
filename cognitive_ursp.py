#!/usr/bin/env python
from spectrum_sensing.usrp_sense import usrpSense
import numpy as np
import time

average = 10
def avg(x): return x/average
def add(x, y): return x + y

def get_y(y): return y[1]
def get_x(x): return x[0]

samp_rate = 5e6
fft_size = 4096
fft_last = int(np.ceil(fft_size/2*0.7))
freq_step = samp_rate/fft_size

start_freq = 1240e6 + (fft_last-1)*freq_step
stop_freq  = 1300e6 - fft_last*freq_step
freq = start_freq

dev1 = usrpSense(samp_rate, freq, fft_size)
dev1.start()

spec = ()
free_channels = ()
ham = [0.] * fft_size
power = [0.] * fft_size

underThr = False
channel_size = 0
while freq <= stop_freq:
    time.sleep(0.01)
    for i in range(average):
        ham[:] = dev1.get_spec()
        power = map(add, ham, power)
        time.sleep(0.01)
    
    ham = map(avg, power)
    power = ham[-fft_last:fft_size-int(250e3/freq_step)]
    #power[fft_last-1] = (power[fft_last-2] + power[fft_last])/2

    for m in range(len(power)):
        spec = spec + ((round((m-fft_last)*freq_step+freq), power[m]),)
        if power[m] <= -150: 
          underThr = True
          channel_size += 1
        else:
          underThr = False
          channel_size = 0
        if underThr and channel_size == 1: 
          f_0 = round((m-fft_last)*freq_step+freq)
        elif underThr and channel_size == 360:
          free_channels = free_channels + ((f_0, round((m-fft_last)*freq_step+freq)),)
          channel_size = 0
    
    
    freq = freq + (len(power)+1)*freq_step
    power = [0.] * fft_size
    dev1.set_freq(freq)

del dev1

print len(free_channels)

import matplotlib.pyplot as plt
plt.ion()
plt.plot(map(get_x, spec), map(get_y, spec))
plt.axis([start_freq-1e6, stop_freq+1e6, -140, -20])
plt.grid(True)
