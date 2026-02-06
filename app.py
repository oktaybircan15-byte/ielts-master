import streamlit as st
import json
import random
import os
from gtts import gTTS
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="IELTS Master", page_icon="🎓", layout="centered")

# --- CSS STİL ---
st.markdown("""
    <style>
    .kelime-kutusu {
        background-color: #2e86c1;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stButton>button { width: 100%; height: 50px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- VERİ YÜKLEME ---
@st.cache_data
def load_data():
    # 1. Klasör yolunu bul
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ielts_words.json")
    
    # 2. Dosyayı kontrol et
    if not os.path.exists(file_path):
        return None, f"Dosya bulunamadı: {file_path}"
    
    # 3. Yükle
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data, "Başarılı"
    except Exception as e:
        return None, f"JSON Hatası: {str(e)}"

# --- SES OLUŞTURMA ---
def create_audio(text):
    try:
        tts = gTTS(text=text, lang='en')
        filename = f"audio_{random.randint(1000,9999)}.mp3"
        tts.save(filename)
        with open(filename, "rb") as f:
            audio_bytes = f.read()
        return audio_bytes
    except:
        return None

# --- ANA PROGRAM ---
def main():
    st.title("🎓 IELTS Master")
    
    # Veriyi Yükle
    data, message = load_data()
    
    # Hata Kontrolü
    if data is None:
        st.error(f"⚠️ HATA: {message}")
        st.info("Lütfen GitHub'a 'ielts_words.json' dosyasını yüklediğinden emin ol.")
        st.stop() # Programı burada durdur
        
    # Oturum Başlatma
    if 'word' not in st.session_state:
        st.session_state.word = random.choice(data)
        st.session_state.show_meaning = False
        st.session_state.audio_bytes = None
        st.session_state.counter = 0

    word = st.session_state.word

    # --- 1. KELİME KARTI ---
    st.markdown(f'<div class="kelime-kutusu">{word["word"].upper()}</div>', unsafe_allow_html=True)

    # --- 2. SES (Try-Except bloğu ile korumalı) ---
    try:
        if st.session_state.audio_bytes is None:
            st.session_state.audio_bytes = create_audio(word["word"])
        
        if st.session_state.audio_bytes:
            # UNIQUE KEY: Her seferinde benzersiz bir kimlik veriyoruz
            st.audio(
                st.session_state.audio_bytes, 
                format='audio/mpeg', 
                start_time=0, 
                key=f"audio_player_{st.session_state.counter}"
            )
    except Exception as e:
        st.warning(f"Ses çalınamadı: {e}")

    # --- 3. BUTONLAR ---
    col1, col2 = st.columns(2)
    
    if not st.session_state.show_meaning:
        if col1.button("🔍 ANLAMI GÖSTER"):
            st.session_state.show_meaning = True
            st.rerun()
    else:
        st.success(f"🇬🇧 {word['eng_def']}")
        st.info(f"🇹🇷 {word['tr_def']}")
        
        # Türevler
        if word.get('related'):
            st.write(f"🔗 **Türevler:** {', '.join(word['related'])}")

        st.markdown("---")
        if st.button("➡️ SIRADAKİ"):
            st.session_state.word = random.choice(data)
            st.session_state.show_meaning = False
            st.session_state.audio_bytes = None
            st.session_state.counter += 1 # Key'i değiştirmek için sayacı artır
            st.rerun()

    # Alt bilgi (Debug için)
    st.caption(f"Veritabanı: {len(data)} kelime yüklü.")

if __name__ == "__main__":
    main()
