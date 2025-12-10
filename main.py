import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# --- 1. AYARLAR VE GÜVENLİK ---
st.set_page_config(page_title="AI Sınav Okuma", layout="wide")

# API Anahtarını Streamlit'in güvenli kasasından (secrets) çekiyoruz
if "GOOGLE_API_KEY" in st.secrets:
    SABIT_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    # Eğer anahtar yoksa boş bırakalım, aşağıda uyarı veririz
    SABIT_API_KEY = ""

# Gemini'yi yapılandır (Eğer anahtar varsa)
if SABIT_API_KEY:
    genai.configure(api_key=SABIT_API_KEY)

st.set_page_config(page_title="Sınav Asistanı Ana Sayfa", layout="wide")

st.title("🏫 AI Sınav Okuma Sistemi")
st.info("Soldaki menüden işlem seçebilirsiniz.")

# --- TÜM SİSTEMİN HAFIZASI BURADA BAŞLAR ---
# Bu liste diğer sayfalarda da ortak kullanılacak.
if 'sinif_verileri' not in st.session_state:
    st.session_state.sinif_verileri = []

st.write(f"📂 Şu an hafızada **{len(st.session_state.sinif_verileri)}** adet okunmuş kağıt var.")

if len(st.session_state.sinif_verileri) > 0:
    if st.button("Tüm Hafızayı Temizle (Yeni Sınıf)"):
        st.session_state.sinif_verileri = []
        st.rerun()
