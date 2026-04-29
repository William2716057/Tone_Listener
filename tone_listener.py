import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100
SIGNAL = 2000
DURATION = 1.5
DURATION_MS = 200
DURATION_S = DURATION_MS / 1000
FREQ_TOLERANCE = 80

CHUNK = int(SAMPLE_RATE * DURATION_S)

def dominant_freq(audio_chunk):
    fft = np.abs(np.fft.rfft(audio_chunk))
    freqs = np.fft.rfftfreq(len(audio_chunk), 1 / SAMPLE_RATE)
    return freqs[np.argmax(fft)]

#define tolerance for false detections
def near(freq, target, tolerance=FREQ_TOLERANCE):
    return abs(freq - target) < tolerance
    
def listen_for_tone(stream):
    print("Listening for tone.....")
    #initialise consecutive 
    consecutive = 0
    required = int(DURATION * 1000/ DURATION_MS)
    
    while True:
        audio, _ = stream.read(CHUNK)
        freq = dominant_freq(audio[:, 0])
        if near(freq, SIGNAL):
            consecutive += 1
            if consecutive >= required:
                print("Signal detected")
                return
    else:
        consecutive = 0

#listen_for_tone(stream)

with sd.InputStream(SAMPLE_RATE, channels=1) as stream:
    listen_for_tone(stream)
    
        