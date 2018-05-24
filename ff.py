#-*- coding: utf-8 -*-
from PyQt4 import QtCore,QtGui,uic
import numpy as np
import libpyuhd as lib
import pyqtgraph as pg
import time
##################CONNECT USRP#########################################
usrp400 = lib.usrp.multi_usrp("addr=192.168.10.1")
usrp800 = lib.usrp.multi_usrp("addr=192.168.10.2")
usrp1200 = lib.usrp.multi_usrp("addr=192.168.10.3")
usrp2400 = lib.usrp.multi_usrp("addr=192.168.10.4")
rate = 50e6
####################GLOBAL SETTINGS400####################################
n400 = 2
x400 = (400e6 - rate / 2) + (np.arange(0, 4096 * n400) * rate / 4096) + 25e6
maxhold400 = np.ones(n400 * 4096) * (-1000)
###################GLOBAL SETTING800#######################################
n800 = 2
x800 = (800e6 - rate / 2) + (np.arange(0, 4096 * n800) * rate / 4096) + 25e6
maxhold800 = np.ones(n800 * 4096) * (-1000)
##################GLOBAL SETTINGS 1200#####################################
n1000 = 4
x1000 = (1000e6 - rate / 2) + (np.arange(0, 4096 * n1000) * rate / 4096) + 25e6
maxhold1200 = np.ones(n1000 * 4096) * (-1000)
#################GLOBAL 2400###############################################
n2400 = 2
x2400 = (2400e6 - rate / 2) + (np.arange(0, 4096 * n2400) * rate / 4096) + 25e6
maxhold2400 = np.ones(n2400 * 4096) * (-1000)
time_sleap=30
class Thread1(QtCore.QThread):
    mysignal_400 = QtCore.pyqtSignal(np.ndarray)
    mysignal_400_1 = QtCore.pyqtSignal(np.ndarray)
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)

        self.start_freq = 400e6

    def run(self):
            chanels = 0
            usrp400.set_rx_rate(rate, 0)
            usrp400.set_rx_gain(30, 0)
            usrp400.set_rx_bandwidth(rate)
            usrp400.set_rx_antenna("RX2")
            st_args = lib.usrp.stream_args("fc32", "sc8")
            st_args.chanels = chanels
            metadata400 = lib.types.rx_metadata()
            streamer400 = usrp400.get_rx_stream(st_args)
            stream_cmd400 = lib.types.stream_cmd(lib.types.stream_mode.num_done)
            stream_cmd400.num_samps = 4096
            stream_cmd400.stream_now = True
            stream_cmd400.time_spec = lib.types.time_spec(1)
            streamer400.issue_stream_cmd(stream_cmd400)

            recv_buff400 = np.zeros(4096, dtype=np.complex64)
            while True:
                #start=time.time()
                QtCore.QThread.msleep(time_sleap)
                fft = np.array([])
                #usrp400.set_rx_gain(window.gain400.value(), 0)
                for i in range(0, n400):
                    usrp400.set_rx_freq(lib.types.tune_request(self.start_freq + rate * i), 0)
                    streamer400.recv(recv_buff400, metadata400)
                    if metadata400.error_code == lib.types.rx_metadata_error_code.timeout:
                        print ("ERRROR")
                    elif metadata400.error_code == lib.types.rx_metadata_error_code.late:
                        print ("ERR1")
                    elif metadata400.error_code == lib.types.rx_metadata_error_code.broken_chain:
                        print ("ERR2")
                    elif metadata400.error_code == lib.types.rx_metadata_error_code.overflow:
                        print ("ERR3")
                    elif metadata400.error_code == lib.types.rx_metadata_error_code.alignment:
                        print ("ERR4")
                    elif metadata400.error_code == lib.types.rx_metadata_error_code.bad_packet:
                        print ("ERR5")
                    prom = np.fft.fft(recv_buff400, axis=0)
                    prom[0:3] = 0
                    fft = np.hstack((np.fft.fftshift(prom),fft))
                    self.dbm = np.abs(fft)
                    stream_cmd400.time_spec = lib.types.time_spec(0)
                    streamer400.issue_stream_cmd(stream_cmd400)
                for i in range(self.dbm.size):
                    if self.dbm[i] > maxhold400[i]:
                        maxhold400[i] = self.dbm[i]
                self.mysignal_400.emit(self.dbm)
                self.mysignal_400_1.emit(maxhold400)
                #print (time.time()-start)

class Thread2(QtCore.QThread):
    mysignal_800 = QtCore.pyqtSignal(np.ndarray)
    mysignal_800_1 = QtCore.pyqtSignal(np.ndarray)
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.start_freq_800=800e6
    def run(self):
        chanels = 0
        usrp800.set_rx_rate(rate, 0)
        usrp800.set_rx_gain(30, 0)
        usrp800.set_rx_bandwidth(rate)
        usrp800.set_rx_antenna("RX2")
        st_args = lib.usrp.stream_args("fc32", "sc8")
        st_args.chanels = chanels
        metadata800 = lib.types.rx_metadata()
        streamer800 = usrp800.get_rx_stream(st_args)
        stream_cmd800 = lib.types.stream_cmd(lib.types.stream_mode.num_done)
        stream_cmd800.num_samps = 4096
        stream_cmd800.stream_now = True
        stream_cmd800.time_spec = lib.types.time_spec(1)
        streamer800.issue_stream_cmd(stream_cmd800)
        recv_buff800 = np.zeros(4096, dtype=np.complex64)
        while True:
            # start=time.time()
            QtCore.QThread.msleep(time_sleap)
            fft = np.array([])
            # usrp400.set_rx_gain(window.gain400.value(), 0)
            for i in range(0, n800):
                usrp800.set_rx_freq(lib.types.tune_request(self.start_freq_800 + rate * i), 0)
                streamer800.recv(recv_buff800, metadata800)
                if metadata800.error_code == lib.types.rx_metadata_error_code.timeout:
                    print ("ERRROR")
                elif metadata800.error_code == lib.types.rx_metadata_error_code.late:
                    print ("ERR1")
                elif metadata800.error_code == lib.types.rx_metadata_error_code.broken_chain:
                    print ("ERR2")
                elif metadata800.error_code == lib.types.rx_metadata_error_code.overflow:
                    print ("ERR3")
                elif metadata800.error_code == lib.types.rx_metadata_error_code.alignment:
                    print ("ERR4")
                elif metadata800.error_code == lib.types.rx_metadata_error_code.bad_packet:
                    print ("ERR5")
                prom = np.fft.fft(recv_buff800, axis=0)
                prom[0:3] = 0
                fft = np.append(fft, np.fft.fftshift(prom))
                self.dbm800 = np.abs(fft)
                stream_cmd800.time_spec = lib.types.time_spec(0)
                streamer800.issue_stream_cmd(stream_cmd800)
            for i in range(self.dbm800.size):
                if self.dbm800[i] > maxhold800[i]:
                    maxhold800[i] = self.dbm800[i]
            self.mysignal_800.emit(self.dbm800)
            self.mysignal_800_1.emit(maxhold800)
class Thread3(QtCore.QThread):
    mysignal_1200 = QtCore.pyqtSignal(np.ndarray)
    mysignal_1200_1=QtCore.pyqtSignal(np.ndarray)
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)

        self.start_freq_1200=1000e6
    def run(self):
        chanels = 0
        usrp1200.set_rx_rate(rate, 0)
        usrp1200.set_rx_gain(30, 0)
        usrp1200.set_rx_bandwidth(rate)
        usrp1200.set_rx_antenna("RX2")
        st_args = lib.usrp.stream_args("fc32", "sc8")
        st_args.chanels = chanels
        metadata1200 = lib.types.rx_metadata()
        streamer1200 = usrp1200.get_rx_stream(st_args)
        stream_cmd1200 = lib.types.stream_cmd(lib.types.stream_mode.num_done)
        stream_cmd1200.num_samps = 4096
        stream_cmd1200.stream_now = True
        stream_cmd1200.time_spec = lib.types.time_spec(1)
        streamer1200.issue_stream_cmd(stream_cmd1200)
        recv_buff1200 = np.zeros(4096, dtype=np.complex64)
        while True:
            # start=time.time()
            QtCore.QThread.msleep(time_sleap)
            fft = np.array([])
            # usrp400.set_rx_gain(window.gain400.value(), 0)
            for i in range(0, n1000):
                usrp1200.set_rx_freq(lib.types.tune_request(self.start_freq_1200 + rate * i), 0)
                streamer1200.recv(recv_buff1200, metadata1200)
                if metadata1200.error_code == lib.types.rx_metadata_error_code.timeout:
                    print ("ERRROR")
                elif metadata1200.error_code == lib.types.rx_metadata_error_code.late:
                    print ("ERR1")
                elif metadata1200.error_code == lib.types.rx_metadata_error_code.broken_chain:
                    print ("ERR2")
                elif metadata1200.error_code == lib.types.rx_metadata_error_code.overflow:
                    print ("ERR3")
                elif metadata1200.error_code == lib.types.rx_metadata_error_code.alignment:
                    print ("ERR4")
                elif metadata1200.error_code == lib.types.rx_metadata_error_code.bad_packet:
                    print ("ERR5")
                prom = np.fft.fft(recv_buff1200, axis=0)
                prom[0:3] = 0
                fft = np.append(fft, np.fft.fftshift(prom))
                self.dbm1200 = np.abs(fft)
                stream_cmd1200.time_spec = lib.types.time_spec(0)
                streamer1200.issue_stream_cmd(stream_cmd1200)
            for i in range(self.dbm1200.size):
                if self.dbm1200[i] > maxhold1200[i]:
                    maxhold1200[i] = self.dbm1200[i]
            self.mysignal_1200.emit(self.dbm1200)
            self.mysignal_1200_1.emit(maxhold1200)
class Thread4(QtCore.QThread):
    mysignal_2400 = QtCore.pyqtSignal(np.ndarray)
    mysignal_2400_1 = QtCore.pyqtSignal(np.ndarray)
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.start_freq_2400=2400e6
    def run(self):
        chanels = 0
        usrp2400.set_rx_rate(rate, 0)
        usrp2400.set_rx_gain(30, 0)
        usrp2400.set_rx_bandwidth(rate)
        usrp2400.set_rx_antenna("RX2")
        st_args = lib.usrp.stream_args("fc32", "sc8")
        st_args.chanels = chanels
        metadata2400 = lib.types.rx_metadata()
        streamer2400 = usrp2400.get_rx_stream(st_args)
        stream_cmd2400 = lib.types.stream_cmd(lib.types.stream_mode.num_done)

        stream_cmd2400.num_samps = 4096
        stream_cmd2400.stream_now = True
        stream_cmd2400.time_spec = lib.types.time_spec(1)
        streamer2400.issue_stream_cmd(stream_cmd2400)
        recv_buff2400 = np.zeros(4096, dtype=np.complex64)
        while True:
            # start=time.time()
            QtCore.QThread.msleep(time_sleap)
            fft = np.array([])
            # usrp400.set_rx_gain(window.gain400.value(), 0)
            for i in range(0, n2400):
                usrp2400.set_rx_freq(lib.types.tune_request(self.start_freq_2400 + rate * i), 0)
                streamer2400.recv(recv_buff2400, metadata2400)
                if metadata2400.error_code == lib.types.rx_metadata_error_code.timeout:
                    print ("ERRROR")
                elif metadata2400.error_code == lib.types.rx_metadata_error_code.late:
                    print ("ERR1")
                elif metadata2400.error_code == lib.types.rx_metadata_error_code.broken_chain:
                    print ("ERR2")
                elif metadata2400.error_code == lib.types.rx_metadata_error_code.overflow:
                    print ("ERR3")
                elif metadata2400.error_code == lib.types.rx_metadata_error_code.alignment:
                    print ("ERR4")
                elif metadata2400.error_code == lib.types.rx_metadata_error_code.bad_packet:
                    print ("ERR5")
                prom = np.fft.fft(recv_buff2400, axis=0)
                prom[0:3] = 0
                fft = np.append(fft, np.fft.fftshift(prom))
                self.dbm2400 = np.abs(fft)
                stream_cmd2400.time_spec = lib.types.time_spec(0)
                streamer2400.issue_stream_cmd(stream_cmd2400)
            for i in range(self.dbm2400.size):
                if self.dbm2400[i] > maxhold2400[i]:
                    maxhold2400[i] = self.dbm2400[i]
            self.mysignal_2400.emit(self.dbm2400)
            self.mysignal_2400_1.emit(maxhold2400)
class MyWindow(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        uic.loadUi("desktop.ui",self)

###################PLOT400########################################################################################################
        self.plott1=self.graphicsView400
        self.plott1.setMenuEnabled(enableMenu=False, enableViewBoxMenu='same')
        self.plott1.showGrid(x=True, y=True, alpha=1)
        self.plott1.setLimits(xMin=min(x400), xMax=max(x400), yMin=-1)
        self.plotta=self.plott1.plot()
        self.plottb = self.plott1.plot()
        self.region400 = pg.LinearRegionItem()
        self.region400.setRegion([400e6, 420e6])
        self.plott1.addItem(self.region400)
###################PLOT800#########################################################################################################
        self.plott2=self.graphicsView800
        self.plott2.setMenuEnabled(enableMenu=False, enableViewBoxMenu='same')
        self.plott2.showGrid(x=True, y=True, alpha=1)
        self.plott2.setLimits(xMin=min(x800), xMax=max(x800), yMin=-1)
        self.plotta2=self.plott2.plot()
        self.plottb2 = self.plott2.plot()
        self.region800 = pg.LinearRegionItem()
        self.region800.setRegion([800e6, 820e6])
        self.plott2.addItem(self.region800)
#################PLOT1000##########################################################################################################
        self.plott3 = self.graphicsView1000
        self.plott3.setMenuEnabled(enableMenu=False, enableViewBoxMenu='same')
        self.plott3.showGrid(x=True, y=True, alpha=1)
        self.plott3.setLimits(xMin=min(x1000), xMax=max(x1000), yMin=-1)
        self.plotta3 = self.plott3.plot()
        self.plottb3 = self.plott3.plot()
        self.region1200 = pg.LinearRegionItem()
        self.region1200.setRegion([1000e6, 1020e6])
        self.plott3.addItem(self.region1200)
################PLOT2400###########################################################################################################
        self.plott4 = self.graphicsView2400
        self.plott4.setMenuEnabled(enableMenu=False, enableViewBoxMenu='same')
        self.plott4.showGrid(x=True, y=True, alpha=1)
        self.plott4.setLimits(xMin=min(x2400), xMax=max(x2400), yMin=-1)
        self.plotta4 = self.plott4.plot()
        self.plottb4 = self.plott4.plot()
        self.region2400 = pg.LinearRegionItem()
        self.region2400.setRegion([2400e6, 2420e6])
        self.plott4.addItem(self.region2400)
###############THREAD#############################################################################################################
        self.tread=Thread1()
        self.tread2=Thread2()
        self.tread3=Thread3()
        self.tread4=Thread4()
#################CONNECT###########################################################################################################
        self.connect(self.reciev,QtCore.SIGNAL("clicked()"),self.on_start)
        self.tread.mysignal_400.connect(self.plot_data)
        self.tread.mysignal_400_1.connect(self.plot_maxhold400)
        self.tread2.mysignal_800.connect(self.plot_data2)
        self.tread2.mysignal_800_1.connect(self.plot_maxhold800)
        self.tread3.mysignal_1200.connect(self.plot_data3)
        self.tread3.mysignal_1200_1.connect(self.plot_maxhold1200)
        self.tread4.mysignal_2400.connect(self.plot_data4)
        self.tread4.mysignal_2400_1.connect(self.plot_maxhold2400)
        self.connect(self.maxhold400,QtCore.SIGNAL("clicked()"),self.clear_maxhold400)
        #self.connect(self.tread,QtCore.SIGNAL("s1(npArray)"),self.plot_data,QtCore.Qt.QueuedConnection)
    def on_start(self):
        self.tread.start()
        self.tread2.start()
        self.tread3.start()
        self.tread4.start()
    def plot_data(self,data):
        self.plotta.setData(x=x400,y=data)
        a, b = self.region400.getRegion()
        if b - a > 50e6:
            centr = a + (b - a) / 2
            self.region400.setRegion([centr - (50e6 / 2), centr + (50e6 / 2)])
            print (centr)
        elif b - a < 1e6:
            centr = a + (b - a) / 2
            self.region400.setRegion([centr - (1e6 / 2), centr + (1e6 / 2)])

    def plot_data2(self,data2):
        #print (2)
        self.plotta2.setData(x=x800,y=data2)
        a, b = self.region800.getRegion()
        if b - a > 50e6:
            centr = a + (b - a) / 2
            self.region800.setRegion([centr - (50e6 / 2), centr + (50e6 / 2)])
            print (centr)
        elif b - a < 1e6:
            centr = a + (b - a) / 2
            self.region800.setRegion([centr - (1e6 / 2), centr + (1e6 / 2)])

    def plot_data3(self, data3):
        # print (2)
        self.plotta3.setData(x=x1000, y=data3)
        a, b = self.region1200.getRegion()
        if b - a > 50e6:
            centr = a + (b - a) / 2
            self.region1200.setRegion([centr - (50e6 / 2), centr + (50e6 / 2)])
            print (centr)
        elif b - a < 1e6:
            centr = a + (b - a) / 2
            self.region1200.setRegion([centr - (1e6 / 2), centr + (1e6 / 2)])
    #def plot_data3(self,data2):
     #   #print (2)
      #  self.plotta3.setData(y=data2)

    def plot_data4(self, data4):
        # print (2)
        self.plotta4.setData(x=x2400, y=data4)
        a, b = self.region2400.getRegion()
        if b - a > 50e6:
            centr = a + (b - a) / 2
            self.region2400.setRegion([centr - (50e6 / 2), centr + (50e6 / 2)])
            print (centr)
        elif b - a < 1e6:
            centr = a + (b - a) / 2
            self.region2400.setRegion([centr - (1e6 / 2), centr + (1e6 / 2)])
    def plot_maxhold400(self, maxhold400):
        self.plottb.setData(x=x400, y=maxhold400, pen="r")


    def plot_maxhold800(self, maxhold800):
        self.plottb2.setData(x=x800, y=maxhold800, pen="r")

    def plot_maxhold1200(self, maxhold1000):
        self.plottb3.setData(x=x1000, y=maxhold1000, pen="r")

    def plot_maxhold2400(self, maxhold2400):
        self.plottb4.setData(x=x2400, y=maxhold2400, pen="r")






    def clear_maxhold400(self):
        maxhold400 = np.ones(n400 * 4096) * (-1000)
        global maxhold400


if __name__ =="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())


