import os
import pandas as pd
import librosa
import soundfile as sf

def preprocess_audio(input_path, output_path):
    audio, sr = librosa.load(input_path, sr=16000, mono=True)
    sf.write(output_path, audio, 16000)

def build_csv(language):
    audio_folder = f"../dataset/{language}/audio"
    transcript_folder = f"../dataset/{language}/transcripts"
    output_folder = f"../preprocessed"
    os.makedirs(output_folder, exist_ok=True)

    data = []
    for filename in os.listdir(audio_folder):
        if filename.endswith(".wav"):
            audio_path = os.path.join(audio_folder, filename)
            txt_path = os.path.join(transcript_folder, filename.replace(".wav", ".txt"))

            if os.path.exists(txt_path):
                with open(txt_path, "r", encoding="utf-8") as f:
                    transcript = f.read().strip()

                # Normalize audio
                preprocess_audio(audio_path, audio_path)
                data.append({"audio_path": audio_path, "transcript": transcript, "language": language})

    df = pd.DataFrame(data)
    csv_path = os.path.join(output_folder, f"{language}.csv")
    df.to_csv(csv_path, index=False)
    print(f"CSV saved: {csv_path}")
    print(df)

# --- Run ---
for lang in ["english", "hindi"]:
    build_csv(lang)

print("\nPreprocessing complete!")
