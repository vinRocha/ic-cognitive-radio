#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Burst Transmitter
# Author: Vinicius Rocha da Silva
# Generated: Thu Mar 30 17:54:40 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from optparse import OptionParser
import time


class burst_transmitter(gr.top_block):

    def __init__(self, freq):
        gr.top_block.__init__(self, "Burst Transmitter")

        ##################################################
        # Variables
        ##################################################
        self.tsh = tsh = 0
        self.sps = sps = 4
        self.nfilts = nfilts = 64
        self.eb = eb = .700
        self.usrp_rate = usrp_rate = 500e3
        
        self.psf_taps = psf_taps = firdes.root_raised_cosine(nfilts/1.5, nfilts, 1.0, eb, 5*sps*nfilts)
          
        
        self.pld_cons = pld_cons = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 4, 1).base()
        
        
        self.hdr_cons = hdr_cons = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 2, 1).base()
        
        self.freq = freq
        
        self.format_0 = format_0 = digital.header_format_default(digital.packet_utils.default_access_code, tsh)
          
        self.b_ntaps = b_ntaps = 50

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        	"packet_len",
        )
        self.uhd_usrp_sink_0.set_samp_rate(usrp_rate)
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  sps,
                  taps=(psf_taps),
        	  flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        	
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, usrp_rate, usrp_rate/sps*1.4, 10e3, firdes.WIN_KAISER, 6.76))
        self.digital_protocol_formatter_async_0 = digital.protocol_formatter_async(format_0)
        self.digital_map_bb_0_0 = digital.map_bb((pld_cons.pre_diff_code()))
        self.digital_map_bb_0 = digital.map_bb((hdr_cons.pre_diff_code()))
        self.digital_diff_encoder_bb_0_0 = digital.diff_encoder_bb(pld_cons.arity())
        self.digital_crc32_async_bb_0 = digital.crc32_async_bb(False)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((pld_cons.points()), pld_cons.dimensionality ())
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((hdr_cons.points()), hdr_cons.dimensionality ())
        self.digital_burst_shaper_xx_0 = digital.burst_shaper_cc((firdes.window(firdes.WIN_HANN, b_ntaps, 0)), 10, 20, True, "packet_len")
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, "packet_len", 0)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", sps)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_SERVER", '127.0.0.1', '52001', 10000, False)
        self.blocks_repack_bits_bb_2 = blocks.repack_bits_bb(8, 1, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(8, 1, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_pdu_to_tagged_stream_1_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        self.blocks_pdu_to_tagged_stream_1 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.digital_crc32_async_bb_0, 'in'))    
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.digital_protocol_formatter_async_0, 'in'))    
        self.msg_connect((self.digital_protocol_formatter_async_0, 'payload'), (self.blocks_pdu_to_tagged_stream_1, 'pdus'))    
        self.msg_connect((self.digital_protocol_formatter_async_0, 'header'), (self.blocks_pdu_to_tagged_stream_1_0, 'pdus'))    
        self.connect((self.blocks_pdu_to_tagged_stream_1, 0), (self.blocks_repack_bits_bb_2, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_1_0, 0), (self.blocks_repack_bits_bb_1, 0))    
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.digital_map_bb_0, 0))    
        self.connect((self.blocks_repack_bits_bb_2, 0), (self.digital_map_bb_0_0, 0))    
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_burst_shaper_xx_0, 0))    
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.pfb_arb_resampler_xxx_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))    
        self.connect((self.digital_diff_encoder_bb_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))    
        self.connect((self.digital_map_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    
        self.connect((self.digital_map_bb_0_0, 0), (self.digital_diff_encoder_bb_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))    

    def get_tsh(self):
        return self.tsh

    def set_tsh(self, tsh):
        self.tsh = tsh

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.pfb_arb_resampler_xxx_0.set_rate(self.sps)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.usrp_rate, self.usrp_rate/self.sps*1.4, 10e3, firdes.WIN_KAISER, 6.76))
        self.blocks_tagged_stream_multiply_length_0.set_scalar(self.sps)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.usrp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.usrp_rate, self.usrp_rate/self.sps*1.4, 10e3, firdes.WIN_KAISER, 6.76))

    def get_psf_taps(self):
        return self.psf_taps

    def set_psf_taps(self, psf_taps):
        self.psf_taps = psf_taps
        self.pfb_arb_resampler_xxx_0.set_taps((self.psf_taps))

    def get_pld_cons(self):
        return self.pld_cons

    def set_pld_cons(self, pld_cons):
        self.pld_cons = pld_cons

    def get_hdr_cons(self):
        return self.hdr_cons

    def set_hdr_cons(self, hdr_cons):
        self.hdr_cons = hdr_cons

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)

    def get_format_0(self):
        return self.format_0

    def set_format_0(self, format_0):
        self.format_0 = format_0

    def get_b_ntaps(self):
        return self.b_ntaps

    def set_b_ntaps(self, b_ntaps):
        self.b_ntaps = b_ntaps


def main(top_block_cls=burst_transmitter, options=None):

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
