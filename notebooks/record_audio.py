import pyaudio
import wave
import os

# Config
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

def record_audio(filename, language):
    folder = f"../dataset/{language}/audio"
    os.makedirs(folder, exist_ok=True)
    
    filepath = os.path.join(folder, filename)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    
    print(f"Recording... (5 seconds)")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Done!")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Saved: {filepath}")

# --- Run karo ---
lang = input("Language? (hindi/english): ").strip().lower()
fname = input("File name (e.g. sample_001.wav): ").strip()
record_audio(fname, lang)