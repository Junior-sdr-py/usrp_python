import numpy as np
import function
import functools
import multiprocessing
from PyQt4 import QtGui, QtCore, uic
import pyqtgraph as pg
import value_400
from scipy import signal
import peakutils
band = 40e6
def reciev(flag,arr,filter_mass,maxhold,start_freq,stop_freq,demod_arr,transmit_data,peaks):
    print('PROC400_START')
    #function.initialization_usrp()
    while True:
        if flag.value == 1:
            #function.preinstall()
            N=8192*2
            # sample spacing
            T=1.0 / 800.0
            x=np.linspace(0.0, N * T, N)
            y1=np.sin(50.0 * 2.0 * np.pi * x) + 0.5 * np.sin(80.0 * 2.0 * np.pi * x) + 0.7 * np.sin(
                30.0 * 2.0 * np.pi * x) + 0.5 * np.sin(10.0 * 2.0 * np.pi * x)
            y2=np.sin(50.0 * 2.0 * np.pi * x) + 0.5 * np.sin(80.0 * 2.0 * np.pi * x) + 0.2 * np.sin(
                60.0 * 2.0 * np.pi * x) + 0.4 * np.sin(40.0 * 2.0 * np.pi * x)
            while flag.value == 1:

                yf1=np.fft.fft(y1)
                arr[:]=2.0 / N * np.abs(yf1[:N / 2])
                peak=peakutils.indexes(arr,thres=0.3,min_dist=20)
                for i in peak:
                    if i not in peaks:
                        peaks.append(i)

                #arr[:] = np.fft.fft(np.random.rand(8192))# function.setZeros(function.reciever(), band * 4, filter_mass, start_freq)
                #maxhold[:] = function.maxhold1(arr, maxhold[:])
        if flag.value == 2:
            function.pre_demodulation(start_freq.value, stop_freq.value)
            while flag.value == 2:
                demod_arr[:] = function.demodulation()
            function.stop_demod()
        if flag.value==3:
            print (transmit_data)
            function.transmiter_setup(start_freq.value,stop_freq.value)
            while flag.value==3:
                function.transmitter(transmit_data)


def res_maxhold(maxhold):
    maxhold[:]=np.ones(8192)*-1000

for i in [reciev]:
    p = multiprocessing.Process(target=i,args=(value_400.flag400,value_400.arr400,value_400.filter_mass_400,value_400.maxhold400,\
                                               value_400.start_freq_400,value_400.stop_freq_400,value_400.demod_arr400,value_400.transmit_data400,value_400.peak400))
    p.daemon = True
    p.start()


class My_Windows(QtGui.QTabWidget):
    def __init__(self, parent=None):
        QtGui.QTabWidget.__init__(self, parent)
        uic.loadUi("UI/NewDesc.ui", self)
        self.wind_dialog = uic.loadUi('UI/dialog.ui')
        self.connect(self.reciev, QtCore.SIGNAL("clicked()"), self.on_start)
        self.region400=pg.LinearRegionItem()
        self.connect(self.pushButton_UHF, QtCore.SIGNAL("clicked()"), functools.partial(self.start_write_400,self.region400,value_400.filter_mass_400,self.tableWidget))
        #self.connect(self.pushButton_UHF_L, QtCore.SIGNAL("clicked()"), self.start_write_800)
        #self.connect(self.pushButton_L, QtCore.SIGNAL("clicked()"), self.start_write_1200)
        #self.connect(self.pushButton_S, QtCore.SIGNAL("clicked()"), self.start_write_2400)
        self.connect(self.demod_400, QtCore.SIGNAL("clicked()"), self.demodulation)
#        self.connect(self.comboBox_UHF, QtCore.SIGNAL("activated (int)"), self.gen_data_tx_400)
        self.reset_maxhold.clicked.connect(functools.partial(res_maxhold,value_400.maxhold400))
        self.transmitt.clicked.connect(self.transmitter)
        data400 = self.graphicsView400
        data800 = self.graphicsView800
        data1200 = self.graphicsView1000
        data2400 = self.graphicsView2400

        self.image_item=pg.ImageItem()
        self.data_demod = self.graphicsView.plot()
        self.graphicsView_2.addItem(self.image_item)
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0, 0, 0, 0], [255, 255, 0, 255], [0, 0, 0, 255], (0, 0, 255, 255), (255, 0, 0, 255)],
                         dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)
        self.image_item.setLookupTable(lut)
        self.image_item.setLevels([-70,0])


        self.tableWidget_2.itemClicked.connect(self.test_800)
        self.tableWidget_3.itemClicked.connect(self.test_1200)
        self.tableWidget_4.itemClicked.connect(self.test_2400)
        self.plota400 = data400.plot()
        self.plotb400 = data400.plot()
        data400.showGrid(x=True, y=True, alpha=1)
        data400.setLimits(xMin=400e6, xMax=600e6, yMin=0, yMax=1)

        hLine = pg.InfiniteLine(pos=-30, angle=0, movable=True, pen='r')
        data400.addItem(hLine, ignoreBounds=True)
        self.region400.setRegion([400e6, 420e6])
        data400.addItem(self.region400)

        self.plota800 = data800.plot()
        self.plotb800 = data800.plot()
        data800.showGrid(x=True, y=True, alpha=1)
        data800.setLimits(xMin=650e6, xMax=1000e6, yMin=-70, yMax=-10)
        self.region800 = pg.LinearRegionItem()
        self.region800.setRegion([650e6, 700e6])
        data800.addItem(self.region800)

        self.plota1200 = data1200.plot()
        self.plotb1200 = data1200.plot()
        data1200.showGrid(x=True, y=True, alpha=1)
        data1200.setLimits(xMin=1000e6, xMax=1900e6, yMin=-70, yMax=-10)
        self.region1200 = pg.LinearRegionItem()
        self.region1200.setRegion([1000e6, 1020e6])
        data1200.addItem(self.region1200)

        self.plota2400 = data2400.plot()
        self.plotb2400 = data2400.plot()
        data2400.showGrid(x=True, y=True, alpha=1)
        data2400.setLimits(xMin=2100e6, xMax=2700e6, yMin=-70, yMax=-10)
        self.region2400 = pg.LinearRegionItem()
        self.region2400.setRegion([2100e6, 2150e6])
        data2400.addItem(self.region2400)

        self.tread = Tread()
        self.peak=peak_detection()
#        self.tread1 = Tread1()
 #       self.tread2 = Tread2()
 #       self.tread3 = Tread3()
        self.thread4 = Tread_demod()
    @staticmethod
    def test_400(item):
        if item.checkState() == QtCore.Qt.Checked:
            print(u'"{}" Checked'.format(item.row()))
            value_400.filter_mass_400.remove(value_400.filter_mass_400[item.row()])
            window.tableWidget.removeRow(item.row())

    @staticmethod
    def test_800(item):
        if item.checkState() == QtCore.Qt.Checked:
            print(u'"{}" Checked'.format(item.row()))
            filter_mass_800.remove(filter_mass_800[item.row()])
            window.tableWidget_2.removeRow(item.row())

    @staticmethod
    def test_1200(item):
        if item.checkState() == QtCore.Qt.Checked:
            print(u'"{}" Checked'.format(item.row()))
            filter_mass_1200.remove(filter_mass_1200[item.row()])
            window.tableWidget_3.removeRow(item.row())

    @staticmethod
    def test_2400(item):
        if item.checkState() == QtCore.Qt.Checked:
            print(u'"{}" Checked'.format(item.row()))
            filter_mass_2400.remove(filter_mass_2400[item.row()])
            window.tableWidget_4.removeRow(item.row())

    def start_write_400(self,region,filter_mass,table):
        lo, hi = region.getRegion()
        filter_mass.append([lo, hi])
        row = len(filter_mass) - 1
        item = QtGui.QTableWidgetItem('Text')
        table.insertRow(row)
        table.setItem(row, 0, QtGui.QTableWidgetItem(str(lo/1e6)))
        table.setItem(row, 1, QtGui.QTableWidgetItem(str(hi/1e6)))
        if row + 1:
            item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
        table.setItem(row, 2, item)

    def on_start(self):
        self.thread4.quit()
        value_400.flag400.value = 1
        self.tread.start()
        self.peak.start()
        # self.tread2.start()
        # self.tread3.start()

    def demodulation(self):
        lo, hi=self.region400.getRegion()
        value_400.start_freq_400.value=lo
        value_400.stop_freq_400.value=hi
        self.tread.quit()
        self.thread4.start()
        value_400.flag400.value = 2
    def transmitter(self):
        lo, hi=self.region400.getRegion()
        value_400.start_freq_400.value=lo
        value_400.stop_freq_400.value=hi
        self.tread.quit()
        self.thread4.quit()
        value_400.flag400.value=3
    def gen_data_tx(self,metod):
        if metod==1:
            value_400.transmit_data400[:]=np.array(np.fft.fft(np.random.randint(-1, 1, value_400.transmit_data400.size)),dtype=np.complex64)
            for i in range(value_400.transmit_data400.size):
                if value_400.transmit_data400[i] > 0:
                    value_400.transmit_data400[i]=1
                else:
                    value_400.transmit_data400[i]=-1
            value_400.transmit_data400[:]=value_400.transmit_data400
class Tread_demod(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()

        self.img_array = np.zeros((1000, value_400.demod_arr400.size / 2 + 1))
        freq = np.arange(( value_400.demod_arr400.size / 4) + 1) / (float( value_400.demod_arr400.size) / 50e6)
        self.yscale = 1.0 / (self.img_array.shape[1] / freq[-1])
        self.win = np.hanning( value_400.demod_arr400.size)

        self.interval = 50e6 /  value_400.demod_arr400.size
    def run(self):
        self.timer1.timeout.connect(self.plot_data)
        self.timer1.start(0.000001)
        self.timer2.timeout.connect(self.plot_waterfall)
        self.timer2.start(1000 / self.interval)

    def plot_data(self):
        window.data_demod.setData(10.0 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(value_400.demod_arr400)))))

    def plot_waterfall(self):
        spec = np.fft.rfft( value_400.demod_arr400 * self.win) /  value_400.demod_arr400.size
        psd = abs(spec)
        psd = 20 * np.log10(psd)
        self.img_array = np.roll(self.img_array, -1, 0)
        self.img_array[-1:] = psd
        window.image_item.setImage(self.img_array.T, autoLevels=False)

class Tread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.timer1 = QtCore.QTimer()

    def run(self):
        self.timer1.timeout.connect(self.plot_data)
        self.timer1.start(1)

    def plot_data(self):
        app.processEvents()
        window.plota400.setData(400e6 + (band / 2048) * np.arange(8192), value_400.arr400)

        window.plotb400.setData(400e6 + (band / 2048) * np.arange(8192), value_400.maxhold400, pen='r')
class peak_detection(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.timer=QtCore.QTimer()
    def run(self):
        window.tableWidget.itemClicked.connect(self.filters)
        self.table_peak()
        self.timer.timeout.connect(self.add_new_peak)
        self.timer.start(10)
    def table_peak(self):
        self.len_peak=len(value_400.peak400)
        for number,data in enumerate(value_400.peak400):
            item=QtGui.QTableWidgetItem('Filter')
            window.tableWidget.insertRow(number)
            window.tableWidget.setItem(number, 0, QtGui.QTableWidgetItem(str((400e6+(band/value_400.arr400.size)*data)/1e6)))
            window.tableWidget.setItem(number, 1, QtGui.QTableWidgetItem(str(value_400.arr400[data])))
            if number + 1:
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked)
            print(number)
            window.tableWidget.setItem(number, 2, item)
    def add_new_peak(self):
        if self.len_peak!=len(value_400.peak400):
            window.tableWidget.insertRow(len(value_400.peak400)-1)
            window.tableWidget.setItem(len(value_400.peak400)-1, 0, QtGui.QTableWidgetItem(str(value_400.peak400[len(value_400.peak400)-1])))
        #table.setItem(row, 2, item)
    def filters(self,item):
        if item.checkState() == QtCore.Qt.Checked:
            print(u'"{}" Checked'.format(item.column()))
            #value_400.filter_mass_400.remove(value_400.filter_mass_400[item.row()])
            window.tableWidget.removeRow(item.row())


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    window = My_Windows()
    window.show()
    if __name__ == '__main__':
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
