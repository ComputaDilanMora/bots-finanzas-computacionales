# Bots de trading algorítmico — Finanzas Computacionales

Cinco estrategias técnicas que corren cada hora en GitHub Actions y avisan por Telegram.

| Bot | Indicadores | Activo |
|---|---|---|
| envelopes_rsi | Envelopes + RSI | ETH-USD |
| ema_elder_ray | EMA + Elder-Ray | BTC-USD |
| ichimoku_wr | Ichimoku + Williams %R | EURUSD=X |
| bb_macd | Banda media Bollinger + MACD | ^GSPC |
| envelopes_wr_macd | Envelopes + Williams %R + MACD | SOL-USD |

Secrets requeridos (Settings > Secrets and variables > Actions): `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`.

Uso local: `pip install -r requirements.txt`, `python run_bot.py <estrategia>`, `python backtest.py`.
Aviso: proyecto académico, no es asesoría financiera.
