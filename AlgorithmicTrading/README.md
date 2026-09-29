# AlgorithmicTrading

Scripts y notebooks exploratorios de análisis de Bitcoin del canal. Son material educativo (no asesoramiento financiero) y no forman una librería.

| Carpeta | Qué hace | Exchange / datos |
| --- | --- | --- |
| [`FinancialGraphs/`](FinancialGraphs/README.md) | Gráfico de velas interactivo | Binance (ccxt), red |
| [`historicaldatabinance/`](historicaldatabinance/README.md) | Descarga histórica de velas y FFT del RSI | `hist_data.py`: **Bitstamp**; `btcdata.py`: CSV local |
| [`TestMarkovChi/`](TestMarkovChi/README.md) | Cadena de Markov + chi-cuadrado sobre retornos diarios | CSV local (BTC-USD) |
| `Backtesting/` | Notebooks de backtesting | Sin documentar aquí (otro ticket) |

> Aviso: la carpeta `historicaldatabinance` se llama «binance», pero `hist_data.py` consulta **Bitstamp**. El nombre se mantiene para no romper enlaces de vídeos anteriores.

Dependencias por módulo: cada carpeta declarará su `requirements.txt` (ticket STQ-9). Mientras tanto, las librerías están indicadas en el README de cada carpeta.
