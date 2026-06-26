import streamlit as st
import whisper
import pyttsx3
from gtts import gTTS
import os
import tempfile

st.set_page_config(page_title="VaakAI", page_icon="🎙️", layout="centered")

st.title("🎙️ VaakAI — Speech Assistant")
st.subheader("Hindi & English Speech to Text + Text to Speech")

# Tabs
tab1, tab2 = st.tabs(["🎙️ Speech to Text", "🔊 Text to Speech"])

# --- STT Tab ---
with tab1:
    st.header("Speech → Text")
    language = st.selectbox("Language select karo:", ["English", "Hindi"])
    audio_file = st.file_uploader("Audio file upload karo (.wav)", type=["wav", "mp3"])
    
    if audio_file and st.button("Transcribe karo"):
        with st.spinner("Transcribing..."):
            # Save temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            
            # Load model and transcribe
            model = whisper.load_model("base")
            lang = "hi" if language == "Hindi" else "en"
            result = model.transcribe(tmp_path, language=lang)
            
            st.success("✅ Transcription:")
            st.write(result["text"])
            os.unlink(tmp_path)

# --- TTS Tab ---
with tab2:
    st.header("Text → Speech")
    tts_language = st.selectbox("Language:", ["English", "Hindi"])
    text_input = st.text_area("Text likho:")
    
    if st.button("Speak karo"):
        if text_input:
            with st.spinner("Generating audio..."):
                lang_code = "hi" if tts_language == "Hindi" else "en"
                tts = gTTS(text=text_input, lang=lang_code)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    tmp_path = tmp.name
                
                st.success("✅ Audio ready!")
                st.audio(tmp_path)
        else:
            st.warning("Pehle text likho!")