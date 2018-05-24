import pyqtgraph as pg
import numpy as np
'''app = pg.mkQApp()
plt = pg.PlotItem()
imv = pg.ImageView(view=plt)
imv.setImage(pg.np.random.normal(size=(10,10)))
imv.show()
imv.getView().invertY(False)
'''
arr=np.zeros((1000,8192))
print ("array1",arr)
arr = np.roll(arr, -1, 0)
print('arrroll',arr.shape)
print(arr[-1:].shape)