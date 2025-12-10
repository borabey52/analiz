import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

st.set_page_config(page_title="Kağıt Oku", layout="wide")

# API Anahtarı Ayarı (Main'den veya Secrets'tan gelen)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ API Anahtarı bulunamadı! Lütfen Streamlit Secrets ayarını yapın.")
    st.stop()

# Hafıza Kontrolü
if 'sinif_verileri' not in st.session_state:
    st.session_state.sinif_verileri = []

st.title("📝 Kağıt Okuma Modülü")

# --- SOL MENÜ: AYARLAR ---
with st.sidebar:
    st.header("Ayarlar")
    ogretmen_notu = st.text_area("Öğretmen Notu / Cevap Anahtarı:", placeholder="Örn: 1-A, 2-C...")

# --- ANA EKRAN ---
giris_yontemi = st.radio("Yükleme Yöntemi:", ["📁 Dosya Yükle", "📷 Kamera"], horizontal=True)

image_data = None
if giris_yontemi == "📁 Dosya Yükle":
    uploaded = st.file_uploader("Kağıt Seç", type=["jpg", "png", "jpeg"])
    if uploaded:
        image_data = Image.open(uploaded)
else:
    camera = st.camera_input("Fotoğraf Çek")
    if camera:
        image_data = Image.open(camera)

if image_data:
    st.image(image_data, caption="Okunacak Kağıt", width=400)
    
    if st.button("✨ Kağıdı Oku ve Kaydet", type="primary"):
        with st.spinner("Yapay zeka kağıdı inceliyor..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                prompt = """
                Bu sınav kağıdını oku.
                1. Öğrenci Adı Soyadını bul.
                2. Puan tablosunu çıkar.
                3. Çıktıyı SADECE şu JSON formatında ver:
                {
                    "Ad Soyad": "Öğrenci İsmi",
                    "Numara": "123",
                    "Not": 85,
                    "Detaylar": {"Soru 1": 10, "Soru 2": 5}
                }
                """
                
                parts = [prompt, image_data]
                if ogretmen_notu:
                    parts.append(f"Cevap Anahtarı / Notlar: {ogretmen_notu}")

                response = model.generate_content(parts)
                
                # JSON Temizleme
                text = response.text.replace("```json", "").replace("```", "").strip()
                veri = json.loads(text)
                
                # --- VERİYİ HAFIZAYA EKLE ---
                st.session_state.sinif_verileri.append(veri)
                
                st.success(f"✅ {veri.get('Ad Soyad')} sisteme eklendi!")
                st.json(veri)
                
            except Exception as e:
                st.error(f"Hata oluştu: {e}")
