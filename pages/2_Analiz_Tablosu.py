import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analiz", layout="wide")
st.title("📊 Sınıf Analizi ve Tablo")

# Hafıza boş mu?
if 'sinif_verileri' not in st.session_state or len(st.session_state.sinif_verileri) == 0:
    st.info("Henüz veri yok. Lütfen 'Kağıt Oku' sayfasından sınav okutun.")
    st.stop()

# --- VERİLERİ TABLOYA ÇEVİR ---
veriler = st.session_state.sinif_verileri

# Pandas DataFrame oluştur
df = pd.json_normalize(veriler)

# --- İSTATİSTİKLER ---
col1, col2, col3 = st.columns(3)
col1.metric("Öğrenci Sayısı", len(df))
if "Not" in df.columns:
    col2.metric("Sınıf Ortalaması", f"{df['Not'].mean():.1f}")
    col3.metric("En Yüksek Not", df['Not'].max())

st.markdown("---")

# --- TABLO GÖSTERİMİ ---
st.subheader("📋 Sınıf Listesi")
st.dataframe(df, use_container_width=True)

# --- EXCEL İNDİR ---
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8-sig')

csv = convert_df(df)
st.download_button("📥 Excel Olarak İndir", csv, "sinif_listesi.csv", "text/csv")
