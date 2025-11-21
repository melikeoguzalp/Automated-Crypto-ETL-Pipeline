import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- AYARLAR ---
# DBeaver'da sol üstte veritabanı ismin 'postgres' ise burası 'postgres' kalmalı.
VERITABANI_ADI = 'bitcoin'  
KULLANICI_ADI = 'postgres'
SIFRE = 'your-password'           # <-- ŞİFRENİ BURAYA YAZ

def grafik_goster():
    # 1. BAĞLANTI
    conn_str = f"postgresql+psycopg2://{KULLANICI_ADI}:{SIFRE}@localhost/{VERITABANI_ADI}"
    
    try:
        engine = create_engine(conn_str)
        
        # 2. VERİYİ ÇEK (DÜZELTME: Tırnakları kaldırdık)
        # PostgreSQL tırnak olmayınca otomatik küçük harfe çevirir ve tabloyu bulur.
        sorgu = """
        SELECT TarihSaat, Fiyat 
        FROM FactMarketHistory 
        WHERE CoinID = 1 
        ORDER BY TarihSaat ASC
        """
        
        print("📊 Veri çekiliyor...")
        df = pd.read_sql(sorgu, engine)
        
        # Sütun isimlerini kontrol edelim (Ekrana basıyoruz)
        print("Gelen Sütunlar:", df.columns) 

        if df.empty:
            print("⚠️ Tablo bulundu ama içi boş! Robotun veri kaydettiğinden emin ol.")
            return

        # 3. GRAFİK ÇİZ (DÜZELTME: Sütun isimlerini küçük harf yaptık)
        # Çünkü PostgreSQL 'TarihSaat'i 'tarihsaat' olarak gönderir.
        plt.figure(figsize=(10, 5))
        
        # df['tarihsaat'] ve df['fiyat'] olarak değiştirdik 👇
        plt.plot(df['tarihsaat'], df['fiyat'], marker='o', linestyle='-', color='orange', label='Bitcoin (BTC)')
        
        plt.title('Canlı Bitcoin Fiyat Takibi 🚀')
        plt.xlabel('Saat')
        plt.ylabel('Fiyat ($)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        # Tarih formatı
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gcf().autofmt_xdate()
        
        plt.show()
        
    except Exception as e:
        print(f"❌ BİR HATA OLUŞTU: {e}")
        print("İpucu: Şifrenin doğru olduğundan emin ol.")

if __name__ == "__main__":
    grafik_goster()