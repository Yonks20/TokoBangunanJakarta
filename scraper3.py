import requests
import time
import pandas as pd

API_KEY = 'MASUKKIN_API_KEY_LO_DISINI'

# Kita test 2 kecamatan dulu aja ya biar cepet ketahuan errornya
kecamatan_list = [
    "Kebayoran Baru, Jakarta Selatan",
    "Menteng, Jakarta Pusat"
]

def scrape_toko_bangunan(kecamatan):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"toko bangunan in {kecamatan}"
    
    params = {
        'query': query,
        'key': API_KEY
    }
    
    response = requests.get(endpoint_url, params=params)
    results = response.json() # Ambil response JSON
    
    # --- INI DETEKSI ERROR DARI GOOGLE ---
    status = results.get('status')
    if status != 'OK':
        print(f"⚠️ Waduh, error dari Google pas nyari di {kecamatan}: {status}")
        if 'error_message' in results:
            print(f"Pesan Error: {results['error_message']}")
        return []
    
    toko_list = []
    
    for place in results.get('results', [])[:8]:
        toko_list.append({
            'Kecamatan': kecamatan,
            'Nama Toko': place.get('name'),
            'Alamat': place.get('formatted_address'),
            'Rating': place.get('rating', 0)
        })
        
    return toko_list

semua_data = []

print("Mulai proses scraping...")
for kec in kecamatan_list:
    print(f"Mengambil data di: {kec}...")
    data_per_kecamatan = scrape_toko_bangunan(kec)
    semua_data.extend(data_per_kecamatan)
    time.sleep(2) 

if len(semua_data) > 0:
    df = pd.DataFrame(semua_data)
    df.to_csv('data_toko_bangunan_jkt.csv', index=False)
    print("✅ Scraping Selesai! Data berhasil disimpan di data_toko_bangunan_jkt.csv")
else:
    print("❌ Gagal nyimpen CSV. Datanya kosong bro, cek error dari Google di atas!")