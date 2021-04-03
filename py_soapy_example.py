import SoapySDR
from SoapySDR import *
import numpy as np
# 2nd step
from matplotlib import pyplot as plt
from SoapySDR import SOAPY_SDR_RX, SOAPY_SDR_CS16

results = SoapySDR.Device.enumerate()
for result in results:
    print(result)

# 2nd step
rx_channel = 0
sample_rate = 5e6
frequency = 94.7e6
rx_bits = 16
num_complex_samples_per_transfer = 16384
N = num_complex_samples_per_transfer
use_agc = True
timeout_us = int(5e6)

limeSDR = SoapySDR.Device("driver=lime")
limeSDR.setSampleRate(SOAPY_SDR_RX, rx_channel, sample_rate)
limeSDR.setGainMode(SOAPY_SDR_RX, rx_channel, use_agc)
limeSDR.setFrequency(SOAPY_SDR_RX, rx_channel, frequency)

rx_buffer = np.empty(2 * num_complex_samples_per_transfer, np.int16)
rx_stream = limeSDR.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CS16, [rx_channel])
limeSDR.activateStream(rx_stream)

streamReader = limeSDR.readStream(rx_stream, [rx_buffer], num_complex_samples_per_transfer, timeoutUs=timeout_us)
rc = streamReader.ret
assert rc == num_complex_samples_per_transfer, 'Error reading samples from device (error code = %d)' % rc

limeSDR.deactivateStream(rx_stream)
limeSDR.closeStream(rx_stream)

# below is copied from https://docs.deepwavedigital.com/Tutorials/1_hello_world.html
############################################################################################
# Plot Signal
############################################################################################
# Convert interleaved shorts (received signal) to numpy.complex64 normalized between [-1, 1]
s0 = rx_buffer.astype(float) / np.power(2.0, rx_bits-1)
s = (s0[::2] + 1j*s0[1::2])

# Take the fourier transform of the signal and perform FFT Shift
S = np.fft.fftshift(np.fft.fft(s, N) / N)

# Time Domain Plot
plt.figure(num=1, figsize=(12.95, 7.8), dpi=150)
plt.subplot(211)
t_us = np.arange(N) / sample_rate / 1e-6
plt.plot(t_us, s.real, 'k', label='I')
plt.plot(t_us, s.imag, 'r', label='Q')
plt.xlim(t_us[0], t_us[-1])
plt.xlabel('Time (us)')
plt.ylabel('Normalized Amplitude')

# Frequency Domain Plot
plt.subplot(212)
f_ghz = (frequency + (np.arange(0, sample_rate, sample_rate/N) - (sample_rate/2) + (sample_rate/N))) / 1e9
plt.plot(f_ghz, 20*np.log10(np.abs(S)))
plt.xlim(f_ghz[0], f_ghz[-1])
plt.ylim(-100, 0)
plt.xlabel('Frequency (GHz)')
plt.ylabel('Amplitude (dBFS)')
plt.show()
# end copied code
