import streamlit as st
import json
import random
import os
from gtts import gTTS
import io

# --- 1. AYARLAR ---
st.set_page_config(page_title="IELTS Master", page_icon="🎓", layout="centered")

# --- 2. VERİ YÜKLEME (En Garanti Yöntem) ---
@st.cache_data
def load_data():
    # Kodun olduğu klasörü bul
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ielts_words.json")
    
    # Dosya yoksa boş liste dön (Hata verme)
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# --- 3. SES MOTORU (Hafızadan Çalan Versiyon) ---
def get_audio(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except:
        return None

# --- 4. ANA PROGRAM ---
def main():
    st.title("🎓 IELTS Master")
    
    data = load_data()

    # Eğer veri yüklenemediyse Ekrana Basit Bir Uyarı Yaz
    if not data or len(data) == 0:
        st.error("⚠️ Veri dosyası bulunamadı!")
        st.warning("GitHub'a 'ielts_words.json' dosyasını yüklediğinden emin ol.")
        return

    # Oturum Yönetimi (Hafıza)
    if 'word' not in st.session_state:
        st.session_state.word = random.choice(data)
        st.session_state.show_meaning = False

    word = st.session_state.word

    # --- EKRAN ---
    # Kelime
    st.markdown(f"<h1 style='text-align: center; color: #2e86c1;'>{word['word'].upper()}</h1>", unsafe_allow_html=True)

    # Ses (iPhone için özel 'key' ayarı ile)
    audio_bytes = get_audio(word["word"])
    if audio_bytes:
        # 'key' parametresi sayesinde her kelimede oynatıcı sıfırlanır
        st.audio(audio_bytes, format='audio/mpeg', start_time=0, key=f"audio_{word['word']}")

    # Butonlar
    col1, col2 = st.columns(2)
    
    if not st.session_state.show_meaning:
        if col1.button("🔍 ANLAMI GÖSTER"):
            st.session_state.show_meaning = True
            st.rerun()
    else:
        st.success(f"🇬🇧 {word['eng_def']}")
        st.info(f"🇹🇷 {word['tr_def']}")
        
        if word.get('related'):
            st.caption(f"🔗 Türevler: {', '.join(word['related'])}")

        st.markdown("---")
        if st.button("➡️ SIRADAKİ"):
            st.session_state.word = random.choice(data)
            st.session_state.show_meaning = False
            st.rerun()

if __name__ == "__main__":
    main()
