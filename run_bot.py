"""Uso: python run_bot.py <nombre_estrategia>   (ej. python run_bot.py bb_macd)"""
import sys

from core import obtener_datos, gestionar_alerta
from strategies import TODAS


def main(nombre: str) -> None:
    est = TODAS[nombre]
    df = obtener_datos(est.TICKER, est.PERIOD, est.INTERVAL)
    s, detalle = est.senales(df)
    senal, precio = int(s.iloc[-1]), float(df["Close"].iloc[-1])
    print(f"{nombre} {est.TICKER} señal={senal} cierre={precio:.4f} {detalle}")
    gestionar_alerta(nombre, est.TICKER, est.TF, senal, precio, detalle)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in TODAS:
        sys.exit("Uso: python run_bot.py <" + "|".join(TODAS) + ">")
    main(sys.argv[1])
