SELECT
    ticker,
    toDate(date) AS date,
    toFloat64(open) AS open,
    toFloat64(high) AS high,
    toFloat64(low) AS low,
    toFloat64(close) AS close,
    toUInt64(volume) AS volume,
    fuente,
    batch_id,
    fecha_carga_utc
FROM raw.stock_prices