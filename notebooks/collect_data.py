import pyaudio
import wave
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

def record_and_save(sample_num, language):
    audio_folder = f"../dataset/{language}/audio"
    transcript_folder = f"../dataset/{language}/transcripts"
    os.makedirs(audio_folder, exist_ok=True)
    os.makedirs(transcript_folder, exist_ok=True)

    filename = f"sample_{sample_num:03d}.wav"
    audio_path = os.path.join(audio_folder, filename)
    transcript_path = os.path.join(transcript_folder, filename.replace(".wav", ".txt"))

    transcript = input(f"[{language.upper()}] Sample {sample_num} - Jo bologe wo likho: ").strip()

    print("3 seconds mein bolna shuru karo...")
    import time
    time.sleep(3)
    print("Recording...")

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Done!")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(audio_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Saved: {filename} + transcript\n")

# --- Main ---
lang = input("Language? (hindi/english): ").strip().lower()
total = int(input("Kitne samples record karne hain?: "))

for i in range(1, total + 1):
    record_and_save(i, lang)

print("All samples done!")