-- 1. TEMİZLİK: Önce eski/hatalı tabloları silelim (Hata vermemesi için IF EXISTS kullanıyoruz)
DROP TABLE IF EXISTS FactMarketHistory;
DROP TABLE IF EXISTS DimCoin;

-- 2. BOYUT TABLOSU: Coinlerin listesini tutacak
CREATE TABLE DimCoin (
    CoinID INT PRIMARY KEY,
    Symbol VARCHAR(10),
    CoinName VARCHAR(50)
);

-- 3. KRİTİK ADIM: Coinleri içeriye GÖMMEMİZ lazım.
-- (İlk hatayı almanın sebebi bu adımın eksik olmasıydı)
INSERT INTO DimCoin (CoinID, Symbol, CoinName) VALUES 
(1, 'BTC', 'Bitcoin'),
(2, 'ETH', 'Ethereum'),
(3, 'SOL', 'Solana');

-- 4. OLAY TABLOSU: Fiyatların akacağı yer
CREATE TABLE FactMarketHistory (
    HistoryID SERIAL PRIMARY KEY,
    CoinID INT,
    Fiyat NUMERIC(18, 2),
    Hacim NUMERIC(24, 2),
    TarihSaat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CoinID) REFERENCES DimCoin(CoinID)
);

-- 5. KONTROL: Bakalım Coinler eklenmiş mi?
SELECT * FROM DimCoin;



















