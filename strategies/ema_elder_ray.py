"""Estrategia 2: EMA9/EMA21 + Elder-Ray (Bulls/Bears Power sobre EMA13). Tendencia. Cripto BTC-USD."""
import numpy as np
import pandas as pd
from indicators import ema, elder_ray

TICKER, PERIOD, INTERVAL, TF = "BTC-USD", "6mo", "1d", "1D"


def senales(df: pd.DataFrame):
    c = df["Close"]
    bulls, bears = elder_ray(df, 13)
    e9, e21 = ema(c, 9), ema(c, 21)
    s = pd.Series(np.where((e9 > e21) & (bulls > 0), 1, np.where((e9 < e21) & (bears < 0), -1, 0)), index=df.index)
    return s, f"Bulls={bulls.iloc[-1]:.1f} | Bears={bears.iloc[-1]:.1f}"
