CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.company_profile (
    ticker TEXT,
    industry TEXT,
    sector TEXT,
    employees BIGINT,
    city TEXT,
    state TEXT,
    country TEXT,
    website TEXT,
    address TEXT,
    phone TEXT,
    fecha_carga_utc TIMESTAMP,
    fuente TEXT,
    batch_id TEXT,

    CONSTRAINT unique_company_profile_ticker UNIQUE (ticker)
);

CREATE TABLE IF NOT EXISTS raw.stock_prices (
    ticker TEXT,
    date DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    fecha_carga_utc TIMESTAMP,
    fuente TEXT,
    batch_id TEXT,

    CONSTRAINT unique_stock_prices_ticker_date UNIQUE (ticker, date)
);

CREATE TABLE IF NOT EXISTS raw.fundamentals (
    ticker TEXT,
    date DATE,
    total_assets NUMERIC,
    total_debt NUMERIC,
    invested_capital NUMERIC,
    shares_issued NUMERIC,
    fecha_carga_utc TIMESTAMP,
    fuente TEXT,
    batch_id TEXT,

    CONSTRAINT unique_fundamentals_ticker_date UNIQUE (ticker, date)
);

CREATE TABLE IF NOT EXISTS raw.holders (
    ticker TEXT,
    date DATE,
    holder TEXT,
    shares NUMERIC,
    value NUMERIC,
    fecha_carga_utc TIMESTAMP,
    fuente TEXT,
    batch_id TEXT,

    CONSTRAINT unique_holders_ticker_date_holder UNIQUE (ticker, date, holder)
);

CREATE TABLE IF NOT EXISTS raw.ratings (
    ticker TEXT,
    date DATE,
    to_grade TEXT,
    from_grade TEXT,
    action TEXT,
    fecha_carga_utc TIMESTAMP,
    fuente TEXT,
    batch_id TEXT,

    CONSTRAINT unique_ratings_ticker_date_action UNIQUE (ticker, date, action)
);