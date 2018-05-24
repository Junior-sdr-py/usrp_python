#-*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore, uic
import datetime

today = datetime.datetime.today()
dist=[[today,400,500],[today,600,700],[today,900,1000],[today,2300,2500]]
app = QtGui.QApplication(sys.argv)
tables1 = QtGui.QTableWidget()
tables1.setRowCount(len(dist))
tables1.setColumnCount(4)
def testing():
    pass

for row_number,row_data in enumerate(dist):
    item=QtGui.QTableWidgetItem('Жмак')
    item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                  QtCore.Qt.ItemIsEnabled)
    item.setCheckState(QtCore.Qt.Unchecked)
    tables1.setItem(row_number,3,item)
    tables1.itemClicked.connect(testing)
    for column_number,data in enumerate(row_data):
        tables1.setItem(row_number,column_number,QtGui.QTableWidgetItem(str(data)))
layout=QtGui.QVBoxLayout()
layout.addWidget(tables1)




#tables1.itemDoubleClicked.connect(testing)

'''
for row_number, row_data in enumerate(res):
    tables1.tableWidget.insertRow(row_number)
    for column_number, data in enumerate(row_data):
            tables1.tableWidget.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))'''
tables1.show()
if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()