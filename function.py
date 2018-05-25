# -*- coding: utf8 -*-
import numpy as np
from scipy import signal
from uhd import libpyuhd as lib
import time
samples=8192
list = [400e6, 456e6, 512e6, 568e6]
channels=[0]
metadata_transmit=lib.types.tx_metadata()
st_args = lib.usrp.stream_args("fc32", "sc16")

def initialization_usrp():
    usrp = lib.usrp.multi_usrp.make(" ")
    usrp.set_clock_source("internal");
    print(usrp.get_pp_string())
    usrp.set_rx_subdev_spec(lib.usrp.subdev_spec("A:A"))
    global usrp
def preinstall():
    usrp.set_rx_rate(56e6)
    print("Установлена частота {} МГц".format(usrp.get_rx_rate()/1e6))
    usrp.set_rx_gain(40, 0)
    print("Установлене підсилення {} dB".format(usrp.get_rx_gain()))
    usrp.set_rx_bandwidth(56e6)
    print("Установлена смуга фільтра ПЧ {} МГц".format(usrp.get_rx_bandwidth()/1e6))
    usrp.set_time_now(lib.types.time_spec(0.0))
    st_args.channels=[0]

    streamer = usrp.get_rx_stream(st_args)
    stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.num_done)
    stream_cmd.num_samps=samples
    stream_cmd.stream_now=True
    recv_buff = np.zeros((len(channels), samples), dtype=np.complex64)
    metadata_rx = lib.types.rx_metadata()

    print(streamer.get_max_num_samps())
    print(usrp.get_rx_num_channels())
    streamer.issue_stream_cmd(stream_cmd)
    global  streamer, recv_buff, stream_cmd,metadata_rx


def reciever():
    buffs = np.array([])

    for i in list:
        usrp.set_rx_freq(lib.types.tune_request(i),0)
        while  usrp.get_tx_sensor("lo_locked").to_bool() != True:
            print(1)
            continue
        streamer.recv(recv_buff, metadata_rx)
        if metadata_rx.error_code == lib.types.rx_metadata_error_code.timeout:
            print ("ERRROR")
        elif metadata_rx.error_code == lib.types.rx_metadata_error_code.late:
            print ("ERR1")
        elif metadata_rx.error_code == lib.types.rx_metadata_error_code.broken_chain:
            print ("ERR2")
        elif metadata_rx.error_code == lib.types.rx_metadata_error_code.overflow:
            print ("ERR3")
        elif metadata_rx.error_code == lib.types.rx_metadata_error_code.alignment:
            print ("ERR4")
        elif metadata_rx.error_code == lib.types.rx_metadata_error_code.bad_packet:
            print ("ERR5")

        stream_cmd.time_spec = lib.types.time_spec(0)
        streamer.issue_stream_cmd(stream_cmd)
        PSD = 10.0 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(recv_buff, 2048) / float(2048))) ** 2)
        buffs = np.append(buffs, PSD)

        # if buffs.size == 4 * 8192:
    #        #  global recv_buff
    return np.append(buffs[2048:],buffs[:2048])
    # else:
    #    return np.ones(4 * 8192)


def maxhold1(data, maxhold):
    for i in np.arange(data.size):
        if data[i] > maxhold[i]:
            maxhold[i] = data[i]
    return maxhold


def setZeros(data
             , bandwidth  # spectrum bandwidth
             , ranges  # list of ranges ([min_freq, max_freq]) for which we should set zeros in spectrum (data)
             , min_freq_in_band=0
             ):
    # number of frequencies (channels)
    freqs_count = data.size
    # frequency step between neighborhood channels
    freq_step = bandwidth / (freqs_count - 1)

    for current_range in ranges:
        min_freq = current_range[0] - min_freq_in_band  # Find minimum frequency in current range
        max_freq = current_range[1] - min_freq_in_band  # Find maximum frequency in current range
        # Estimate minimum and maximum indices
        min_ind = min([freqs_count - 1, max([0, np.floor(min_freq / freq_step).astype('int')])])
        max_ind = min([freqs_count - 1, max([0, np.ceil(max_freq / freq_step).astype('int')])])
        if max_ind > min_ind:
            ind = range(min_ind, max_ind + 1)
            data[ind] = np.random.randint(-90, -67, len(ind))
    return data


def pre_demodulation(start_freq, stop_freq):
    #st_args = lib.usrp.stream_args("fc32", "sc16")
    streamer1 = usrp.get_rx_stream(st_args)
    global streamer1
    band = stop_freq - start_freq
    center_freq = start_freq + band / 2
    if band > 56e6:
       band=56e6
    usrp.set_rx_freq(lib.types.tune_request(center_freq), 0)
    usrp.set_rx_rate(band)
    usrp.set_rx_bandwidth(band)
    stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.start_cont)
    stream_cmd.num_samps = 8192
    stream_cmd.stream_now = True
    streamer.issue_stream_cmd(stream_cmd)


def demodulation():
    streamer1.recv(recv_buff, metadata_rx)
    return recv_buff
def stop_demod():
    stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.start_cont)
    streamer1.issue_stream_cmd(stream_cmd)
    time.sleep(1)
    print("STOP_DEMOD")
def transmiter_setup(start_f,stop_f):

    tx_band=stop_f-start_f
    tx_freq=start_f+tx_band/2
    if tx_band>56e6:
        tx_band=56e6
    st_args.channels=[0]
    usrp.set_master_clock_rate(tx_band)
    usrp.set_tx_rate(tx_band, 0)
    usrp.set_tx_freq(lib.types.tune_request(tx_freq), 0)
    print(tx_freq)
    usrp.set_tx_gain(60, 0)
    usrp.set_time_now(lib.types.time_spec(0))
    metadata_transmit.start_of_burst=True
    metadata_transmit.end_of_burst=False
    metadata_transmit.has_time_spec=True
    metadata_transmit.time_spec=lib.types.time_spec(0.1)
    metadata_transmit.time_spec+=usrp.get_time_now()
    streamer_transmit=usrp.get_tx_stream(st_args)
    global streamer_transmit
def transmitter(data):
        streamer_transmit.send(data,metadata_transmit)
        metadata_transmit.start_of_burst=False
        metadata_transmit.end_of_burst=False
        metadata_transmit.has_time_spec=False
def filter(filt_list,data,num_samps):
    for i in filt_list:
        a,b=signal.butter(6,[float(i[0])/(num_samps/2),float(i[1])/(num_samps/2)],'bandstop')
        data=signal.filtfilt(a,b,data)
    return np.fft.fft(data)
def detect_start_stop(center_sample,data,start=0,stop=0):
    for i in range(center_sample,data.size):
        if data[i]<=0.1:
            print("for1",i)
            start=i
            break
    for i in range(center_sample,0,-1):
        if data[i] <=0.1 :
            print(i)
            stop=i
            break
    return start,stop

'''def show_widget():
    res = conn.execute("SELECT * from SPECTRUM")
    tables1.tableWidget.setColumnCount(4)
    tables1.tableWidget.setRowCount(0)
    for row_number, row_data in enumerate(res):
        tables1.tableWidget.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            tables1.tableWidget.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))
    tables1.show()'''
