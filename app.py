import streamlit as st
import json
import random
import os
import io

# Kütüphane kontrolü (Hata vermemesi için)
try:
    from gtts import gTTS
except ImportError:
    st.error("⚠️ HATA: 'requirements.txt' eksik. Lütfen 'gTTS' ekleyin.")
    st.stop()

st.set_page_config(page_title="IELTS Master", page_icon="🎓", layout="centered")

# --- VERİ YÜKLEME ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ielts_words.json")
    
    if not os.path.exists(file_path):
        return None  # Dosya yok
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data: return None # Dosya boş
            return data
    except:
        return None # Dosya bozuk

# --- SES MOTORU ---
def get_audio_bytes(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except:
        return None

# --- ANA PROGRAM ---
def main():
    st.title("🎓 IELTS Master")
    
    # Veriyi Yükle
    data = load_data()
    
    # --- KRİTİK KONTROL ---
    if data is None:
        st.error("⚠️ Veri Dosyası Bulunamadı!")
        st.warning("""
        **Sorun:** 'ielts_words.json' dosyası GitHub'da yok veya içi boş.
        
        **Çözüm:**
        1. GitHub sayfana git (ielts-master).
        2. 'Add file' -> 'Upload files' butonuna bas.
        3. Bilgisayarındaki 'ielts_words.json' dosyasını yükle.
        4. Sonra sayfayı yenile.
        """)
        return # Programı durdur

    # Oturum Yönetimi
    if 'word' not in st.session_state:
        st.session_state.word = random.choice(data)
        st.session_state.show_meaning = False
        st.session_state.audio_data = None

    word = st.session_state.word

    # --- KELİME KARTI ---
    st.markdown(
        f"""
        <div style="background-color:#2e86c1; padding:20px; border-radius:15px; text-align:center; color:white; margin-bottom:20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style='margin:0; font-size: 36px;'>{word['word'].upper()}</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # --- SES (iPhone Uyumlu) ---
    # Sesi anlık oluşturuyoruz
    if st.session_state.audio_data is None:
         st.session_state.audio_data = get_audio_bytes(word['word'])
    
    if st.session_state.audio_data:
        # Key: Sesin her kelimede yenilenmesini sağlar
        st.audio(st.session_state.audio_data, format='audio/mpeg', start_time=0, key=f"audio_{word['word']}")

    # --- BUTONLAR ---
    col1, col2 = st.columns(2)

    if not st.session_state.show_meaning:
        if col1.button("🔍 ANLAMI GÖSTER", use_container_width=True):
            st.session_state.show_meaning = True
            st.rerun()
    else:
        st.success(f"🇬🇧 {word.get('eng_def', '...')}")
        st.info(f"🇹🇷 {word.get('tr_def', '...')}")
        
        if word.get('sentences'):
            st.markdown("#### 📝 Örnekler")
            for ex in word['sentences']:
                st.write(f"• {ex}")

        st.markdown("---")
        if st.button("➡️ SIRADAKİ KELİME", use_container_width=True):
            st.session_state.word = random.choice(data)
            st.session_state.show_meaning = False
            st.session_state.audio_data = None
            st.rerun()

if __name__ == "__main__":
    main()
