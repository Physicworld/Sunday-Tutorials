# TestMarkovChi

`test.ipynb` estudia si los retornos diarios de BTC tienen «memoria»: discretiza los retornos en 2, 3 y 4 estados (por cuantiles), cuenta las transiciones entre estados de días consecutivos (matriz de Markov) y aplica el test chi-cuadrado de independencia. El notebook incluye hipótesis, método y conclusión en celdas markdown.

- Librerías: `numpy`, `pandas`, `matplotlib`, `scipy`, y `jupyter` para abrirlo.
- **Abre el notebook con esta carpeta como directorio de trabajo** (`jupyter lab` dentro de `TestMarkovChi/`): el CSV se lee con la ruta relativa `BTC-USD.csv`.
- Salida esperada: las matrices de transición y, para cada número de estados, `(matriz, chi², p-valor)`. Con los datos incluidos los p-valores son muy pequeños (independencia rechazada).

## Datos

`BTC-USD.csv`: cierres diarios de BTC-USD (columnas `Date, Open, High, Low, Close, Adj Close, Volume`, formato de Yahoo Finance) del 2014-09-17 al 2023-08-21, ~3260 filas. Se conserva tal cual.
