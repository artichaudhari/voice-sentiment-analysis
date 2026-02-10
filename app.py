import streamlit as st
import speech_recognition as sr
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import plotly.graph_objects as go
from pydub import AudioSegment
import tempfile
import os

# ---------- NLTK ----------
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="VibeAI Premium",
    page_icon="💎",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 20% 10%, #1e293b 0%, #0f172a 100%);
    color: white;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.glass-card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
}
</style>
""", unsafe_allow_html=True)

# ---------- AUDIO CONVERSION ----------
def convert_to_wav(uploaded_file):
    audio = AudioSegment.from_file(uploaded_file)
    audio = (
        audio
        .set_channels(1)
        .set_frame_rate(16000)
        .set_sample_width(2)
    )

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp.name, format="wav")
    return temp.name

# ---------- HEADER ----------
st.markdown("<h1 style='text-align:center;'>💎 VibeAI Premium</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#94a3b8;'>Sophisticated Voice Emotion Analytics</p>",
    unsafe_allow_html=True
)

# ---------- MAIN ----------
col1, col2 = st.columns([1, 1.2], gap="large")

text = None
scores = None

with col1:
    st.subheader("🎙️ Upload Audio")

    audio_file = st.file_uploader(
        "Supported: WAV, MP3, M4A, OGG",
        type=["wav", "mp3", "m4a", "ogg"]
    )

    if audio_file:
        st.audio(audio_file)

        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True

        with st.spinner("✨ Processing audio..."):
            try:
                wav_path = convert_to_wav(audio_file)

                with sr.AudioFile(wav_path) as source:
                    audio_data = recognizer.record(
                        source,
                        duration=30
                    )

                text = recognizer.recognize_google(audio_data)
                scores = sia.polarity_scores(text)

                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("**📝 Transcription**")
                st.write(f'"{text}"')
                st.markdown("</div>", unsafe_allow_html=True)

            except sr.UnknownValueError:
                st.error("❌ Speech not clear enough to recognize.")
            except sr.RequestError:
                st.error("❌ Google Speech API unavailable.")
            except Exception as e:
                st.error(f"❌ Processing error: {e}")
            finally:
                if "wav_path" in locals() and os.path.exists(wav_path):
                    os.remove(wav_path)

with col2:
    if text and scores:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=(scores["compound"] + 1) * 50,
            title={"text": "Sentiment Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#6366f1"},
                "steps": [
                    {"range": [0, 35], "color": "rgba(239,68,68,0.35)"},
                    {"range": [35, 65], "color": "rgba(234,179,8,0.35)"},
                    {"range": [65, 100], "color": "rgba(34,197,94,0.35)"}
                ]
            }
        ))

        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )

        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Positive", f"{scores['pos']:.2f}")
        c2.metric("Neutral", f"{scores['neu']:.2f}")
        c3.metric("Negative", f"{scores['neg']:.2f}")

    else:
        st.markdown("""
        <div class="glass-card" style="height:360px;display:flex;align-items:center;justify-content:center;">
            <p style="color:#94a3b8;">Upload audio to view emotional analysis</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;color:#94a3b8;'>Powered by VADER & Google Speech Recognition</p>",
    unsafe_allow_html=True
)
