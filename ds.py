from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
def detect_start_stop(center_sample,data,start=0,stop=0):
    for i in range(center_sample,data.size):
        data[i]
        if data[i]<=0.1:
            print(data[i])
            start=i
            break
    for i in range(center_sample,0,-1):
        if data[i] <=0.2 :
            stop=i
            break
    return start,stop
def filter(filt_list,data,num_samps):
    global data1
    for i in filt_list:
        a,b=signal.butter(6,[float(i[0])/(num_samps/2),float(i[1])/(num_samps/2)],'bandstop')
        data=signal.filtfilt(a,b,data)
    return data
filt=[[48,55],[79,82]]
print(np.arange(100,0,-1))
N=800
# sample spacing
T=1.0 / 800.0
x=np.linspace(0.0, N * T, N)
y1=np.sin(50.0 * 2.0 * np.pi * x) + 0.5 * np.sin(80.0 * 2.0 * np.pi * x) + 0.7 * np.sin(
    30.0 * 2.0 * np.pi * x) + 0.5 * np.sin(10.0 * 2.0 * np.pi * x)
'''y2=np.sin(50.0 * 2.0 * np.pi * x) + 0.5 * np.sin(80.0 * 2.0 * np.pi * x) + 0.2 * np.sin(
    60.0 * 2.0 * np.pi * x) + 0.4 * np.sin(40.0 * 2.0 * np.pi * x)'''
#
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
# Frequency response

# Generate frequency axis


yf1=np.fft.fft(filter(filt,y1,800))
yf1=2.0 / N * np.abs(yf1[:N / 2])

yf2=np.fft.fft(y1)
yf2=2.0 / N * np.abs(yf2[:N / 2])
start,stop=detect_start_stop(50,yf2)
print(start)
print(stop)


# Plot
fig, ax = plt.subplots(4, 1, figsize=(8, 6))
ax[0].plot(y1)
ax[1].plot(20*np.log10(np.abs(np.fft.rfft(y1))))
ax[2].plot(yf2)
ax[3].plot(yf1)
plt.show()

