
-- Création de la table users
CREATE TABLE users (
    id_users INTEGER NOT NULL,
    username VARCHAR(50),
    email VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (id_users)
);

-- Création de la table crypto_characteristics
CREATE TABLE crypto_characteristics (
    id_crypto_characteristics INTEGER NOT NULL,
    name VARCHAR(50),
    symbol VARCHAR(16),
    market_cap BIGINT,
    circulating_supply BIGINT,
    max_supply BIGINT,
    PRIMARY KEY (id_crypto_characteristics)
);

-- Création de la table intervals
CREATE TABLE intervals (
    id_interval INTEGER NOT NULL,
    intervals VARCHAR(4),
    PRIMARY KEY (id_interval)
);

-- Création de la table user_historical_data
CREATE TABLE user_historical_data (
    id_user_historical_data INTEGER NOT NULL,
    id_users INTEGER,
    id_crypto_characteristics INTEGER,
    id_interval INTEGER,
    PRIMARY KEY (id_user_historical_data),
    CONSTRAINT fk_users FOREIGN KEY (id_users) REFERENCES users (id_users),
    CONSTRAINT fk_crypto_characteristics1 FOREIGN KEY (id_crypto_characteristics) REFERENCES crypto_characteristics (id_crypto_characteristics),
    CONSTRAINT fk_interval1 FOREIGN KEY (id_interval) REFERENCES intervals (id_interval)
);

-- Création de la table historical_crypto_data
CREATE TABLE historical_crypto_data (
    id_historical_crypto_data INTEGER NOT NULL,
    id_crypto_characteristics INTEGER,
    id_interval INTEGER,
    open_time BIGINT,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    volume FLOAT,
    close_time BIGINT,
    quote_asset_volume FLOAT,
    number_of_trades FLOAT,
    taker_buy_base_asset_volume FLOAT,
    taker_buy_quote_asset_volume FLOAT,
    PRIMARY KEY (id_historical_crypto_data),
    CONSTRAINT fk_crypto_characteristics2 FOREIGN KEY (id_crypto_characteristics) REFERENCES crypto_characteristics (id_crypto_characteristics),
    CONSTRAINT fk_interval2 FOREIGN KEY (id_interval) REFERENCES intervals (id_interval)
);

-- Création de la table stream_crypto_data
CREATE TABLE stream_crypto_data (
    id_stream_crypto_data INTEGER NOT NULL,
    id_crypto_characteristics INTEGER,
    event_time BIGINT,
    first_trade_id BIGINT,
    last_trade_id BIGINT,
    open_time BIGINT,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    close_time BIGINT,
    base_asset_volume FLOAT,
    number_of_trades FLOAT,
    is_this_kline_closed BOOLEAN,
    PRIMARY KEY (id_stream_crypto_data),
    CONSTRAINT fk_crypto_characteristics3 FOREIGN KEY (id_crypto_characteristics) REFERENCES crypto_characteristics (id_crypto_characteristics)
);
