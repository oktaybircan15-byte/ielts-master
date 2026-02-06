
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
    # Senin özel klasörün
    user_path = r"C:\Users\oktay\OneDrive\Masaüstü\VOC"
    
    possible_paths = [
        "ielts_words.json",
        os.path.join(current_dir, "ielts_words.json"),
        os.path.join(user_path, "ielts_words.json")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data: return data
            except:
                continue
    return []

# --- SES FONKSİYONU (GARANTİ YÖNTEM: DİSKE KAYDETME) ---
def text_to_speech(text):
    filename = "gecici_ses.mp3"
    try:
        # 1. Sesi oluştur
        tts = gTTS(text=text, lang='en')
        
        # 2. Dosya olarak kaydet (iPhone bunu daha çok sever)
        tts.save(filename)
        
        # 3. Dosyayı binary (veri) olarak oku
        with open(filename, "rb") as f:
            audio_bytes = f.read()
            
        return audio_bytes
    except Exception as e:
        st.error(f"Ses hatası: {e}")
        return None

# --- ANA UYGULAMA ---
def main():
    st.title("🎓 IELTS Master")
    st.caption("🚀 Senin Kişisel Kelime Koçun")
    
    data = load_data()

    if not data:
        st.error("⚠️ Veri dosyası (ielts_words.json) bulunamadı!")
        st.warning("Lütfen önce pdf_botu.py'yi çalıştır.")
        return

    # Oturum Yönetimi
    if 'current_word' not in st.session_state:
        st.session_state.current_word = random.choice(data)
        st.session_state.show_meaning = False
        st.session_state.audio_bytes = None

    word = st.session_state.current_word

    # --- KELİME KARTI ---
    st.markdown(f'<div class="kelime-kutusu">{word["word"].upper()}</div>', unsafe_allow_html=True)

    # Ses Oynatıcı
    if st.session_state.audio_bytes is None:
        with st.spinner('Ses hazırlanıyor...'):
            st.session_state.audio_bytes = text_to_speech(word["word"])
    
    if st.session_state.audio_bytes:
        # Formatı 'audio/mpeg' yaptık, iPhone standardı budur.
        st.audio(st.session_state.audio_bytes, format='audio/mpeg')
    else:
        st.warning("Ses yüklenemedi.")

    # --- BUTONLAR ---
    col1, col2 = st.columns([1, 1])

    if not st.session_state.show_meaning:
        with col1:
             if st.button("🔍 ANLAMI GÖSTER", type="primary"):
                st.session_state.show_meaning = True
                st.rerun()
    else:
        # Anlamlar
        st.success(f"🇬🇧 {word['eng_def']}")
        st.info(f"🇹🇷 {word['tr_def']}")

        # Türevler
        if word.get('related') and len(word['related']) > 0:
            st.markdown(f"""
            <div class="related-box">
                <b>🔗 Kelime Ailesi:</b> {', '.join(word['related'])}
            </div>
            """, unsafe_allow_html=True)

        # Örnekler
        if word.get('sentences'):
            st.markdown("#### 📝 Örnek Cümleler")
            for ex in word['sentences']:
                st.write(f"• {ex}")

        st.markdown("---")
        if st.button("➡️ SIRADAKİ KELİME"):
            st.session_state.current_word = random.choice(data)
            st.session_state.show_meaning = False
            st.session_state.audio_bytes = None
            st.rerun()

if __name__ == "__main__":
    main()
