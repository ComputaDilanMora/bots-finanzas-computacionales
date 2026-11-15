"""Estrategia 4: Banda media de Bollinger (SMA20) + MACD(12,26,9). Ruptura direccional. Índice ^GSPC."""
import numpy as np
import pandas as pd
from indicators import sma, macd

TICKER, PERIOD, INTERVAL, TF = "^GSPC", "1y", "1d", "1D"


def senales(df: pd.DataFrame):
    c = df["Close"]
    m = sma(c, 20)
    linea, senal, _ = macd(c)
    s = pd.Series(np.where((c > m) & (linea > senal), 1, np.where((c < m) & (linea < senal), -1, 0)), index=df.index)
    return s, f"MACD={linea.iloc[-1]:.2f}"
