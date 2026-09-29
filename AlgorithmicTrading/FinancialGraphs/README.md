# FinancialGraphs

`graph.py` descarga 1000 velas de 15 minutos de **BTC/USDT desde Binance** (a través de `ccxt`, API pública, sin claves) y abre un gráfico de velas interactivo con Plotly en el navegador.

- Librerías: `ccxt`, `pandas`, `plotly`.
- Requiere conexión a Internet (si Binance no es accesible desde tu región, `ccxt` lanzará un error de red/HTTP).
- Ejecutar (desde cualquier carpeta):

```bash
python FinancialGraphs/graph.py
```

- Salida esperada: se abre una pestaña del navegador con el gráfico de velas de las últimas ~10 días (1000 × 15 min). No escribe archivos.
