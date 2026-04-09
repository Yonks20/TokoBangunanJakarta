import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Toko Bangunan", layout="wide")
st.title("🏗️ Sebaran Toko Bangunan di Jakarta")
st.write("Visualisasi data toko bangunan hasil scraping dari Google Maps API.")

try:
    df = pd.read_csv('data_toko_bangunan_jkt.csv')
    
    # Cek apakah dataframe-nya ada isinya atau cuma header doang
    if df.empty:
        st.warning("⚠️ File CSV-nya ada, tapi isinya kosong bro! Cek terminal pas running scraper-nya, biasanya ada error dari Google API.")
    else:
        total_toko = len(df)
        total_kecamatan = df['Kecamatan'].nunique()
        
        col1, col2 = st.columns(2)
        col1.metric("Total Toko Ditemukan", total_toko)
        col2.metric("Total Kecamatan Tercover", total_kecamatan)
        
        st.markdown("---")
        st.subheader("📊 Jumlah Toko per Kecamatan")
        count_toko = df['Kecamatan'].value_counts()
        st.bar_chart(count_toko)
        
        st.subheader("📋 Detail Data Toko")
        pilih_kecamatan = st.selectbox("Pilih Kecamatan untuk difilter:", ["Semua"] + list(df['Kecamatan'].unique()))
        
        if pilih_kecamatan == "Semua":
            st.dataframe(df, use_container_width=True)
        else:
            filtered_df = df[df['Kecamatan'] == pilih_kecamatan]
            st.dataframe(filtered_df, use_container_width=True)

# Sabuk pengaman buat error yang tadi!
except pd.errors.EmptyDataError:
    st.error("❌ File CSV kosong melompong! Script scraping-nya gagal dapet data dari Google. Cek API Key lo ya!")
except FileNotFoundError:
    st.error("❌ File 'data_toko_bangunan_jkt.csv' belum ada. Run scraper.py dulu ya bro!")