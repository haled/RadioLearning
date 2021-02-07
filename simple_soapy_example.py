import simplesoapy
import numpy
import pyaudio


# List all connected SoapySDR devices
print(simplesoapy.detect_devices(as_string=True))

# Initialize SDR device
sdr = simplesoapy.SoapyDevice('driver=lime')

# Set sample rate
sdr.sample_rate = 5e6

# Set center frequency
sdr.freq = 94.7e6

#p = pyaudio.PyAudio()
#audioStream = p.open(output = True)
    
# Setup base buffer and start receiving samples. Base buffer size is determined
# by SoapySDR.Device.getStreamMTU(). If getStreamMTU() is not implemented by driver,
# SoapyDevice.default_buffer_size is used instead
sdr.start_stream()

# Create numpy array for received samples
samples = numpy.empty(len(sdr.buffer) * 100, numpy.complex64)

# Receive all samples
sdr.read_stream_into_buffer(samples)
w = open("simplesoapy.wav", "wb")
w.write(samples)
w.close()
#stream.write(data)
    
# Stop receiving
sdr.stop_stream()
#p.close()
#p.terminate()
