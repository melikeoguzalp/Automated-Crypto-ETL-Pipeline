import requests
import psycopg2
import json

# Hangi API ID'si veritabanında hangi CoinID'ye denk geliyor?
COIN_MAPPING = {
    'bitcoin': 1,
    'ethereum': 2,
    'solana': 3
}

# --- ADIM 1: API'den Veriyi Çek (EXTRACT) ---
def veriyi_getir():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_vol=true"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("✅ Veriler API'den başarıyla çekildi.")
            return data
        else:
            print(f"❌ API Hatası: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Bağlantı Sorunu: {e}")
        return None

# --- ADIM 2: PostgreSQL'e Kaydet (LOAD) ---
def veritabanina_yaz(data):
    if data is None:
        return

    conn = None
    try:
        # --- BAĞLANTI BİLGİLERİNİ KONTROL ET ---
        conn = psycopg2.connect(
            host="localhost",
            database="bitcoin",  # DBeaver'da sol tarafta yazan veritabanı adı (genelde postgres'tir)
            user="postgres",      # DBeaver kullanıcı adın
            password="YOUR_PASSWORD_HERE"   # DBeaver şifren (Burası senin şifrenle değişmeli!)
        )
        cursor = conn.cursor()
        
        # SQL Sorgusu (TarihSaat'i PostgreSQL otomatik ekleyecek)
        insert_query = """
            INSERT INTO FactMarketHistory (CoinID, Fiyat, Hacim) 
            VALUES (%s, %s, %s)
        """

        for api_name, detaylar in data.items():
            if api_name in COIN_MAPPING:
                coin_id = COIN_MAPPING[api_name]
                fiyat = detaylar['usd']
                hacim = detaylar['usd_24h_vol']
                
                # Veriyi demet (tuple) haline getir
                veri = (coin_id, fiyat, hacim)
                
                # Veritabanına emri gönder
                cursor.execute(insert_query, veri)
                print(f"📥 {api_name.upper()} eklendi -> Fiyat: ${fiyat}")

        conn.commit() # Değişiklikleri kalıcı yap (Save butonu gibi)
        print("\n✅ --- BÜTÜN İŞLEMLER BAŞARIYLA TAMAMLANDI ---")
        
    except Exception as e:
        print(f"❌ Veritabanı Hatası: {e}")
        print("İpucu: Şifrenin veya veritabanı adının doğru olduğundan emin ol.")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Script çalıştığında burası başlar
if __name__ == "__main__":
    print("--- Kripto ETL Başlıyor ---")
    gelen_veri = veriyi_getir()
    veritabanina_yaz(gelen_veri)