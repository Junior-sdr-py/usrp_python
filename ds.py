from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

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

a,b =signal.butter(2,[0.21,0.32],'bandstop')
fy = signal.filtfilt(a,b,y1)

# Frequency response

# Generate frequency axis

yf1=np.fft.fft(fy)
yf1=2.0 / N * np.abs(yf1[:N / 2])

yf2=np.fft.fft(y1)
yf2=2.0 / N * np.abs(yf2[:N / 2])



# Plot
fig, ax = plt.subplots(4, 1, figsize=(8, 6))
ax[0].plot(y1)
ax[1].plot(20*np.log10(np.abs(np.fft.rfft(y1))))
ax[2].plot(yf1)
ax[3].plot(yf2)
plt.show()

