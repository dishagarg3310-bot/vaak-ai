import streamlit as st
import whisper
from gtts import gTTS
import os
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wav

st.set_page_config(page_title="VaakAI", page_icon="🎙️", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

# --- HOME PAGE ---
if st.session_state.page == "home":
    st.markdown("""
        <h1 style='text-align: center; font-size: 3em;'>🎙️ VaakAI</h1>
        <h3 style='text-align: center; color: gray;'>Hindi & English Speech Assistant</h3>
        <br><br>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style='background-color:#1e1e2e; border-radius:15px; padding:40px; 
            text-align:center; border:1px solid #444; min-height:250px;'>
            <h1>🎤</h1>
            <h2>Speech to Text</h2>
            <p style='color:gray;'>Record your voice or upload audio and convert it to text</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Open Speech to Text →", use_container_width=True):
            st.session_state.page = "stt"
            st.rerun()

    with col2:
        st.markdown("""
            <div style='background-color:#1e1e2e; border-radius:15px; padding:40px; 
            text-align:center; border:1px solid #444; min-height:250px;'>
            <h1>🔊</h1>
            <h2>Text to Speech</h2>
            <p style='color:gray;'>Type any text and convert it to natural voice</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Open Text to Speech →", use_container_width=True):
            st.session_state.page = "tts"
            st.rerun()

# --- STT PAGE ---
elif st.session_state.page == "stt":
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("# 🎤 Speech to Text")
    st.markdown("---")

    language = st.selectbox("Select Language:", ["English", "Hindi"])
    lang = "hi" if language == "Hindi" else "en"

    st.subheader("🔴 Live Recording")
    duration = st.slider("Recording duration (seconds):", 3, 10, 5)

    if st.button("Start Recording 🎙️", use_container_width=True):
        with st.spinner(f"Recording for {duration} seconds... Speak now!"):
            sample_rate = 16000
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype='int16'
            )
            sd.wait()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                wav.write(tmp.name, sample_rate, recording)
                tmp_path = tmp.name

        with st.spinner("Transcribing..."):
            model = whisper.load_model("base")
            result = model.transcribe(tmp_path, language=lang)
            os.unlink(tmp_path)

        st.success("✅ Transcription:")
        st.markdown(f"### {result['text']}")

    st.markdown("---")
    st.subheader("📁 Upload Audio File")
    audio_file = st.file_uploader("Upload .wav file", type=["wav", "mp3"])

    if audio_file and st.button("Transcribe ▶️", use_container_width=True):
        with st.spinner("Transcribing..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name

            model = whisper.load_model("base")
            result = model.transcribe(tmp_path, language=lang)
            os.unlink(tmp_path)

        st.success("✅ Transcription:")
        st.markdown(f"### {result['text']}")

# --- TTS PAGE ---
elif st.session_state.page == "tts":
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("# 🔊 Text to Speech")
    st.markdown("---")

    tts_language = st.selectbox("Select Language:", ["English", "Hindi"])
    text_input = st.text_area("Enter text here:", height=150)

    if st.button("Generate Speech 🔊", use_container_width=True):
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
            st.warning("Please enter some text first!")