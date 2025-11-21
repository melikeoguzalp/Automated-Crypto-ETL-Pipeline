import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.dates as mdates

# --- AYARLAR ---
VERITABANI_ADI = 'bitcoin'
KULLANICI_ADI = 'postgres'
SIFRE = 'sifre123'  # <-- ŞİFRENİ GİRMEYİ UNUTMA!

def cizgi_grafik_ciz():
    # 1. BAĞLANTI
    conn_str = f"postgresql+psycopg2://{KULLANICI_ADI}:{SIFRE}@localhost/{VERITABANI_ADI}"
    engine = create_engine(conn_str)

    # 2. VERİ ÇEKME
    # Tırnak kullanmıyoruz, PostgreSQL küçük harfe çevirip bulsun.
    sorgu = """
    SELECT 
        dc.CoinName, 
        fmh.TarihSaat, 
        fmh.Fiyat
    FROM FactMarketHistory fmh
    JOIN DimCoin dc ON fmh.CoinID = dc.CoinID
    ORDER BY fmh.TarihSaat ASC
    """
    
    print("📊 Veriler çekiliyor...")
    try:
        df = pd.read_sql(sorgu, engine)
        
        if df.empty:
            print("⚠️ Veri yok! Robot çalışmamış olabilir.")
            return

        # 3. GÖRSELLEŞTİRME (Line Plot - Çizgi Grafik)
        plt.figure(figsize=(12, 6))
        
        # Scatterplot yerine Lineplot kullanıyoruz 👇
        sns.lineplot(
            data=df, 
            x='tarihsaat', 
            y='fiyat', 
            hue='coinname',    # Her coine ayrı renk ver
            style='coinname',  # Çizgi stillerini de ayır (Opsiyonel)
            markers=True,      # Çizgi üzerine nokta koy (Veri anını gösterir)
            dashes=False,      # Çizgiler düz olsun (kesik kesik olmasın)
            linewidth=2.5,     # Çizgi kalınlığı
            marker='o',        # Nokta şekli yuvarlak olsun
            markersize=8       # Nokta büyüklüğü
        )

        # 4. SÜSLEMELER
        plt.title('Kripto Para Canlı Takip Grafiği (Trend) 📈', fontsize=16)
        plt.xlabel('Saat', fontsize=12)
        plt.ylabel('Fiyat ($) - Logaritmik', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend(title='Kripto Para')
        
        # Tarih formatı (Saat:Dakika)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
        
        # Logaritmik Ölçek (Bitcoin ve Solana'yı aynı anda görmek için)
        plt.yscale('log') 

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"❌ HATA: {e}")

if __name__ == "__main__":
    cizgi_grafik_ciz()