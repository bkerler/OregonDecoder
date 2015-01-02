#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Fri Jan  2 20:16:30 2015
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import osmosdr
import sip
import sys
import time

from distutils.version import StrictVersion
class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.data_rate_V2 = data_rate_V2 = 510*2
        self.version_chooser = version_chooser = data_rate_V2
        self.freq_range = freq_range = 433.995
        self.audio_rate = audio_rate = 48000
        self.trans = trans = 1.2e3
        self.samp_rate = samp_rate = 2400000
        self.samp_per_sym = samp_per_sym = audio_rate/version_chooser
        self.gain = gain = 390
        self.freq_offset = freq_offset = 100e3
        self.freq = freq = (0*433.886e6+0*433.877e6+0*433.995e6)+freq_range*1e6+100e3
        self.data_rate_V1 = data_rate_V1 = 680
        self.data_rate = data_rate = version_chooser
        self.channel_trans = channel_trans = 2000
        self.channel_spacing = channel_spacing = 25e3

        ##################################################
        # Blocks
        ##################################################
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, "Frequency")
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, "Signal")
        self.tab_widget_2 = Qt.QWidget()
        self.tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_2)
        self.tab_grid_layout_2 = Qt.QGridLayout()
        self.tab_layout_2.addLayout(self.tab_grid_layout_2)
        self.tab.addTab(self.tab_widget_2, "Datarate")
        self.top_layout.addWidget(self.tab)
        self._gain_layout = Qt.QVBoxLayout()
        self._gain_tool_bar = Qt.QToolBar(self)
        self._gain_layout.addWidget(self._gain_tool_bar)
        self._gain_tool_bar.addWidget(Qt.QLabel("Decoder_Gain"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._gain_counter = qwt_counter_pyslot()
        self._gain_counter.setRange(0, 1000, 1)
        self._gain_counter.setNumButtons(2)
        self._gain_counter.setValue(self.gain)
        self._gain_tool_bar.addWidget(self._gain_counter)
        self._gain_counter.valueChanged.connect(self.set_gain)
        self._gain_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._gain_slider.setRange(0, 1000, 1)
        self._gain_slider.setValue(self.gain)
        self._gain_slider.setMinimumWidth(1000)
        self._gain_slider.valueChanged.connect(self.set_gain)
        self._gain_layout.addWidget(self._gain_slider)
        self.tab_layout_1.addLayout(self._gain_layout)
        self._version_chooser_options = [data_rate_V1, data_rate_V2]
        self._version_chooser_labels = ["V1","V2"]
        self._version_chooser_tool_bar = Qt.QToolBar(self)
        self._version_chooser_tool_bar.addWidget(Qt.QLabel("Oregon Scientific Version"+": "))
        self._version_chooser_combo_box = Qt.QComboBox()
        self._version_chooser_tool_bar.addWidget(self._version_chooser_combo_box)
        for label in self._version_chooser_labels: self._version_chooser_combo_box.addItem(label)
        self._version_chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._version_chooser_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._version_chooser_options.index(i)))
        self._version_chooser_callback(self.version_chooser)
        self._version_chooser_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_version_chooser(self._version_chooser_options[i]))
        self.tab_grid_layout_2.addWidget(self._version_chooser_tool_bar, 0,0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_rate, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 2,0)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq-freq_offset, #fc
        	samp_rate/50, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._qtgui_sink_x_0_win)
        
        self.qtgui_sink_x_0.enable_rf_freq(True)
        
        
          
        self.qtgui_number_sink_0 = qtgui.number_sink(
                gr.sizeof_float,
                0,
                qtgui.NUM_GRAPH_HORIZ,
        	1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        units = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])
        
        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.tab_grid_layout_1.addWidget(self._qtgui_number_sink_0_win, 0,0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 0,0)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("TX/RX", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(50, (firdes.low_pass(1, samp_rate, 
        channel_spacing,channel_trans, firdes.WIN_BLACKMAN, 6.76)), -freq_offset, samp_rate)
        self._freq_range_layout = Qt.QVBoxLayout()
        self._freq_range_tool_bar = Qt.QToolBar(self)
        self._freq_range_layout.addWidget(self._freq_range_tool_bar)
        self._freq_range_tool_bar.addWidget(Qt.QLabel("Frequency"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._freq_range_counter = qwt_counter_pyslot()
        self._freq_range_counter.setRange(433, 434, 0.005)
        self._freq_range_counter.setNumButtons(2)
        self._freq_range_counter.setValue(self.freq_range)
        self._freq_range_tool_bar.addWidget(self._freq_range_counter)
        self._freq_range_counter.valueChanged.connect(self.set_freq_range)
        self._freq_range_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._freq_range_slider.setRange(433, 434, 0.005)
        self._freq_range_slider.setValue(self.freq_range)
        self._freq_range_slider.setMinimumWidth(1)
        self._freq_range_slider.valueChanged.connect(self.set_freq_range)
        self._freq_range_layout.addWidget(self._freq_range_slider)
        self.tab_grid_layout_0.addLayout(self._freq_range_layout, 1,0)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samp_per_sym*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_1 = digital.binary_slicer_fb()
        self._data_rate_tool_bar = Qt.QToolBar(self)
        self._data_rate_tool_bar.addWidget(Qt.QLabel("Datarate"+": "))
        self._data_rate_line_edit = Qt.QLineEdit(str(self.data_rate))
        self._data_rate_tool_bar.addWidget(self._data_rate_line_edit)
        self._data_rate_line_edit.returnPressed.connect(
        	lambda: self.set_data_rate(int(self._data_rate_line_edit.text().toAscii())))
        self.tab_grid_layout_2.addWidget(self._data_rate_tool_bar, 1,0)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "/tmp/fifo", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((gain*1e-3, ))
        self.band_pass_filter_0 = filter.fir_filter_ccc(1, firdes.complex_band_pass(
        	1, samp_rate/50, -2500, 2500, trans, firdes.WIN_HAMMING, 6.76))
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=samp_rate/50,
        	audio_decim=1,
        	audio_pass=0*500+1*2500,
        	audio_stop=5000,
        )
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, 1e-2, 1, 0)
        self.analog_agc2_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_binary_slicer_fb_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_1, 0))
        self.connect((self.osmosdr_source_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_data_rate_V2(self):
        return self.data_rate_V2

    def set_data_rate_V2(self, data_rate_V2):
        self.data_rate_V2 = data_rate_V2
        self.set_version_chooser(self.data_rate_V2)

    def get_version_chooser(self):
        return self.version_chooser

    def set_version_chooser(self, version_chooser):
        self.version_chooser = version_chooser
        self.set_samp_per_sym(self.audio_rate/self.version_chooser)
        self._version_chooser_callback(self.version_chooser)
        self.set_data_rate(self.version_chooser)

    def get_freq_range(self):
        return self.freq_range

    def set_freq_range(self, freq_range):
        self.freq_range = freq_range
        self.set_freq((0*433.886e6+0*433.877e6+0*433.995e6)+self.freq_range*1e6+100e3)
        Qt.QMetaObject.invokeMethod(self._freq_range_counter, "setValue", Qt.Q_ARG("double", self.freq_range))
        Qt.QMetaObject.invokeMethod(self._freq_range_slider, "setValue", Qt.Q_ARG("double", self.freq_range))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_samp_per_sym(self.audio_rate/self.version_chooser)

    def get_trans(self):
        return self.trans

    def set_trans(self, trans):
        self.trans = trans
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate/50, -2500, 2500, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, 
        self.channel_spacing,self.channel_trans, firdes.WIN_BLACKMAN, 6.76)))
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate/50, -2500, 2500, self.trans, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(self.freq-self.freq_offset, self.samp_rate/50)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_per_sym*(1+0.0))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_add_const_vxx_0.set_k((self.gain*1e-3, ))
        Qt.QMetaObject.invokeMethod(self._gain_counter, "setValue", Qt.Q_ARG("double", self.gain))
        Qt.QMetaObject.invokeMethod(self._gain_slider, "setValue", Qt.Q_ARG("double", self.gain))

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-self.freq_offset)
        self.qtgui_sink_x_0.set_frequency_range(self.freq-self.freq_offset, self.samp_rate/50)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.qtgui_sink_x_0.set_frequency_range(self.freq-self.freq_offset, self.samp_rate/50)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_data_rate_V1(self):
        return self.data_rate_V1

    def set_data_rate_V1(self, data_rate_V1):
        self.data_rate_V1 = data_rate_V1

    def get_data_rate(self):
        return self.data_rate

    def set_data_rate(self, data_rate):
        self.data_rate = data_rate
        Qt.QMetaObject.invokeMethod(self._data_rate_line_edit, "setText", Qt.Q_ARG("QString", str(self.data_rate)))

    def get_channel_trans(self):
        return self.channel_trans

    def set_channel_trans(self, channel_trans):
        self.channel_trans = channel_trans
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, 
        self.channel_spacing,self.channel_trans, firdes.WIN_BLACKMAN, 6.76)))

    def get_channel_spacing(self):
        return self.channel_spacing

    def set_channel_spacing(self, channel_spacing):
        self.channel_spacing = channel_spacing
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, 
        self.channel_spacing,self.channel_trans, firdes.WIN_BLACKMAN, 6.76)))

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = top_block()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
