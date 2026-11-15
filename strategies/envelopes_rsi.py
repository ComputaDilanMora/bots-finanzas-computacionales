"""Estrategia 1: Envelopes (SMA20 +/-2.5%) + RSI14. Reversión a la media. Cripto ETH-USD."""
import numpy as np
import pandas as pd
from indicators import sma, rsi

TICKER, PERIOD, INTERVAL, TF = "ETH-USD", "3mo", "1h", "1H"


def senales(df: pd.DataFrame):
    c = df["Close"]
    m = sma(c, 20)
    r = rsi(c, 14)
    s = pd.Series(np.where((c < m * 0.975) & (r < 30), 1, np.where((c > m * 1.025) & (r > 70), -1, 0)), index=df.index)
    return s, f"RSI={r.iloc[-1]:.2f}"
