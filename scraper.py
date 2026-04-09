import requests
import json
import time
import pandas as pd # Tambahan buat nyimpen data ke CSV

API_KEY = 'AIzaSyDXjTxREsFVzwjki2Q-Gt5SG3YxOuqUAp0'

# Sample 5 kecamatan dari total 44 kecamatan di Jakarta
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

def scrape_toko_bangunan(kecamatan):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"toko bangunan in {kecamatan}"
    
    params = {
        'query': query,
        'key': API_KEY
    }
    
    response = requests.get(endpoint_url, params=params)
    results = json.loads(response.content)
    
    toko_list = []
    
    # Ambil maksimal 8 toko teratas
    for place in results.get('results', [])[:8]:
        toko_list.append({
            'Kecamatan': kecamatan, # Kita catet juga kecamatannya biar gampang difilter nanti
            'Nama Toko': place.get('name'),
            'Alamat': place.get('formatted_address'),
            'Rating': place.get('rating', 0)
        })
        
    return toko_list

# Siapkan list kosong untuk nampung SEMUA data
semua_data = []

# Looping ke setiap kecamatan
print("Mulai proses scraping...")
for kec in kecamatan_list:
    print(f"Mengambil data di: {kec}")
    data_per_kecamatan = scrape_toko_bangunan(kec)
    semua_data.extend(data_per_kecamatan) # Gabungin datanya
    
    # NAH DI SINI POSISI time.sleep NYA BRO!
    # Berhenti 2 detik sebelum lanjut ke kecamatan berikutnya biar aman dari blokir Google
    time.sleep(2) 

# --- FORMAT DATANYA ---
# Kita ubah data list tadi jadi DataFrame (Tabel) pakai Pandas
df = pd.DataFrame(semua_data)

# Simpan jadi file CSV
df.to_csv('data_toko_bangunan_jkt.csv', index=False)
print("Scraping Selesai! Data berhasil disimpan di data_toko_bangunan_jkt.csv")