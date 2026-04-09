import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Vendor Bangun Jakarta", layout="wide")
st.title("🏗️ Sebaran Vendor Konstruksi di Jakarta")
st.write("Visualisasi data vendor material hasil scraping dari Google Maps API.")

try:
    df = pd.read_excel('data_toko_bangunan_jkt.xlsx')
    
    if df.empty:
        st.warning("⚠️ File Excel-nya ada, tapi isinya kosong bro!")
    else:
        # --- VISUALISASI 1: METRIK CEPAT ---
        total_toko = len(df)
        total_kecamatan = df['Kecamatan'].nunique()
        total_kategori = df['Kategori'].nunique() # Tambahan metrik kategori
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Vendor Ditemukan", total_toko)
        col2.metric("Total Kecamatan Tercover", total_kecamatan)
        col3.metric("Kategori Vendor", total_kategori)
        
        st.markdown("---")
        
        # --- VISUALISASI 2: BAR CHART ---
        # Kita bagi dua kolom biar grafiknya sebelahan
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("📊 Jumlah Toko per Kecamatan")
            count_kecamatan = df['Kecamatan'].value_counts()
            st.bar_chart(count_kecamatan)
            
        with chart_col2:
            st.subheader("🛠️ Proporsi Kategori Toko")
            count_kategori = df['Kategori'].value_counts()
            st.bar_chart(count_kategori)
        
        st.markdown("---")
        
        # --- VISUALISASI 3: TABEL INTERAKTIF & FILTER ---
        st.subheader("📋 Detail Data Vendor")
        
        # Sekarang ada 3 Filter yang sejajar
        f_col1, f_col2, f_col3 = st.columns(3)
        
        with f_col1:
            pilih_kategori = st.selectbox("Pilih Kategori:", ["Semua"] + list(df['Kategori'].unique()))
            
        with f_col2:
            pilih_kecamatan = st.selectbox("Pilih Kecamatan:", ["Semua"] + list(df['Kecamatan'].unique()))
            
        with f_col3:
            search_query = st.text_input("🔍 Cari Nama, Alamat, atau Keyword:")
        
        # --- LOGIKA FILTERING ---
        filtered_df = df.copy()
        
        if pilih_kategori != "Semua":
            filtered_df = filtered_df[filtered_df['Kategori'] == pilih_kategori]
            
        if pilih_kecamatan != "Semua":
            filtered_df = filtered_df[filtered_df['Kecamatan'] == pilih_kecamatan]
            
        if search_query:
            mask = (
                filtered_df['Nama Toko'].str.contains(search_query, case=False, na=False) |
                filtered_df['Alamat'].str.contains(search_query, case=False, na=False) |
                filtered_df['Kecamatan'].str.contains(search_query, case=False, na=False) |
                filtered_df['Kategori'].str.contains(search_query, case=False, na=False)
            )
            filtered_df = filtered_df[mask]
        
        st.write(f"Menampilkan **{len(filtered_df)}** hasil:")
        st.dataframe(filtered_df, use_container_width=True)

except pd.errors.EmptyDataError:
    st.error("❌ File Excel kosong melompong!")
except FileNotFoundError:
    st.error("❌ File 'data_toko_bangunan_jkt.xlsx' belum ada. Run scraper.py dulu ya bro!")