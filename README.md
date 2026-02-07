
# 🎙️ VibeAI: Voice Sentiment Analysis Dashboard

An end-to-end **AI-powered Web Application** that transcribes human speech and analyzes emotional sentiment in real-time.  
This project demonstrates expertise in **Natural Language Processing (NLP)**, **Speech Recognition**, **Data Visualization**, and **Streamlit Dashboarding**.

---

## 🖼️ Project Overview
<img width="1781" height="781" alt="Screenshot 2026-02-07 144624" src="https://github.com/user-attachments/assets/0e4ee6db-0543-422d-b94b-56ebc55261f4" />

VibeAI provides a "Classy & Premium" interface for users to upload voice files and receive instant emotional intelligence insights. It converts complex audio data into actionable sentiment metrics (Positive, Neutral, Negative) using the VADER algorithm.



---

## 🧭 Purpose & Objective

This project was developed to:
- Bridge the gap between **Audio Signal Processing** and **Text Analytics**.
- Implement **VADER (Valence Aware Dictionary and sEntiment Reasoner)** for nuanced emotional detection.
- Create a high-end **Glassmorphism UI** for data presentation.
- Demonstrate end-to-end deployment of a Machine Learning-powered tool.

---

## 🧰 Tech Stack

- **Python 3.x** – Core Logic  
- **Streamlit** – Premium Frontend & Dashboarding  
- **NLTK (VADER)** – Sentiment Analysis Engine  
- **SpeechRecognition** – Google Web Speech API Integration  
- **Plotly** – Interactive Dynamic Gauge Charts  
- **CSS3** – Custom Glassmorphism Styling  

---

## 📂 Project Structure

The application follows a modular architecture for easy scalability:

```text
voice-sentiment-dashboard/
│
├── app.py              # Main Streamlit Application & UI logic
├── requirements.txt    # Project dependencies (Streamlit, NLTK, Plotly, etc.)
├── nltk_data/          # Local storage for VADER lexicon
└── README.md           # Project documentation

```

---

## 🛠️ Technical Workflow

### 1️⃣ Speech-to-Text (STT) Layer

* The system accepts `.wav` audio files.
* It utilizes the **Google Speech Recognition engine** to convert audio frequencies into clean, structured text.
* Implements error handling for low-clarity audio or background noise.

### 2️⃣ Sentiment Intelligence Engine

* The transcribed text is processed through **NLTK's SentimentIntensityAnalyzer**.
* It calculates a **Compound Score** (ranging from -1 to +1) to determine the overall "Vibe" of the speech.

### 3️⃣ Data Visualization Dashboard

* **Dynamic Gauge:** A Plotly-powered visual index showing the intensity of the sentiment.
* **Metric Cards:** Real-time breakdown of Positivity, Neutrality, and Negativity percentages.
* **Glassmorphism UI:** A sleek, dark-themed interface using custom CSS for a professional SaaS feel.

---

## ✨ Key Highlights & Learnings

* ✅ **Advanced NLP:** Mastered the use of VADER for social-media style sentiment nuances.
* ✅ **Interactive UI:** Implemented custom CSS and Plotly for a "Premium" user experience.
* ✅ **API Integration:** Seamlessly integrated external Speech-to-Text APIs.
* ✅ **Data Normalization:** Learned to normalize sentiment scores for visual gauge representation.

---

## ⚙️ How to Run Locally

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt

```

### 2️⃣ Launch the App

```bash
streamlit run app.py

```

---

## 💡 Practical Applications

* **Customer Service:** Analyze the tone of support calls to improve customer satisfaction.
* **Mental Health:** Tools for tracking emotional well-being through voice journals.
* **Media & PR:** Analyzing interview clips or podcasts for public sentiment.

---

## 📧 Contact

👩‍💻 **Arti Chaudhari** 🎓 BE Graduate '25 | Aspiring Data Analyst

📩 Email: [chaudhariarti2146@gmail.com](mailto:chaudhariarti2146@gmail.com)

🌐 GitHub: [github.com/artichaudhari](https://github.com/artichaudhari)

💼 LinkedIn: https://www.linkedin.com/in/arti-chaudhari-b998a82a9/

---

⭐ **If you found this project insightful, don’t forget to star the repo!**




