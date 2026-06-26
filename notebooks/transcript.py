import os

def save_transcript(filename, text, language):
    folder = f"../dataset/{language}/transcripts"
    os.makedirs(folder, exist_ok=True)
    
    # Same name, .txt extension
    txt_filename = filename.replace(".wav", ".txt")
    filepath = os.path.join(folder, txt_filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Transcript saved: {filepath}")

# --- Run karo ---
lang = input("Language? (hindi/english): ").strip().lower()
fname = input("Audio file name (e.g. sample_001.wav): ").strip()
transcript = input("Jo bola tune wo likho: ").strip()

save_transcript(fname, transcript, lang)