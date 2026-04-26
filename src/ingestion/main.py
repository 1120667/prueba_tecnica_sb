from uuid import uuid4
from datetime import datetime

from config import engine

from extract import (
    get_stock_prices,
    get_company_profile,
    get_fundamentals,
    get_holders,
    get_ratings
)

from transform import (
    transform_prices,
    transform_company_profile,
    transform_fundamentals,
    transform_holders,
    transform_ratings
)

from load import (
    load_stock_prices,
    load_company_profile,
    load_fundamentals,
    load_holders,
    load_ratings
)


TICKERS = ["JPM", "BAC", "WFC"]


def run():
    metadata = {
        "batch_id": str(uuid4()),
        "fecha_carga_utc": datetime.utcnow(),
        "fuente": "yahoo_finance"
    }

    for ticker in TICKERS:
        print(f"Procesando {ticker}")

        try:
            prices_df = get_stock_prices(ticker)
            prices_df = transform_prices(prices_df, metadata)
            load_stock_prices(prices_df, engine)
            print(f"stock_prices cargado: {ticker}")
        except Exception as e:
            print(f"Error stock_prices {ticker}: {e}")

        try:
            profile_data = get_company_profile(ticker)
            profile_data = transform_company_profile(profile_data, metadata)
            load_company_profile(profile_data, engine)
            print(f"company_profile cargado: {ticker}")
        except Exception as e:
            print(f"Error company_profile {ticker}: {e}")

        try:
            fundamentals_data = get_fundamentals(ticker)
            fundamentals_data = transform_fundamentals(
                fundamentals_data,
                metadata
            )
            load_fundamentals(fundamentals_data, engine)
            print(f"fundamentals cargado: {ticker}")
        except Exception as e:
            print(f"Error fundamentals {ticker}: {e}")

        try:
            holders_df = get_holders(ticker)

            if holders_df is not None:
                holders_df = transform_holders(holders_df, metadata)
                load_holders(holders_df, engine)
                print(f"holders cargado: {ticker}")
            else:
                print(f"holders sin datos: {ticker}")

        except Exception as e:
            print(f"Error holders {ticker}: {e}")

        try:
            ratings_df = get_ratings(ticker)

            if ratings_df is not None:
                ratings_df = transform_ratings(ratings_df, metadata)
                load_ratings(ratings_df, engine)
                print(f"ratings cargado: {ticker}")
            else:
                print(f"ratings sin datos: {ticker}")

        except Exception as e:
            print(f"Error ratings {ticker}: {e}")


if __name__ == "__main__":
    run()