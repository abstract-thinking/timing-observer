CREATE TABLE IF NOT EXISTS indices(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS dates(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS quotes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    close FLOAT NOT NULL,
    rsl FLOAT,
    code_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    FOREIGN KEY (code_id) REFERENCES indices (id),
    FOREIGN KEY (date_id) REFERENCES dates (id)
    UNIQUE (code_id, date_id) ON CONFLICT IGNORE
);

CREATE TABLE indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE NOT NULL,
    interest_rate REAL,
    inflation_rate REAL,
    exchange_rate REAL

);


INSERT OR IGNORE INTO indices(code, description) VALUES('^GDAXI', 'DAX');
INSERT OR IGNORE INTO indices(code, description) VALUES('^MDAXI', 'MDAX');
INSERT OR IGNORE INTO indices(code, description) VALUES('^TECDAX', 'TecDAX');
INSERT OR IGNORE INTO indices(code, description) VALUES('^SDAXI', 'SDAX');
INSERT OR IGNORE INTO indices(code, description) VALUES('^STOXX50E', 'Euro Stoxx 50');
INSERT OR IGNORE INTO indices(code, description) VALUES('^GSPC', 'S&P 500');
INSERT OR IGNORE INTO indices(code, description) VALUES('^DJI', 'Dow Jones 30');
INSERT OR IGNORE INTO indices(code, description) VALUES('^IXIC', 'Nasdaq Compositive');
INSERT OR IGNORE INTO indices(code, description) VALUES('^N225', 'Nikkei 225');
-- INSERT OR IGNORE INTO indices(code, description) VALUES('^FTSE', 'FTSE 100');
INSERT OR IGNORE INTO indices(code, description) VALUES('^NYA', 'NYSE COMPOSITE (DJ)');
INSERT OR IGNORE INTO indices(code, description) VALUES('^FCHI', 'CAC 40');
INSERT OR IGNORE INTO indices(code, description) VALUES('IMOEX.ME', 'MOEX Russia Index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^RUT', 'Russell 2000');
INSERT OR IGNORE INTO indices(code, description) VALUES('^XAX', 'NYSE AMEX COMPOSITE INDEX');
INSERT OR IGNORE INTO indices(code, description) VALUES('^N100', 'EURONEXT 100');
INSERT OR IGNORE INTO indices(code, description) VALUES('^BFX', 'BEL 20');
INSERT OR IGNORE INTO indices(code, description) VALUES('^HSI', 'HANG SENG INDEX');
INSERT OR IGNORE INTO indices(code, description) VALUES('000001.SS', 'SSE Composite Index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^AXJO', 'S&P/ASX 200');
INSERT OR IGNORE INTO indices(code, description) VALUES('^AORD', 'ALL ORDINARIES');
INSERT OR IGNORE INTO indices(code, description) VALUES('^BSESN', 'S&P BSE SENSEX');
INSERT OR IGNORE INTO indices(code, description) VALUES('^JKSE', 'Jakarta Composite Index');
-- INSERT OR IGNORE INTO indices(code, description) VALUES('^KLSE', 'FTSE Bursa Malaysia KLCI');
INSERT OR IGNORE INTO indices(code, description) VALUES('^NZ50', 'S&P/NZX 50 INDEX GROSS');
INSERT OR IGNORE INTO indices(code, description) VALUES('^KS11', 'KOSPI Composite Index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^TWII', 'TSEC weighted index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^GSPTSE', 'S&P/TSX Composite index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^BVSP', 'IBOVESPA');
INSERT OR IGNORE INTO indices(code, description) VALUES('^MXX', 'IPC MEXICO');
INSERT OR IGNORE INTO indices(code, description) VALUES('^IPSA', 'IPSA SANTIAGO DE CHILE');
INSERT OR IGNORE INTO indices(code, description) VALUES('^MERV', 'MERVAL');
INSERT OR IGNORE INTO indices(code, description) VALUES('^TA125.TA', 'TA-125');
INSERT OR IGNORE INTO indices(code, description) VALUES('^CASE30', 'EGX 30 Price Return Index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^JN0U.JO', 'Top 40 USD Net TRI Index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^ATX', 'Austrian Traded Index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^SSMI', 'Swiss Market Index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^OSEAX', 'Oslo Bors All-share');
INSERT OR IGNORE INTO indices(code, description) VALUES('^OMX', 'OMX Stockholm 30 Index');
INSERT OR IGNORE INTO indices(code, description) VALUES('^OMXC20', 'OMX Copenhagen 20');
INSERT OR IGNORE INTO indices(code, description) VALUES('^IBEX', 'IBEX');
INSERT OR IGNORE INTO indices(code, description) VALUES('PSEI.PS', 'PSEi INDEX');
