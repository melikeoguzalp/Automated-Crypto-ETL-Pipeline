-- Eğer eskisi varsa sil (Temiz iş)
DROP VIEW IF EXISTS vw_KriptoAnaliz;

-- Görünüm (View) Oluştur
CREATE VIEW vw_KriptoAnaliz AS
SELECT 
    dc.CoinName,
    fmh.TarihSaat,
    fmh.Fiyat AS GuncelFiyat,
    
    -- ANALİZ 1: Bir önceki satırdaki fiyatı getir (LAG Fonksiyonu)
    LAG(fmh.Fiyat, 1) OVER(PARTITION BY dc.CoinName ORDER BY fmh.TarihSaat) AS OncekiFiyat,
    
    -- ANALİZ 2: Değişimi Hesapla (Güncel - Önceki)
    fmh.Fiyat - LAG(fmh.Fiyat, 1) OVER(PARTITION BY dc.CoinName ORDER BY fmh.TarihSaat) AS DegisimMiktari,

    -- ANALİZ 3: Yön Belirle (CASE WHEN ile makyaj)
    CASE 
        WHEN fmh.Fiyat > LAG(fmh.Fiyat, 1) OVER(PARTITION BY dc.CoinName ORDER BY fmh.TarihSaat) THEN '⬆️ Yükseliş'
        WHEN fmh.Fiyat < LAG(fmh.Fiyat, 1) OVER(PARTITION BY dc.CoinName ORDER BY fmh.TarihSaat) THEN '⬇️ Düşüş'
        ELSE '➖ Sabit' 
    END AS Yon

FROM FactMarketHistory fmh
INNER JOIN DimCoin dc ON fmh.CoinID = dc.CoinID;

SELECT * FROM vw_KriptoAnaliz 
ORDER BY TarihSaat DESC;