# historicaldatabinance

> El nombre de la carpeta es histórico: `hist_data.py` **no usa Binance, usa Bitstamp**.

## `hist_data.py` — descarga de velas (Bitstamp)

Pide a Bitstamp (vía `ccxt`, API pública, sin claves) velas de **BTC/USDT** de 1 hora, en bloques de hasta 1500, desde `2018-01-01` hasta ahora, y las imprime por pantalla (ordenadas de más nuevas a más antiguas). **No guarda ningún archivo**, a pesar del nombre `save_candles`. La descarga empieza al importar/ejecutar el script.

- Librerías: `ccxt`, `pandas`.
- Requiere Internet. Si una petición falla imprime `No more data`; sin red o si el par no está disponible el script terminará con error.

```bash
python historicaldatabinance/hist_data.py
```

## `btcdata.py` — RSI y FFT sobre el precio (datos locales)

Lee `btcprice.csv` (junto al script, se encuentra desde cualquier carpeta), calcula el RSI de 30 periodos, su media móvil de 30 y la transformada de Fourier de esa media, y dibuja 3 gráficos: precio, RSI (+ media móvil) y espectro FFT.

- Librerías: `pandas`, `pandas_ta`, `numpy`, `matplotlib`. `pandas_ta` depende de `numba`, que puede no estar disponible para las versiones de Python más recientes: usa una versión de Python compatible con tu instalación de `pandas_ta`.
- Salida esperada: ventana de matplotlib con tres subgráficos (sin salida por consola; matplotlib puede avisar de que descarta la parte imaginaria de la FFT al dibujar).

```bash
python historicaldatabinance/btcdata.py
```

## Datos

`btcprice.csv`: columnas `Timestamp` (fecha) y `market-price` (precio medio de BTC en USD, una fila cada ~3 días, del 2009-01-02 al 2021-04-18; ~1500 filas; empieza con BOM UTF-8). Se conserva tal cual; no se ha verificado su origen exacto.
