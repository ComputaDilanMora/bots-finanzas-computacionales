"""Estrategia 5: Envelopes (EMA20 +/-1.5%) + Williams %R(14) + giro del histograma MACD. Cripto SOL-USD."""
import numpy as np
import pandas as pd
from indicators import ema, williams_r, macd

TICKER, PERIOD, INTERVAL, TF = "SOL-USD", "3mo", "1h", "1H"


def senales(df: pd.DataFrame):
    c = df["Close"]
    e = ema(c, 20)
    wr = williams_r(df, 14)
    _, _, hist = macd(c)
    sube, baja = hist > hist.shift(1), hist < hist.shift(1)
    s = pd.Series(
        np.where((c <= e * 0.985) & (wr < -80) & sube, 1,
                 np.where((c >= e * 1.015) & (wr > -20) & baja, -1, 0)),
        index=df.index,
    )
    return s, f"WR={wr.iloc[-1]:.1f} | Hist={hist.iloc[-1]:.3f}"
