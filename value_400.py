import multiprocessing
import numpy as np
flag400 = multiprocessing.Value('i', 1)

transmit_data400= multiprocessing.Array('d', 4096*6)
transmit_data400 = np.frombuffer(transmit_data400.get_obj())

arr400 = multiprocessing.Array('d', 8193)
arr400 = np.frombuffer(arr400.get_obj())


start_freq_400=multiprocessing.Value('f', 1)
stop_freq_400=multiprocessing.Value('f', 1)


demod_arr400 = multiprocessing.Array('d', 8192)
demod_arr400 = np.frombuffer(demod_arr400.get_obj())

manager = multiprocessing.Manager()

filter_mass_400 = manager.list()

maxhold400 = multiprocessing.Array('d', 8192)

maxhold400 = np.frombuffer(maxhold400.get_obj())

maxhold400[:] = np.ones(8192) * -1000

peak400=manager.list()
filter_list=manager.list()