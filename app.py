import streamlit as st
import speech_recognition as sr
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import plotly.graph_objects as go
from pydub import AudioSegment
import tempfile
import os

# Ensure VADER lexicon
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

st.set_page_config(page_title="VibeAI Premium", page_icon="💎", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
.stApp {
    background: radial-gradient(circle at 20% 10%, #1e293b 0%, #0f172a 100%);
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.glass-card {
    background: rgba(255,255,255,0.05);
    border-radius: 24px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
}
.metric-box {
    text-align:center;
    padding:15px;
    border-radius:15px;
    background: rgba(255,255,255,0.03);
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1 style='text-align:center;'>💎 VibeAI Premium</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#94a3b8;'>Sophisticated Voice Emotion Analytics</p>", unsafe_allow_html=True)

# ---------- AUDIO HANDLING ----------
def convert_to_wav(uploaded_file):
    audio = AudioSegment.from_file(uploaded_file)
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_wav.name, format="wav")
    return temp_wav.name

# ---------- MAIN ----------
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("🎙️ Upload Audio")
    audio_file = st.file_uploader(
        "Supports WAV, MP3, MPEG, M4A, OGG",
        type=["wav", "mp3", "mpeg", "m4a", "ogg"]
    )

    if audio_file:
        st.audio(audio_file)

        recognizer = sr.Recognizer()
        with st.spinner("✨ Processing audio..."):
            try:
                # Convert any format to WAV
                wav_path = convert_to_wav(audio_file)

                with sr.AudioFile(wav_path) as source:
                    audio = recognizer.record(source)

                text = recognizer.recognize_google(audio)
                os.remove(wav_path)

                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("**📝 Transcription**")
                st.write(text)
                st.markdown("</div>", unsafe_allow_html=True)

                scores = sia.polarity_scores(text)
                compound = scores["compound"]

            except Exception as e:
                st.error("❌ Unable to process audio. Please try a clearer file.")
                text = None

with col2:
    if audio_file and text:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=(compound + 1) * 50,
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#6366f1"},
                "steps": [
                    {"range": [0, 35], "color": "rgba(239,68,68,0.3)"},
                    {"range": [35, 65], "color": "rgba(234,179,8,0.3)"},
                    {"range": [65, 100], "color": "rgba(34,197,94,0.3)"}
                ],
            }
        ))

        fig.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )

        st.plotly_chart(fig, use_container_width=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Positive", f"{scores['pos']:.2f}")
        m2.metric("Neutral", f"{scores['neu']:.2f}")
        m3.metric("Negative", f"{scores['neg']:.2f}")

    else:
        st.markdown("""
        <div class="glass-card" style="height:380px;display:flex;align-items:center;justify-content:center;">
            <p style="color:#64748b;">Upload any audio to begin analysis</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#475569;'>Powered by VADER & Speech Recognition</p>", unsafe_allow_html=True)
