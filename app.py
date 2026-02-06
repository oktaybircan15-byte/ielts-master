import streamlit as st
import json
import random
import os
from gtts import gTTS

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="IELTS Master",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS STİL ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .kelime-kutusu {
        background-color: #2e86c1;
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .related-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #2e86c1;
        margin-top: 15px;
        color: #2c3e50;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 55px;
        font-weight: bold;
        font-size: 18px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# --- VERİ YÜKLEME ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ielts_words.json")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data: return data
        except:
            return []
    return []

# --- SES FONKSİYONU (CLOUD UYUMLU) ---
def get_audio_bytes(text):
    try:
        # 1. Ses dosyasını oluştur
        tts = gTTS(text=text, lang='en')
        
        # 2. Geçici bir dosyaya kaydet (Cloud diskine)
        temp_file = "temp_audio.mp3"
        tts.save(temp_file)
        
        # 3. Dosyayı binary olarak geri oku
        with open(temp_file, "rb") as f:
            audio_bytes = f.read()
            
        return audio_bytes
    except Exception as e:
        st.error(f"Ses Hatası: {e}")
        return None

# --- ANA UYGULAMA ---
def main():
    st.title("🎓 IELTS Master")
    st.caption("🚀 Senin Kişisel Kelime Koçun")
    
    data = load_data()

    if not data:
        st.error("⚠️ Veri dosyası (ielts_words.json) bulunamadı!")
        st.info("Github'a dosyanın yüklendiğinden emin ol.")
        return

    # Oturum Yönetimi
    if 'current_word' not in st.session_state:
        st.session_state.current_word = random.choice(data)
        st.session_state.show_meaning = False
        # Sesi sıfırla
        st.session_state.audio_data = None 

    word = st.session_state.current_word

    # --- KELİME KARTI ---
    st.markdown(f'<div class="kelime-kutusu">{word["word"].upper()}</div>', unsafe_allow_html=True)

    # --- SES OYNATICI ---
    # Sesi sadece kelime değiştiğinde veya ilk açılışta oluştur
    if st.session_state.audio_data is None:
        with st.spinner('Ses oluşturuluyor...'):
            st.session_state.audio_data = get_audio_bytes(word["word"])
            
    if st.session_state.audio_data:
        # İŞTE KRİTİK NOKTA: format='audio/mpeg' (iPhone bunu sever)
