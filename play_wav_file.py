# https://realpython.com/playing-and-recording-sound-python/#python-sounddevice
import sounddevice as sd
import soundfile as sf

filename = 'imperial_march.wav'

data, fs = sf.read(filename, dtype='float32')
sd.play(data, fs)
status = sd.wait()
