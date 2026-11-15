"""Motor: descarga de datos (yfinance), memoria de estado (JSON) y notificación a Telegram."""
import json
import os

import pandas as pd
import requests
import yfinance as yf

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state")


def obtener_datos(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df.dropna()


def enviar_telegram(mensaje: str) -> None:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Faltan credenciales de Telegram. Mensaje:\n" + mensaje)
        return
    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"},
        timeout=15,
    )
    r.raise_for_status()


def gestionar_alerta(nombre, ticker, temporalidad, senal, precio, detalle) -> bool:
    """Avisa solo si hay señal activa (1/-1) distinta a la última guardada. Devuelve True si avisó."""
    os.makedirs(STATE_DIR, exist_ok=True)
    ruta = os.path.join(STATE_DIR, f"{nombre}.json")
    anterior = 0
    if os.path.exists(ruta):
        with open(ruta) as f:
            anterior = json.load(f).get("ultima_senal", 0)

    avisó = False
    if senal != 0 and senal != anterior:
        tipo = "🟢 COMPRA" if senal == 1 else "🔴 VENTA"
        enviar_telegram(
            f"*{tipo} — {nombre.upper()}*\n"
            f"• *Activo:* `{ticker}` ({temporalidad})\n"
            f"• *Precio cierre:* `${precio:,.4f}`\n"
            f"• *Condición:* {detalle}"
        )
        avisó = True

    with open(ruta, "w") as f:
        json.dump({"ultima_senal": int(senal)}, f)
    return avisó
