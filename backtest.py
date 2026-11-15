"""Backtest simple long-only de las 5 estrategias.

Reglas: 1 = entrar/mantener largo, -1 = salir a efectivo, 0 = mantener la posición anterior.
La posición se aplica a la vela SIGUIENTE (sin mirar el futuro). Comisión 0.1% por cambio de posición.
Uso: python backtest.py   -> imprime tabla y guarda backtest_resultados.csv y graficas/*.png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from core import obtener_datos
from strategies import TODAS

COMISION = 0.001
# Historia más larga que la del bot en vivo: 1h permite máx. ~730 días en Yahoo; 1d usamos 5 años.
PERIODO_BT = {"1h": "730d", "1d": "5y"}


def backtest(df, senal):
    pos = senal.replace(0, float("nan")).ffill().clip(lower=0).fillna(0)  # largo=1, efectivo=0
    pos = pos.shift(1).fillna(0)
    ret = df["Close"].pct_change().fillna(0)
    costo = pos.diff().abs().fillna(0) * COMISION
    estrategia = (1 + pos * ret - costo).cumprod()
    bh = (1 + ret).cumprod()
    return pos, estrategia, bh


def max_dd(curva):
    return float((curva / curva.cummax() - 1).min())


def main():
    os.makedirs("graficas", exist_ok=True)
    filas = []
    for nombre, est in TODAS.items():
        df = obtener_datos(est.TICKER, PERIODO_BT[est.INTERVAL], est.INTERVAL)
        s, _ = est.senales(df)
        pos, curva, bh = backtest(df, s)
        entradas = int(((pos.diff() == 1)).sum())
        filas.append({
            "estrategia": nombre, "activo": est.TICKER, "velas": len(df),
            "señales_compra": int((s == 1).sum()), "señales_venta": int((s == -1).sum()),
            "operaciones": entradas,
            "retorno_estrategia_%": round((curva.iloc[-1] - 1) * 100, 2),
            "retorno_buy&hold_%": round((bh.iloc[-1] - 1) * 100, 2),
            "max_drawdown_%": round(max_dd(curva) * 100, 2),
            "tiempo_en_mercado_%": round(pos.mean() * 100, 1),
        })
        fig, ax = plt.subplots(figsize=(9, 4))
        curva.plot(ax=ax, label="Estrategia"); bh.plot(ax=ax, label="Buy & Hold")
        ax.set_title(f"{nombre} — {est.TICKER} ({est.INTERVAL})"); ax.legend(); ax.grid(alpha=.3)
        fig.tight_layout(); fig.savefig(f"graficas/{nombre}.png", dpi=130); plt.close(fig)

    res = pd.DataFrame(filas)
    res.to_csv("backtest_resultados.csv", index=False)
    pd.set_option("display.width", 200)
    print(res.to_string(index=False))


if __name__ == "__main__":
    main()
