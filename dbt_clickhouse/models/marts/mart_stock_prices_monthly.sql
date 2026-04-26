SELECT
    ticker,
    toStartOfMonth(date) AS month,
    avg(open) AS avg_open_price,
    avg(close) AS avg_close_price,
    avg(volume) AS avg_volume,
    count(*) AS trading_days
FROM {{ ref('stg_stock_prices') }}
GROUP BY
    ticker,
    month