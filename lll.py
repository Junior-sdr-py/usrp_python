#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: uhd_b200_tx_rand_freq_hop
# Author: Ryan Bosley (N4ONS)
# Description: Sets the center frequency based on input frequency list
# Generated: Sun Jun 19 17:49:27 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys
import threading
import time

from distutils.version import StrictVersion
class uhd_b200_tx_rand_freq_hop(gr.top_block, Qt.QWidget):

    def __init__(self, tx_gain=0, index=0):
        gr.top_block.__init__(self, "uhd_b200_tx_rand_freq_hop")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("uhd_b200_tx_rand_freq_hop")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "uhd_b200_tx_rand_freq_hop")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.tx_gain = tx_gain
        self.index = index

        ##################################################
        # Variables
        ##################################################
        self.freq_list = freq_list = [902e6,928e6,910e6,906e6,912e6,922e6,923e6,907e6,918e6,909e6,911e6,916e6]
        self.freq_index = freq_index = index
        self.variable_qtgui_label = variable_qtgui_label = freq_list[freq_index]
        self.samp_rate = samp_rate = 4e6

        ##################################################
        # Blocks
        ##################################################
        self.probe_index = blocks.probe_signal_i()
        def _freq_index_probe():
            while True:
                val = self.probe_index.level()
                try:
                    self.set_freq_index(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (20))
        _freq_index_thread = threading.Thread(target=_freq_index_probe)
        _freq_index_thread.daemon = True
        _freq_index_thread.start()
        self._variable_qtgui_label_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_formatter = None
        else:
          self._variable_qtgui_label_formatter = lambda x: x
        
        self._variable_qtgui_label_tool_bar.addWidget(Qt.QLabel("Center_Frequency"+": "))
        self._variable_qtgui_label_label = Qt.QLabel(str(self._variable_qtgui_label_formatter(self.variable_qtgui_label)))
        self._variable_qtgui_label_tool_bar.addWidget(self._variable_qtgui_label_label)
        self.top_layout.addWidget(self._variable_qtgui_label_tool_bar)
          
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(freq_list[freq_index], 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.analog_sig_source_x_1 = analog.sig_source_i(samp_rate, analog.GR_SAW_WAVE, 10, len(freq_list), 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.analog_sig_source_x_1, 0), (self.probe_index, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "uhd_b200_tx_rand_freq_hop")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
        self.set_freq_index(self.index)

    def get_freq_list(self):
        return self.freq_list

    def set_freq_list(self, freq_list):
        self.freq_list = freq_list
        self.uhd_usrp_sink_0.set_center_freq(self.freq_list[self.freq_index], 0)
        self.analog_sig_source_x_1.set_amplitude(len(self.freq_list))
        self.set_variable_qtgui_label(self._variable_qtgui_label_formatter(self.freq_list[self.freq_index]))

    def get_freq_index(self):
        return self.freq_index

    def set_freq_index(self, freq_index):
        self.freq_index = freq_index
        self.uhd_usrp_sink_0.set_center_freq(self.freq_list[self.freq_index], 0)
        self.set_variable_qtgui_label(self._variable_qtgui_label_formatter(self.freq_list[self.freq_index]))

    def get_variable_qtgui_label(self):
        return self.variable_qtgui_label

    def set_variable_qtgui_label(self, variable_qtgui_label):
        self.variable_qtgui_label = variable_qtgui_label
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.variable_qtgui_label)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-t", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set tx_gain [default=%default]")
    parser.add_option("-f", "--index", dest="index", type="intx", default=0,
        help="Set index [default=%default]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = uhd_b200_tx_rand_freq_hop(tx_gain=options.tx_gain, index=options.index)
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
tb = None #to clean