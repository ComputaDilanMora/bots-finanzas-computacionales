"""Indicadores técnicos vectorizados (pandas). Usados por los bots y por el backtest."""
import pandas as pd


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n).mean()


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    """RSI de Wilder (suavizado exponencial alpha=1/n), igual al de TradingView."""
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + gain / loss)


def macd(close: pd.Series, fast=12, slow=26, sig=9):
    linea = ema(close, fast) - ema(close, slow)
    senal = ema(linea, sig)
    return linea, senal, linea - senal


def williams_r(df: pd.DataFrame, n: int = 14) -> pd.Series:
    hh = df["High"].rolling(n).max()
    ll = df["Low"].rolling(n).min()
    return -100 * (hh - df["Close"]) / (hh - ll)


def ichimoku(df: pd.DataFrame, t=9, k=26, b=52):
    tenkan = (df["High"].rolling(t).max() + df["Low"].rolling(t).min()) / 2
    kijun = (df["High"].rolling(k).max() + df["Low"].rolling(k).min()) / 2
    span_a = ((tenkan + kijun) / 2).shift(k)
    span_b = ((df["High"].rolling(b).max() + df["Low"].rolling(b).min()) / 2).shift(k)
    return tenkan, kijun, span_a, span_b


def elder_ray(df: pd.DataFrame, n: int = 13):
    e = ema(df["Close"], n)
    return df["High"] - e, df["Low"] - e  # bulls, bears
