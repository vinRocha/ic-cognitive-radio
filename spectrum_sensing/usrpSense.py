#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Usrpsense
# Author: Vinicius Rocha da Silva
# Description: measures the rf spectrum for an desired frequency range.
# Generated: Tue Mar 28 16:14:33 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import time


class usrpSense(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Usrpsense")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 4e6
        self.freq = freq = 1240e6
        self.fft_size = fft_size = 2048

        ##################################################
        # Blocks
        ##################################################
        self.vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fft_size)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(10, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_float*1, fft_size)
        self.stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.multiply_const_0 = blocks.multiply_const_vcc((1./fft_size, ))
        self.log10_0 = blocks.nlog10_ff(10, 1, 0)
        self.freq_sink = blocks.probe_signal_vf(fft_size)
        self.fft_0 = fft.fft_vcc(fft_size, True, (), False, 0)
        self.complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.complex_to_mag_squared_0, 0), (self.log10_0, 0))    
        self.connect((self.fft_0, 0), (self.vector_to_stream_0, 0))    
        self.connect((self.log10_0, 0), (self.stream_to_vector_1, 0))    
        self.connect((self.multiply_const_0, 0), (self.complex_to_mag_squared_0, 0))    
        self.connect((self.stream_to_vector_0, 0), (self.fft_0, 0))    
        self.connect((self.stream_to_vector_1, 0), (self.freq_sink, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.stream_to_vector_0, 0))    
        self.connect((self.vector_to_stream_0, 0), (self.multiply_const_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self.multiply_const_0.set_k((1./self.fft_size, ))


def main(top_block_cls=usrpSense, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
