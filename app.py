import streamlit as st
import speech_recognition as sr
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import plotly.graph_objects as go
from pydub import AudioSegment
import tempfile
import os

# --- PRE-REQUISITES ---
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

# --- APP CONFIG ---
st.set_page_config(page_title="VibeAI Premium", page_icon="💎", layout="wide")

# --- CSS STYLING (UPDATED FOR WHITE TEXT) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

/* Global Background and Text Color */
.stApp {
    background: radial-gradient(circle at 20% 10%, #1e293b 0%, #0f172a 100%);
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: white !important;
}

/* Force headers, labels, and metrics to be white */
h1, h2, h3, p, span, label, .stMarkdown, [data-testid="stMetricValue"] {
    color: white !important;
}

/* Glassmorphism Card Effect */
.glass-card {
    background: rgba(255,255,255,0.05);
    border-radius: 24px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
    margin-bottom: 20px;
    color: white;
}

/* File Uploader Text */
.stFileUploader section {
    background-color: rgba(255, 255, 255, 0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def convert_to_wav(uploaded_file):
    try:
        audio = AudioSegment.from_file(uploaded_file)
        # Convert to mono and 16k Hz for better recognition
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(temp_wav.name, format="wav")
        return temp_wav.name
    except Exception as e:
        st.error(f"Audio Conversion Error: {e}")
        return None

# --- HEADER ---
st.markdown("<h1 style='text-align:center;'>💎 VibeAI Premium</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#94a3b8 !important;'>Sophisticated Voice Emotion Analytics</p>", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 1.2], gap="large")

text = None
scores = None

with col1:
    st.subheader("🎙️ Upload Audio")
    audio_file = st.file_uploader(
        "Supports WAV, MP3, M4A, OGG",
        type=["wav", "mp3", "m4a", "ogg"]
    )

    if audio_file:
        st.audio(audio_file)
        recognizer = sr.Recognizer()
        
        with st.spinner("✨ Analyzing speech patterns..."):
            wav_path = convert_to_wav(audio_file)
            
            if wav_path:
                try:
                    with sr.AudioFile(wav_path) as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio_data = recognizer.record(source)
                    
                    # Convert speech to text
                    text = recognizer.recognize_google(audio_data)
                    
                    # Sentiment Analysis
                    scores = sia.polarity_scores(text)

                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown("<b style='color:white;'>📝 Transcription</b>", unsafe_allow_html=True)
                    st.write(f'"{text}"')
                    st.markdown("</div>", unsafe_allow_html=True)

                except sr.UnknownValueError:
                    st.error("❌ Google Speech Recognition could not understand the audio.")
                except sr.RequestError:
                    st.error("❌ Service unavailable. Check your internet connection.")
                except Exception as e:
                    st.error(f"❌ Error processing file: {e}")
                finally:
                    if os.path.exists(wav_path):
                        os.remove(wav_path)

with col2:
    if audio_file and text and scores:
        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=(scores['compound'] + 1) * 50,
            title={'text': "Sentiment Score", 'font': {'color': "white"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "white"},
                "bar": {"color": "#6366f1"},
                "steps": [
                    {"range": [0, 35], "color": "rgba(239,68,68,0.4)"},
                    {"range": [35, 65], "color": "rgba(234,179,8,0.4)"},
                    {"range": [65, 100], "color": "rgba(34,197,94,0.4)"}
                ],
            }
        ))

        fig.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )

        st.plotly_chart(fig, use_container_width=True)

        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Positive", f"{scores['pos']:.2f}")
        m2.metric("Neutral", f"{scores['neu']:.2f}")
        m3.metric("Negative", f"{scores['neg']:.2f}")

    else:
        st.markdown("""
        <div class="glass-card" style="height:380px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
            <p style="color:white;font-size:1.2rem;">Ready for Analysis</p>
            <p style="color:#94a3b8;">Upload a clear audio file to see the emotional breakdown.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center;color:#94a3b8 !important;'>Powered by VADER & Google Speech API</p>", unsafe_allow_html=True)
