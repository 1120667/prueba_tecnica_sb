import pandas as pd


def add_metadata_to_dict(data, metadata):
    data["fecha_carga_utc"] = metadata["fecha_carga_utc"]
    data["fuente"] = metadata["fuente"]
    data["batch_id"] = metadata["batch_id"]
    return data


def add_metadata_to_df(df, metadata):
    df["fecha_carga_utc"] = metadata["fecha_carga_utc"]
    df["fuente"] = metadata["fuente"]
    df["batch_id"] = metadata["batch_id"]
    return df


def transform_prices(df, metadata):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns = [col.strip().lower() for col in df.columns]

    df = df[[
        "date", "open", "high", "low", "close", "volume", "ticker"
    ]]

    return add_metadata_to_df(df, metadata)


def transform_company_profile(data, metadata):
    data = {
        "ticker": data.get("ticker"),
        "industry": data.get("industry"),
        "sector": data.get("sector"),
        "employees": data.get("employee_count"),
        "city": data.get("city"),
        "state": data.get("state"),
        "country": data.get("country"),
        "website": data.get("website"),
        "address": data.get("address"),
        "phone": data.get("phone"),
    }

    return add_metadata_to_dict(data, metadata)


def transform_fundamentals(data, metadata):
    data = {
        "ticker": data.get("ticker"),
        "date": data.get("date"),
        "total_assets": data.get("assets"),
        "total_debt": data.get("debt"),
        "invested_capital": data.get("invested_capital"),
        "shares_issued": data.get("share_issued"),
    }

    return add_metadata_to_dict(data, metadata)


def transform_holders(df, metadata):
    df.columns = [
        col.strip().lower().replace(" ", "_")
        for col in df.columns
    ]

    df = df.rename(columns={
        "date_reported": "date",
        "holder": "holder",
        "shares": "shares",
        "value": "value",
        "ticker": "ticker"
    })

    expected_columns = [
        "ticker", "date", "holder", "shares", "value"
    ]

    for col in expected_columns:
        if col not in df.columns:
            df[col] = None

    df = df[expected_columns]

    return add_metadata_to_df(df, metadata)


def transform_ratings(df, metadata):
    df.columns = [
        col.strip().lower().replace(" ", "_")
        for col in df.columns
    ]

    df = df.rename(columns={
        "date": "date",
        "to_grade": "to_grade",
        "from_grade": "from_grade",
        "action": "action",
        "ticker": "ticker"
    })

    expected_columns = [
        "ticker", "date", "to_grade", "from_grade", "action"
    ]

    for col in expected_columns:
        if col not in df.columns:
            df[col] = None

    df = df[expected_columns]

    return add_metadata_to_df(df, metadata)