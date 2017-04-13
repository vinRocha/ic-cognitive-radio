#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Rtlsense
# Author: Vinicius Rocha da Silva
# Description: measures the rf spectrum for an desired frequency range.
# Generated: Tue Mar 21 18:18:10 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr


class RtlSense(gr.top_block):

    def __init__(self, samp_rate, freq, fft_size):
        gr.top_block.__init__(self, "Rtlsense")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate
        self.freq = freq
        self.fft_size = fft_size

        ##################################################
        # Blocks
        ##################################################
        self.vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fft_size)
        self.stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_float*1, fft_size)
        self.stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.src_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.src_0.set_sample_rate(samp_rate)
        self.src_0.set_center_freq(freq, 0)
        self.src_0.set_freq_corr(0, 0)
        self.src_0.set_dc_offset_mode(2, 0)
        self.src_0.set_iq_balance_mode(2, 0)
        self.src_0.set_gain_mode(True, 0)
        self.src_0.set_gain(15, 0)
        self.src_0.set_if_gain(15, 0)
        self.src_0.set_bb_gain(15, 0)
        self.src_0.set_antenna('', 0)
        self.src_0.set_bandwidth(0, 0)
          
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
        self.connect((self.src_0, 0), (self.stream_to_vector_0, 0))    
        self.connect((self.stream_to_vector_0, 0), (self.fft_0, 0))    
        self.connect((self.stream_to_vector_1, 0), (self.freq_sink, 0))    
        self.connect((self.vector_to_stream_0, 0), (self.multiply_const_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.src_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.src_0.set_center_freq(self.freq, 0)

    def get_fft_size(self):
        return self.fft_size

    # def set_fft_size(self, fft_size):
        # self.fft_size = fft_size
        # self.multiply_const_0.set_k((1./self.fft_size, ))

    def get_spec(self):
        return self.freq_sink.level()


def main(top_block_cls=RtlSense, options=None):

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
