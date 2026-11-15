"""Estrategia 3: Nube Ichimoku (9,26,52) + Williams %R(14). Tendencia + timing. Divisas EURUSD=X."""
import numpy as np
import pandas as pd
from indicators import ichimoku, williams_r

TICKER, PERIOD, INTERVAL, TF = "EURUSD=X", "6mo", "1h", "1H"


def senales(df: pd.DataFrame):
    c = df["Close"]
    tenkan, kijun, a, b = ichimoku(df)
    techo, piso = pd.concat([a, b], axis=1).max(axis=1), pd.concat([a, b], axis=1).min(axis=1)
    wr = williams_r(df, 14)
    s = pd.Series(
        np.where((c > techo) & (tenkan > kijun) & (wr < -80), 1,
                 np.where((c < piso) & (tenkan < kijun) & (wr > -20), -1, 0)),
        index=df.index,
    )
    return s, f"Williams %R={wr.iloc[-1]:.2f}"
