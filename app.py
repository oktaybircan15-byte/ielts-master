import streamlit as st
import json
import random
import os
import io

# --- KÜTÜPHANE KONTROLÜ ---
try:
    from gtts import gTTS
except ImportError:
    st.error("⚠️ HATA: 'requirements.txt' dosyası eksik veya hatalı.")
    st.stop()

st.set_page_config(page_title="IELTS Master", page_icon="🎓", layout="centered")

# --- AKILLI DOSYA BULUCU (Senin durumun için özel) ---
def find_data_file(filename="ielts_words.json"):
    # 1. Olduğu yere bak
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Bütün alt klasörleri tara (VOC, Data, vs. ne varsa)
    for root, dirs, files in os.walk(current_dir):
        # Büyük/Küçük harf duyarlılığını kaldırmak için hepsini küçük harfe çevirip ara
        for file in files:
            if file.lower() == filename.lower():
                return os.path.join(root, file)
            
    return None

# --- VERİ YÜKLEME ---
@st.cache_data
def load_data():
    file_path = find_data_file("ielts_words.json")
    
    if not file_path:
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

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
    
    data = load_data()
    
    # --- EĞER DOSYA HALA BULUNAMAZSA ---
    if not data:
        st.error("⚠️ DOSYA BULUNAMADI!")
        st.warning("Kod bütün klasörleri aradı ama 'ielts_words.json' dosyasını bulamadı.")
        
        # Hata ayıklama: Hangi klasörleri gördüğünü yazdıralım
        st.write("👀 Kodun taradığı klasörler:")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_list = []
        for root, dirs, files in os.walk(current_dir):
            folder_name = os.path.basename(root)
            if folder_name: folder_list.append(f"📁 {folder_name}")
            for f in files:
                folder_list.append(f"  └─ 📄 {f}")
        st.code("\n".join(folder_list))
        return

    # --- UYGULAMA ---
    if 'word' not in st.session_state:
        st.session_state.word = random.choice(data)
        st.session_state.show_meaning = False
        st.session_state.audio_data = None

    word = st.session_state.word

    # Kelime Kartı
    st.markdown(
        f"""
        <div style="background-color:#2e86c1; padding:20px; border-radius:15px; text-align:center; color:white; margin-bottom:20px;">
            <h1 style='margin:0; font-size: 32px;'>{word['word'].upper()}</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Ses
    if st.session_state.audio_data is None:
        st.session_state.audio_data = get_audio_bytes(word['word'])
    
    if st.session_state.audio_data:
        st.audio(st.session_state.audio_data, format='audio/mpeg', start_time=0, key=f"audio_{word['word']}")

    # Butonlar
    col1, col2 = st.columns(2)

    if not st.session_state.show_meaning:
        if col1.button("🔍 ANLAMI GÖSTER", use_container_width=True):
            st.session_state.show_meaning = True
            st.rerun()
    else:
        st.success(f"🇬🇧 {word.get('eng_def', '-')}")
        st.info(f"🇹🇷 {word.get('tr_def', '-')}")
        
        if st.button("➡️ SIRADAKİ KELİME", use_container_width=True):
            st.session_state.word = random.choice(data)
            st.session_state.show_meaning = False
            st.session_state.audio_data = None
            st.rerun()

if __name__ == "__main__":
    main()
