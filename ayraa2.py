"""
Ayurveda Personal AI — Dr. Ayra (Cloud-Compatible Version, No Login Required)
-------------------------------------------------------------------------------
This version is fully compatible with GitHub deployment or any cloud service (Streamlit Cloud, Hugging Face Spaces, etc.).
It removes all admin or login requirements.
Supports default Ayurveda knowledge, multiple patients, and optional TTS audio.
"""

import os
import json
import tempfile
from typing import List, Optional

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ModuleNotFoundError:
    STREAMLIT_AVAILABLE = False

try:
    from gtts import gTTS
except Exception:
    gTTS = None

# Cloud-friendly storage using relative path
SESSIONS_DIR = 'sessions'
os.makedirs(SESSIONS_DIR, exist_ok=True)
PATIENTS_FILE = os.path.join(SESSIONS_DIR, 'patients.json')

# Default Ayurveda knowledge
DEFAULT_KNOWLEDGE = [
    "Amla is very good for digestion and immunity.",
    "Tulsi helps in relieving cold and cough.",
    "Ashwagandha reduces stress and improves energy.",
    "Triphala promotes healthy bowel movements and detoxification.",
    "Ginger helps in improving digestion and reducing nausea."
]

# Load / save JSON helper functions
def load_json(file_path, default=None):
    default = default or {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

patients = load_json(PATIENTS_FILE)

# Simple retriever class
class SimpleRetriever:
    def __init__(self, docs: Optional[List[str]] = None):
        self.docs = docs or DEFAULT_KNOWLEDGE
    def query(self, q: str) -> str:
        q_lower = (q or '').lower()
        for d in self.docs:
            if any(w in d.lower() for w in q_lower.split()):
                return f"👩‍⚕️ Main Dr. Ayra bol rahi hoon — {d}"
        return "👩‍⚕️ Main Dr. Ayra hoon — Mujhe is bare mein abhi info nahi mili, par main aapki help ke liye yahan hoon. 💚"

retriever = SimpleRetriever()

if STREAMLIT_AVAILABLE:
    # Streamlit UI
    st.set_page_config(page_title="Dr. Ayra", page_icon="🪷", layout="wide")
    st.title("🪷 Dr. Ayra — Ayurveda Doctor 👩‍⚕️")

    # Patient Profile Section (No login required)
    patient_id = st.text_input("Enter Patient ID")
    if patient_id:
        profile = patients.get(patient_id, {})
        name = st.text_input("Name", value=profile.get('name',''))
        age = st.text_input("Age", value=profile.get('age',''))
        lifestyle = st.text_area("Lifestyle / Habits", value=profile.get('lifestyle',''))
        if st.button("Save Profile"):
            patients[patient_id] = {'name': name, 'age': age, 'lifestyle': lifestyle}
            save_json(PATIENTS_FILE, patients)
            st.success("Profile saved ✅")

    # Chat Section
    query = st.text_input("Ask Dr. Ayra")
    if query:
        response = retriever.query(query)
        st.write(response)
        if gTTS:
            try:
                tts_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                gTTS(text=response, lang='hi').save(tts_file.name)
                st.audio(tts_file.name, format='audio/mp3')
            except Exception:
                st.warning("Audio playback not supported in this cloud environment.")

    # GitHub Deployment Note
    st.info("Push this repo to GitHub and deploy on Streamlit Cloud or compatible cloud service. Sessions folder and patients.json are created automatically.")
else:
    print("⚠️ Streamlit is not installed in this environment. Please install Streamlit or deploy on a cloud service that supports it.")
    print("You can still use the core functionality by running the code in a local Python environment with Streamlit installed.")
