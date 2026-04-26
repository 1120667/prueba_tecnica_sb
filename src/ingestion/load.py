from sqlalchemy import text


def load_stock_prices(df, engine):
    query = text("""
        INSERT INTO raw.stock_prices (
            ticker, date, open, high, low, close, volume,
            fecha_carga_utc, fuente, batch_id
        )
        VALUES (
            :ticker, :date, :open, :high, :low, :close, :volume,
            :fecha_carga_utc, :fuente, :batch_id
        )
        ON CONFLICT (ticker, date) DO NOTHING;
    """)

    with engine.begin() as conn:
        conn.execute(query, df.to_dict(orient="records"))


def load_company_profile(data, engine):
    query = text("""
        INSERT INTO raw.company_profile (
            ticker, industry, sector, employees, city, state,
            country, website, address, phone,
            fecha_carga_utc, fuente, batch_id
        )
        VALUES (
            :ticker, :industry, :sector, :employees, :city, :state,
            :country, :website, :address, :phone,
            :fecha_carga_utc, :fuente, :batch_id
        )
        ON CONFLICT (ticker) DO NOTHING;
    """)

    with engine.begin() as conn:
        conn.execute(query, data)


def load_fundamentals(data, engine):
    query = text("""
        INSERT INTO raw.fundamentals (
            ticker, date, total_assets, total_debt,
            invested_capital, shares_issued,
            fecha_carga_utc, fuente, batch_id
        )
        VALUES (
            :ticker, :date, :total_assets, :total_debt,
            :invested_capital, :shares_issued,
            :fecha_carga_utc, :fuente, :batch_id
        )
        ON CONFLICT (ticker, date) DO NOTHING;
    """)

    with engine.begin() as conn:
        conn.execute(query, data)


def load_holders(df, engine):
    query = text("""
        INSERT INTO raw.holders (
            ticker, date, holder, shares, value,
            fecha_carga_utc, fuente, batch_id
        )
        VALUES (
            :ticker, :date, :holder, :shares, :value,
            :fecha_carga_utc, :fuente, :batch_id
        )
        ON CONFLICT (ticker, date, holder) DO NOTHING;
    """)

    records = df.to_dict(orient="records")

    if records:
        with engine.begin() as conn:
            conn.execute(query, records)


def load_ratings(df, engine):
    query = text("""
        INSERT INTO raw.ratings (
            ticker, date, to_grade, from_grade, action,
            fecha_carga_utc, fuente, batch_id
        )
        VALUES (
            :ticker, :date, :to_grade, :from_grade, :action,
            :fecha_carga_utc, :fuente, :batch_id
        )
        ON CONFLICT (ticker, date, action) DO NOTHING;
    """)

    records = df.to_dict(orient="records")

    if records:
        with engine.begin() as conn:
            conn.execute(query, records)