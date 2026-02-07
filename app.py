import streamlit as st
import speech_recognition as sr
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import plotly.graph_objects as go

# Ensure VADER lexicon is downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

# Page Setup - 'wide' is better for side-by-side dashboards
st.set_page_config(page_title="VibeAI Premium", page_icon="💎", layout="wide")

# --- ENHANCED CLASSY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at 20% 10%, #1e293b 0%, #0f172a 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Modern Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #475569; border-radius: 10px; }

    /* Glass Card Refinement */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Gradient Title */
    .title-text {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -3px;
        text-align: center;
        margin-bottom: 0px;
    }

    .sub-text {
        color: #94a3b8;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 50px;
        font-weight: 300;
    }

    /* Metric Box */
    .metric-box {
        text-align: center;
        padding: 15px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.03);
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI HEADER ---
st.markdown('<h1 class="title-text">VibeAI Premium</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Sophisticated Voice Emotion Analytics</p>', unsafe_allow_html=True)

# --- MAIN CONTENT AREA ---
# Using a central container to keep things from touching the screen edges
main_container = st.container()

with main_container:
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown("### 🎙️ Audio Input")
        with st.container(): # Grouping for better spacing
            audio_file = st.file_uploader("", type=["wav"], label_visibility="collapsed")
            
            if audio_file:
                st.audio(audio_file, format='audio/wav')
                
                recognizer = sr.Recognizer()
                with st.spinner("✨ Decoding Audio Stream..."):
                    try:
                        with sr.AudioFile(audio_file) as source:
                            audio = recognizer.record(source)
                        text = recognizer.recognize_google(audio)
                        
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.markdown("<p style='color:#6366f1; font-weight:700; font-size:0.8rem; margin-bottom:10px;'>TRANSCRIPTION</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='font-size:1.2rem; line-height:1.6; color:#e2e8f0;'>\"{text}\"</p>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        scores = sia.polarity_scores(text)
                        compound = scores["compound"]
                    except:
                        st.error("Neural engine failed to parse audio. Try a clearer file.")
                        text = None

    with col2:
        if audio_file and text:
            # st.markdown("### 💎 Emotional Intelligence")
            st.markdown("<h3 style='color: white;'>💎 Emotional Intelligence</h3>", unsafe_allow_html=True)
            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = (compound + 1) * 50,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                    'bar': {'color': "#6366f1"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 35], 'color': 'rgba(239, 68, 68, 0.2)'},
                        {'range': [35, 65], 'color': 'rgba(234, 179, 8, 0.2)'},
                        {'range': [65, 100], 'color': 'rgba(34, 197, 94, 0.2)'}
                    ],
                }
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font={'color': "#f8fafc", 'family': "Plus Jakarta Sans"}, 
                height=380,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)

            # Styled Metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="metric-box"><p style="color:#94a3b8;margin:0;">Positive</p><h2 style="color:#22c55e;margin:0;">{scores["pos"]:.2f}</h2></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-box"><p style="color:#94a3b8;margin:0;">Neutral</p><h2 style="color:#eab308;margin:0;">{scores["neu"]:.2f}</h2></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-box"><p style="color:#94a3b8;margin:0;">Negative</p><h2 style="color:#ef4444;margin:0;">{scores["neg"]:.2f}</h2></div>', unsafe_allow_html=True)
                
        else:
            # Placeholder for empty state
            st.markdown("""
                <div class="glass-card" style="height: 400px; display: flex; align-items: center; justify-content: center; border: 2px dashed rgba(255,255,255,0.1);">
                    <div style="text-align:center;">
                        <h2 style="color: #475569; margin-bottom:0;">Awaiting Input</h2>
                        <p style="color: #475569;">Upload audio to begin analysis</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br><p style='text-align:center; color:#475569; font-size:0.9rem;'>Powered by VADER Sentiment & Google Speech Engine</p>", unsafe_allow_html=True)