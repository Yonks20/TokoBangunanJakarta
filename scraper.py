import requests
import time
import pandas as pd

API_KEY = 'AIzaSyDXjTxREsFVzwjki2Q-Gt5SG3YxOuqUAp0'

kecamatan_list = [
    # --- Jakarta Pusat (8 Kecamatan) ---
    "Cempaka Putih, Jakarta Pusat",
    "Gambir, Jakarta Pusat",
    "Johar Baru, Jakarta Pusat",
    "Kemayoran, Jakarta Pusat",
    "Menteng, Jakarta Pusat",
    "Sawah Besar, Jakarta Pusat",
    "Senen, Jakarta Pusat",
    "Tanah Abang, Jakarta Pusat",

    # --- Jakarta Utara (6 Kecamatan) ---
    "Cilincing, Jakarta Utara",
    "Kelapa Gading, Jakarta Utara",
    "Koja, Jakarta Utara",
    "Pademangan, Jakarta Utara",
    "Penjaringan, Jakarta Utara",
    "Tanjung Priok, Jakarta Utara",

    # --- Jakarta Barat (8 Kecamatan) ---
    "Cengkareng, Jakarta Barat",
    "Grogol Petamburan, Jakarta Barat",
    "Kalideres, Jakarta Barat",
    "Kebon Jeruk, Jakarta Barat",
    "Kembangan, Jakarta Barat",
    "Palmerah, Jakarta Barat",
    "Taman Sari, Jakarta Barat",
    "Tambora, Jakarta Barat",

    # --- Jakarta Selatan (10 Kecamatan) ---
    "Cilandak, Jakarta Selatan",
    "Jagakarsa, Jakarta Selatan",
    "Kebayoran Baru, Jakarta Selatan",
    "Kebayoran Lama, Jakarta Selatan",
    "Mampang Prapatan, Jakarta Selatan",
    "Pancoran, Jakarta Selatan",
    "Pasar Minggu, Jakarta Selatan",
    "Pesanggrahan, Jakarta Selatan",
    "Setiabudi, Jakarta Selatan",
    "Tebet, Jakarta Selatan",

    # --- Jakarta Timur (10 Kecamatan) ---
    "Cakung, Jakarta Timur",
    "Cipayung, Jakarta Timur",
    "Ciracas, Jakarta Timur",
    "Duren Sawit, Jakarta Timur",
    "Jatinegara, Jakarta Timur",
    "Kramat Jati, Jakarta Timur",
    "Makasar, Jakarta Timur",
    "Matraman, Jakarta Timur",
    "Pasar Rebo, Jakarta Timur",
    "Pulo Gadung, Jakarta Timur",

    # --- Kepulauan Seribu (2 Kecamatan) ---
    "Kepulauan Seribu Selatan, Kepulauan Seribu",
    "Kepulauan Seribu Utara, Kepulauan Seribu"
]

# 2. List Kategori Toko yang lo mau
kategori_list = [
    "toko bangunan",
    "toko listrik",
    "toko kayu",
    "toko kaca",
    "toko besi",
    "toko alumunium"
]

def scrape_toko(kategori, kecamatan):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    # Querynya dinamis gabungin kategori dan kecamatan
    query = f"{kategori} in {kecamatan}"
    
    params = {
        'query': query,
        'key': API_KEY
    }
    
    response = requests.get(endpoint_url, params=params)
    results = response.json()
    
    status = results.get('status')
    # ZERO_RESULTS itu wajar kalau misal di kecamatan itu emang gak ada toko kacanya
    if status != 'OK' and status != 'ZERO_RESULTS': 
        print(f"⚠️ Error nyari {kategori} di {kecamatan}: {status}")
        return []
        
    toko_list = []
    
    for place in results.get('results', [])[:25]:
        toko_list.append({
            'Kategori': kategori.title(), # title() bikin huruf depannya kapital (Toko Listrik)
            'Kecamatan': kecamatan,
            'Nama Toko': place.get('name'),
            'Alamat': place.get('formatted_address'),
            'Rating': place.get('rating', 0)
        })
        
    return toko_list

semua_data = []

print("Mulai proses scraping multi-kategori...")

# Nested Looping (Looping di dalam Looping)
for kec in kecamatan_list:
    print(f"\n--- Mengambil data di: {kec} ---")
    
    for kat in kategori_list:
        print(f"🔍 Mencari {kat}...")
        data_toko = scrape_toko(kat, kec)
        semua_data.extend(data_toko)
        
        # Jeda waktu 2 detik per KATEGORI biar aman dari blokir Google
        time.sleep(2) 

if len(semua_data) > 0:
    df = pd.DataFrame(semua_data)
    df.to_excel('data_toko_bangunan_jkt.xlsx', index=False, engine='openpyxl')
    print("\n✅ Scraping Selesai! Data multi-kategori berhasil disimpan ke data_toko_bangunan_jkt.xlsx")
else:
    print("\n❌ Gagal nyimpen Excel. Datanya kosong bro!")