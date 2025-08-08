def forecast_from_csv(csv_path: str, periods: int, freq: str = 'D'):
    df = pd.read_csv(csv_path)

    print("📊 CSV content:")
    print(df.head())

    if 'ds' not in df.columns or 'y' not in df.columns:
        raise ValueError("CSV must contain 'ds' and 'y' columns")

    df['ds'] = pd.to_datetime(df['ds'])

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)

    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)

    print("📈 Forecast result:")
    print(result)

    return result
