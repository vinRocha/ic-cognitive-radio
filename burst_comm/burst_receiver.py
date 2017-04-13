#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Burst Receiver
# Author: Vinicius Rocha da Silva
# Generated: Fri Mar 31 15:14:34 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import time


class burst_receiver(gr.top_block):

    def __init__(self, freq):
        gr.top_block.__init__(self, "Burst Receiver")

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        
        self.hdr_cons = hdr_cons = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 2, 1).base()
        
        self.eb = eb = .700
        self.tsh = tsh = 0
        self.rxmod = rxmod = digital.generic_mod(hdr_cons, False, sps, True, eb, False, False)
        self.preamble = preamble = [0xac, 0xdd, 0xa4, 0xe2, 0xf2, 0x8c, 0x20, 0xfc]
        self.nfilts = nfilts = 64
        self.mark_delays = mark_delays = [0, 34, 87, 0, 262]
        self.usrp_rate = usrp_rate = 500e3
        
        self.rx_psf_taps = rx_psf_taps = firdes.root_raised_cosine(nfilts, sps*nfilts, 1.0, eb, nfilts*sps*11)
          
        
        self.pld_cons = pld_cons = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 4, 1).base()
        
        self.modulated_sync_word = modulated_sync_word = digital.modulate_vector_bc(rxmod .to_basic_block(), (preamble), ([1]))
        self.mark_delay = mark_delay = mark_delays[sps/2]
        self.freq = freq
        
        self.format_0 = format_0 = digital.header_format_default(digital.packet_utils.default_access_code, tsh)
          

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(usrp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.digital_protocol_parser_b_0 = digital.protocol_parser_b(format_0)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 6.28/400, (rx_psf_taps), nfilts, 16, 1.5, 1)
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
        	  format_0.header_nbits()/hdr_cons.bits_per_symbol(),
        	  1,
        	  0,
        	  "payload symbols",
        	  "time_est",
        	  False,
        	  gr.sizeof_gr_complex,
        	  "rx_time",
                  1,
                  "",
                  0,
            )
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, eb, 16, 6.28/100)
        self.digital_diff_decoder_bb_0_0 = digital.diff_decoder_bb(pld_cons.arity())
        self.digital_crc32_async_bb_1 = digital.crc32_async_bb(True)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(6.28/400, pld_cons.arity(), False)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(6.28/400, hdr_cons.arity(), False)
        self.digital_corr_est_cc_0 = digital.corr_est_cc((modulated_sync_word), sps, mark_delay, 0.9999999)
        self.digital_constellation_decoder_cb_1 = digital.constellation_decoder_cb(pld_cons)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(hdr_cons)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "payload symbols")
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_CLIENT", '127.0.0.1', '52002', 10000, False)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "payload symbols", True, gr.GR_MSB_FIRST)
        self.blocks_multiply_by_tag_value_cc_0 = blocks.multiply_by_tag_value_cc("amp_est", 1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.digital_crc32_async_bb_1, 'in'))    
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.digital_protocol_parser_b_0, 'info'), (self.digital_header_payload_demux_0, 'header_data'))    
        self.connect((self.blocks_multiply_by_tag_value_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_protocol_parser_b_0, 0))    
        self.connect((self.digital_constellation_decoder_cb_1, 0), (self.digital_diff_decoder_bb_0_0, 0))    
        self.connect((self.digital_corr_est_cc_0, 0), (self.blocks_multiply_by_tag_value_cc_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))    
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_constellation_decoder_cb_1, 0))    
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self.blocks_repack_bits_bb_0, 0))    
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_corr_est_cc_0, 0))    
        self.connect((self.digital_header_payload_demux_0, 0), (self.digital_costas_loop_cc_0, 0))    
        self.connect((self.digital_header_payload_demux_0, 1), (self.digital_costas_loop_cc_0_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_header_payload_demux_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_fll_band_edge_cc_0, 0))    

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_mark_delay(self.mark_delays[self.sps/2])
        self.set_rxmod(digital.generic_mod(self.hdr_cons, False, self.sps, True, self.eb, False, False))

    def get_hdr_cons(self):
        return self.hdr_cons

    def set_hdr_cons(self, hdr_cons):
        self.hdr_cons = hdr_cons
        self.set_rxmod(digital.generic_mod(self.hdr_cons, False, self.sps, True, self.eb, False, False))

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_rxmod(digital.generic_mod(self.hdr_cons, False, self.sps, True, self.eb, False, False))

    def get_tsh(self):
        return self.tsh

    def set_tsh(self, tsh):
        self.tsh = tsh

    def get_rxmod(self):
        return self.rxmod

    def set_rxmod(self, rxmod):
        self.rxmod = rxmod

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts

    def get_mark_delays(self):
        return self.mark_delays

    def set_mark_delays(self, mark_delays):
        self.mark_delays = mark_delays
        self.set_mark_delay(self.mark_delays[self.sps/2])

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.usrp_rate)

    def get_rx_psf_taps(self):
        return self.rx_psf_taps

    def set_rx_psf_taps(self, rx_psf_taps):
        self.rx_psf_taps = rx_psf_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.rx_psf_taps))

    def get_pld_cons(self):
        return self.pld_cons

    def set_pld_cons(self, pld_cons):
        self.pld_cons = pld_cons

    def get_modulated_sync_word(self):
        return self.modulated_sync_word

    def set_modulated_sync_word(self, modulated_sync_word):
        self.modulated_sync_word = modulated_sync_word

    def get_mark_delay(self):
        return self.mark_delay

    def set_mark_delay(self, mark_delay):
        self.mark_delay = mark_delay
        self.digital_corr_est_cc_0.set_mark_delay(self.mark_delay)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_format_0(self):
        return self.format_0

    def set_format_0(self, format_0):
        self.format_0 = format_0


def main(top_block_cls=burst_receiver, options=None):

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
