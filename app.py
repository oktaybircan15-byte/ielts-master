import streamlit as st
import json
import random
import os
from gtts import gTTS
import io

# --- 1. AYARLAR ---
st.set_page_config(page_title="IELTS Master", page_icon="🎓", layout="centered")

# --- 2. VERİ YÜKLEME ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ielts_words.json")
    
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# --- 3. SES MOTORU (Hatasız) ---
def get_audio_bytes(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        # Ses hatası olsa bile programı durdurma, None döndür
        print(f"Ses Hatası: {e}")
        return None

# --- 4. ANA PROGRAM ---
def main():
    st.title("🎓 IELTS Master")
    
    data = load_data()

    # Dosya Kontrolü
    if not data:
        st.error("⚠️ HATA: 'ielts_words.json' dosyası bulunamadı!")
        st.info("Lütfen GitHub sayfana gidip bu dosyanın yüklü olduğundan emin ol.")
        return

    # Oturum Yönetimi
    if 'word' not in st.session_state:
        st.session_state.word = random.choice(data)
        st.session_state.show_meaning = False
        # Sesi burada oluşturmuyoruz, aşağıda anlık oluşturacağız

    word = st.session_state.word

    # --- A. KELİME KARTI ---
    st.markdown(
        f"""
        <div style="background-color:#2e86c1; padding:20px; border-radius:10px; text-align:center; color:white; margin-bottom:20px;">
            <h1 style='margin:0; color:white;'>{word['word'].upper()}</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # --- B. SES (iPhone Uyumlu) ---
    # Sesi anlık oluşturuyoruz (Hata olsa bile devam eder)
    audio_bytes = get_audio_bytes(word['word'])
    
    if audio_bytes:
        # Key parametresi, sesin her kelimede yenilenmesini sağlar
        st.audio(audio_bytes, format='audio/mpeg', start_time=0, key=f"audio_{word['word']}")
    else:
        st.warning("Ses oluşturulamadı (İnternet bağlantısı veya sunucu yoğunluğu).")

    # --- C. BUTONLAR VE ANLAM ---
    # Burası "Sadece kelime var" sorununu çözer. Butonlar artık ses bloğundan bağımsız.
    
    col1, col2 = st.columns(2)

    if not st.session_state.show_meaning:
        if col1.button("🔍 ANLAMI GÖSTER", use_container_width=True):
            st.session_state.show_meaning = True
            st.rerun()
    else:
        # Tanımlar
        st.success(f"🇬🇧 {word.get('eng_def', '...')}")
        st.info(f"🇹🇷 {word.get('tr_def', '...')}")
        
        # Örnekler
        if word.get('sentences'):
            st.markdown("#### 📝 Örnekler")
            for ex in word['sentences']:
                st.write(f"• {ex}")

        st.markdown("---")
        # Sıradaki Butonu
        if st.button("➡️ SIRADAKİ KELİME", use_container_width=True):
            st.session_state.word = random.choice(data)
            st.session_state.show_meaning = False
            st.rerun()

if __name__ == "__main__":
    main()
