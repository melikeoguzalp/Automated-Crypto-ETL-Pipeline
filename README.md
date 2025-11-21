# Automated-Crypto-ETL-Pipeline
Python, SQL ve Task Scheduler kullanarak canlı veri işleyen otomatik sistem.
# 🚀 Automated Crypto ETL Pipeline

Bu proje, **CoinGecko API**'sinden canlı Bitcoin, Ethereum ve Solana verilerini çeken, **PostgreSQL** veritabanına kaydeden ve **Windows Task Scheduler** ile 7/24 otomatik çalışan uçtan uca bir veri mühendisliği projesidir.


## 🛠️ Kullanılan Teknolojiler
* **Python:** Veri çekme (Requests) ve Veri İşleme (Pandas).
* **SQL (PostgreSQL):** Veri Ambarı ve Arşivleme.
* **Otomasyon:** Windows Görev Zamanlayıcı (Task Scheduler).
* **Analiz:** SQL Window Functions (LAG, AVG) ile trend analizi.
* **Görselleştirme:** Matplotlib ile canlı grafik.

## ⚙️ Nasıl Çalışır?
1.  Python scripti API'ye bağlanır ve anlık fiyat/hacim bilgisini çeker.
2.  Veri temizlenir ve PostgreSQL veritabanındaki `FactMarketHistory` tablosuna basılır.
3.  SQL Views, gelen veriyi bir önceki saatle karşılaştırıp "Yükseliş/Düşüş" analizi yapar.
4.  Bu işlem **her 5 dakikada bir** otomatik olarak tekrarlanır.

## 📊 Veritabanı Şeması
* **DimCoin:** Coin bilgilerini tutan boyut tablosu.
* **FactMarketHistory:** Canlı verilerin aktığı tarihçe tablosu.

---
*Geliştiren: Melike Oğuzalp
