import yfinance as yf


def get_stock_prices(ticker, start="2024-01-01", end="2025-12-31"):
    df = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        group_by="column",
        auto_adjust=False,
        progress=False
    )

    df.reset_index(inplace=True)
    df["ticker"] = ticker

    return df


def get_company_profile(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info or {}

    return {
        "ticker": ticker,
        "industry": info.get("industry"),
        "sector": info.get("sector"),
        "employee_count": info.get("fullTimeEmployees"),
        "city": info.get("city"),
        "phone": info.get("phone"),
        "state": info.get("state"),
        "country": info.get("country"),
        "website": info.get("website"),
        "address": info.get("address1"),
    }


from datetime import date

def get_fundamentals(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info or {}

    return {
        "ticker": ticker,
        "date": date.today(),
        "assets": info.get("totalAssets"),
        "debt": info.get("totalDebt"),
        "invested_capital": info.get("investedCapital"),
        "share_issued": info.get("sharesOutstanding"),
    }


def get_holders(ticker):
    stock = yf.Ticker(ticker)
    df = stock.institutional_holders

    if df is None or df.empty:
        return None

    df["ticker"] = ticker
    return df


def get_ratings(ticker):
    stock = yf.Ticker(ticker)
    df = stock.upgrades_downgrades

    if df is None or df.empty:
        return None

    df.reset_index(inplace=True)
    df["ticker"] = ticker
    return df