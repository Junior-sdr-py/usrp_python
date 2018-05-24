from PyQt4 import QtCore,QtGui
class Window(QtGui.QWidget):
    def __init__(self,rows,columns):
        QtGui.QWidget.__init__(self)
        self.table=QtGui.QTableWidget(rows,columns,self)
        for columns in range(columns):
            for row in range(rows):
                item=QtGui.QTableWidgetItem('Text%d' % row)
                if row:
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable|
                                  QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked)
                self.table.setItem(row,columns,item)
        self.table.itemClicked.connect(self.test)
        layout=QtGui.QVBoxLayout(self)
        layout.addWidget(self.table)
        self._list=[]
    def test(self,item):
        if item.checkState()==QtCore.Qt.Checked:
            print('"%s" Checked' %item.pow())
        else:
            print (2)
if __name__ == '__main__':
    import sys
    app=QtGui.QApplication(sys.argv)
    window=Window(6,3)
    window.resize(350,300)
    window.show()
    sys.exit(app.exec_())