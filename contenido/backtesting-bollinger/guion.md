# Guion de Video: Backtesting con Bandas de Bollinger en Python (Masterclass Cuantitativa)

- **Duración estimada:** 13 minutos 30 segundos (rango objetivo: 12 - 15 minutos).
- **Tema:** Diseño, simulación y optimización de una estrategia cuantitativa sobre Bitcoin (`BTC-USD`) aplicando Bandas de Bollinger sobre retornos logarítmicos, con análisis de 200 combinaciones de Stop Loss y Take Profit, y advertencias sobre sesgos mortales en trading algorítmico.
- **Público objetivo:** Programadores, analistas cuantitativos, estudiantes de finanzas y traders que buscan pasar del análisis técnico subjetivo al backtesting estadístico riguroso en Python.
- **Archivo fuente del repositorio:** `AlgorithmicTrading/Backtesting/backtesting.ipynb` (16 celdas, intocado).

---

## Aviso Legal Obligatorio (Trading Disclaimer)

> **AVISO:** Este video es solo contenido educativo. No es asesoría financiera, ni una recomendación de compra o venta de ningún activo. Los resultados de un backtest son históricos y no garantizan resultados futuros. Operar criptomonedas y derivados implica un alto riesgo de pérdida de capital; nunca inviertas dinero que no puedas permitirte perder y consulta a un profesional autorizado.
> *(Política: Contenido educativo gratuito. No se vende ni se cobra ninguna estrategia como producto).*

---

## Tabla de Tiempos y Estructura

| Bloque | Minuto inicio | Minuto fin | Duración | Descripción |
|---|---|---|---|---|
| 0. Disclaimer y Gancho | 0:00 | 1:00 | 1:00 | Disclaimer en pantalla + El mito de la rentabilidad pasada: por qué el 95% de los backtests mienten. |
| 1. Fundamento Matemático: Retornos Logarítmicos | 1:00 | 2:45 | 1:45 | ¿Por qué retornos logarítmicos y no precio bruto? Estacionariedad y bandas $\mu \pm 2\sigma$. |
| 2. Secuencia en Notebook: Datos e Indicadores | 2:45 | 4:30 | 1:45 | Ejecución guiada de **Celdas 0, 1, 2, 3 y 4**: descarga Yahoo Finance, cálculo de `LOGRET_1` y bandas. |
| 3. El Motor del Backtester orientado a objetos | 4:30 | 6:30 | 2:00 | Ejecución de **Celdas 5, 6, 7, 8, 9 y 10**: clases `Order`, `Backtester`, órdenes, comisiones y gráfica de equity. |
| 4. Optimización de Parámetros (Grid Search) | 6:30 | 8:30 | 2:00 | Ejecución de **Celdas 11, 12 y 13**: 200 combinaciones (SL 1-20%, TP 5-50%) y los 4 mapas de calor. |
| 5. Análisis de Resultados: Retorno vs. Win Rate | 8:30 | 10:15 | 1:45 | Ejecución de **Celda 14**: el mejor retorno (1090.8%) vs la mejor tasa de acierto (71.6%). |
| 6. Las Tres Trampas Mortales del Cuantitativo | 10:15 | 12:30 | 2:15 | Sesgo de anticipación (*look-ahead bias*), sobreajuste (*overfitting*) y costes de deslizamiento (*slippage*). |
| 7. Conclusión y Llamada a la Acción (CTA) | 12:30 | 13:30 | 1:00 | Código en el repositorio, curso de Udemy, membresía del canal y debate. |

---

## Tabla de Pantallas y Elementos Visuales

| Bloque | Tipo de plano | Elemento en pantalla | Apoyo gráfico / Texto sobreimpreso |
|---|---|---|---|
| 0 | Cámara + Banner inferior | Presentador serio + Disclaimer legal completo en banner fijo | "Contenido educativo - No es asesoría financiera" |
| 1 | Pizarra digital / Diapositiva | Gráfica de precio no estacionario vs. gráfica de retornos con media cero y distribución normal | $r_t = \ln(P_t / P_{t-1})$; Bandas: $\text{BBU/BBL} = \text{SMA}_{20}(r_t) \pm 2\sigma_{20}$ |
| 2 | Jupyter Notebook | Pantalla completa con `backtesting.ipynb`: ejecutar Celdas 0 a 4; mostrar gráfica de retornos | Resaltar líneas punteadas verdes y rojas en torno al cero |
| 3 | Jupyter Notebook | Celdas 5 a 10: código de `Order` y `Backtester`, dataframes `orders_df`, `trades_df` y gráfico de 2 paneles | Resaltar panel superior (precio con triángulos) e inferior (curva de balance $10.000) |
| 4 | Jupyter Notebook | Celdas 11 a 13: barra de progreso de optimización (0% a 100%) y los 4 mapas de calor de Seaborn | Grilla 2x2: Total Return, Win Rate, Sharpe Ratio, Total Trades |
| 5 | Jupyter Notebook | Celda 14: tabla de parámetros óptimos en terminal del notebook | Comparativa: SL 1% / TP 50% (Win Rate 23.5%) vs SL 18% / TP 5% (Win Rate 71.6%) |
| 6 | Diapositiva de advertencia | Tres tarjetas rojas: 1. Look-ahead bias (`bfill`), 2. Overfitting (in-sample 2014-2024), 3. Slippage en SL 1% | "¿Tu backtest sobreviviría al mercado real?" |
| 7 | Cámara + Pantalla final | Presentador con llamadas interactivas al repo y curso | Tarjeta curso Udemy "Ciencia de datos con Python y R" + botón "Unirme" |

---

## Guion Detallado (Locución y Acciones)

### 0. Disclaimer y Gancho (0:00 - 1:00)
- **[CÁMARA CON DISCLAIMER FIJO EN PANTALLA]**
- *"Antes de comenzar, un aviso fundamental: este video tiene fines estrictamente educativos. No constituye asesoría financiera ni recomendación de inversión. El trading algorítmico y los derivados implican riesgo sustancial de pérdida de capital."*
- *"Dicho esto: ¿cuántas veces has visto en redes sociales capturas de pantalla de estrategias con un 1000% de rentabilidad o un 75% de acierto? La inmensa mayoría de esos números son una ilusión provocada por errores metodológicos que arruinan a cualquier trader en cuanto conecta dinero real."*
- *"Hoy vamos a abrir un notebook cuantitativo profesional de nuestro repositorio: `backtesting.ipynb`. Vamos a simular una estrategia sobre Bitcoin basada en Bandas de Bollinger sobre retornos logarítmicos, optimizaremos 200 combinaciones de Stop Loss y Take Profit, y destaparemos las tres trampas invisibles que separan un backtest de fantasía de la realidad de los mercados."*

### 1. Fundamento Matemático: Retornos Logarítmicos (`backtesting.ipynb:Celda 2`) (1:00 - 2:45)
- **[PIZARRA DIGITAL / GRÁFICA]**
- *"La mayoría de novatos aplican las Bandas de Bollinger directamente sobre el precio de cierre. En activos con tendencias exponenciales como Bitcoin, eso genera bandas asimétricas que se deforman con el tiempo."*
- *"En finanzas cuantitativas trabajamos con **retornos logarítmicos** continuos:"*
  $$r_t = \ln\left(\frac{P_t}{P_{t-1}}\right) = \ln(P_t) - \ln(P_{t-1})$$
- *"¿Por qué? Porque los precios son no estacionarios (tienen tendencia y varianza infinita), mientras que los retornos oscilan alrededor de una media cercana a cero con varianza finita."*
- *"Sobre esta serie de retornos calculamos la media móvil simple de 20 periodos y sumamos o restamos 2 desviaciones típicas ($\sigma$):"*
  $$\text{BBU}_t = \mu_{20}(r) + 2\sigma_{20}(r), \quad \text{BBL}_t = \mu_{20}(r) - 2\sigma_{20}(r)$$
- *"Cuando el retorno diario supera la banda superior, no significa sobrecompra clásica: significa una **anomalía de volatilidad positiva** (impulso alcista inusual). Esa es la señal que utilizaremos."*

### 2. Secuencia en Notebook: Datos e Indicadores (`Celdas 0 a 4`) (2:45 - 4:30)
- **[JUPYTER NOTEBOOK EN PANTALLA COMPLETA]**
- *"Pasamos al notebook. Vamos a ejecutar las primeras celdas paso a paso:"*
- **Ejecutar Celda 0:** *"Importamos las librerías: `matplotlib`, `yfinance`, `pandas`, `numpy` y `pandas_ta`."*
- **Ejecutar Celda 1:** *"Descargamos el histórico diario de `BTC-USD` desde septiembre de 2014 hasta hoy con `yfinance`. Obtenemos los precios OHLC estándar."*
  - **Resultado en pantalla:** DataFrame con más de 3.500 velas diarias arrancando en 465 USD en 2014.
- **Ejecutar Celda 2:** *"Añadimos los indicadores con dos líneas usando `pandas_ta`:"*
  ```python
  df.ta.log_return(cumulative=False, append=True)
  df.ta.bbands(close=df['LOGRET_1'], length=20, std=2, append=True)
  ```
  - **Resultado en pantalla:** Columnas añadidas: `LOGRET_1`, `BBL_20_2.0`, `BBM_20_2.0`, `BBU_20_2.0`.
- **Ejecutar Celda 3:** *"Generamos la señal:"*
  ```python
  df["SIGNAL"] = np.where(df["LOGRET_1"] > df["BBU_20_2.0"], 1,
                         np.where(df["LOGRET_1"] < df["BBL_20_2.0"], -1, np.nan))
  df["SIGNAL"] = df["SIGNAL"].ffill().bfill()
  ```
  - *"Cuando el retorno supera la banda superior marcamos 1 (compra). Cuando cae por debajo de la inferior marcamos -1 (venta). Rellenamos hacia adelante con `ffill()` y hacia atrás con `bfill()`."* *(Ojo: quédate con esa línea, porque volveremos a ella en la sección de advertencias).*
- **Ejecutar Celda 4:** *"Mostramos la gráfica de retornos."*
  - **Resultado en pantalla:** Gráfica horizontal donde los retornos oscilan entre -15% y +15%, con las bandas verdes y rojas delimitando la volatilidad normal y los puntos de ruptura claramente visibles.

### 3. El Motor del Backtester (`Celdas 5 a 10`) (4:30 - 6:30)
- **[JUPYTER NOTEBOOK - CELDAS 5 A 10]**
- *"Ahora necesitamos un motor de ejecución realista. En vez de multiplicar retornos ciegamente con un `shift`, el notebook implementa un simulador orientado a objetos:"*
- **Ejecutar Celdas 5 y 6:** *"Definimos la clase `Order` (con marca temporal, símbolo, lado, cantidad, precio de ejecución y comisiones) y `BacktestingSettings`."*
- **Ejecutar Celda 7:** *"Configuramos un primer escenario base:"*
  - Capital inicial: 10.000 USD
  - Tamaño de posición: 500 USD fijos por operación
  - Comisión por operación: **0.75%** (muy realista para exchanges spot / taker)
  - Take Profit: 50%
  - Stop Loss: 1%
- **Ejecutar Celdas 8 y 9:** *"Inspeccionamos los registros `orders_df` y `trades_df`. Cada entrada registra el precio exacto de compra, la comisión deducida y el motivo de salida (por señal, por Stop Loss o por Take Profit)."*
- **Ejecutar Celda 10:** *"Graficamos el rendimiento."*
  - **Resultado en pantalla:** Un gráfico en dos niveles. Arriba, el precio de Bitcoin en escala semilogarítmica con triángulos verdes de compra y rojos de venta. Abajo, la curva de balance (*Equity Curve*), mostrando cómo el capital de 10.000 USD evoluciona a lo largo de los ciclos con sus respectivas caídas (*drawdowns*).

### 4. Optimización de Parámetros: Grid Search (`Celdas 11 a 13`) (6:30 - 8:30)
- **[JUPYTER NOTEBOOK - CELDAS 11 A 13]**
- *"¿Cómo sabemos si un Stop Loss del 1% y un Take Profit del 50% son los mejores valores? Vamos a comprobarlo matemáticamente con una búsqueda en rejilla (*Grid Search*):"*
- **Ejecutar Celda 11:**
  - Rango de Stop Loss: de 1% a 20% en pasos de 1% (20 valores).
  - Rango de Take Profit: de 5% a 50% en pasos de 5% (10 valores).
  - **Total:** $20 \times 10 = 200$ combinaciones simultáneas.
- **Ejecutar Celda 12:** *"Lanzamos la función `run_backtest_optimization(df, ...)`."*
  - **Resultado en pantalla:** Barra de progreso completando del 10% al 100% en pocos segundos, calculando para cada combinación el retorno total, la tasa de acierto (*win rate*), el ratio de Sharpe y el número total de operaciones.
- **Ejecutar Celda 13:** *"Generamos los 4 mapas de calor con `create_heatmaps`."*
  - **Resultado en pantalla:** Cuatro mapas de calor 2D espectaculares:
    1. **Total Return:** tonos brillantes concentrados en la esquina superior izquierda (Stop Loss muy ajustado, Take Profit amplio).
    2. **Win Rate:** el patrón es exactamente el inverso: la tasa de acierto sube hacia la esquina inferior derecha (Stop Loss amplio, Take Profit pequeño).
    3. **Sharpe Ratio:** resalta la zona óptima de rendimiento ajustado al riesgo.
    4. **Total Trades:** muestra la frecuencia operativa según la tolerancia de salida.

### 5. Análisis de Resultados: Retorno vs. Win Rate (`Celda 14`) (8:30 - 10:15)
- **[JUPYTER NOTEBOOK - CELDA 14]**
- **Ejecutar Celda 14:** *"Llamamos a `find_optimal_parameters(results_df)`. Miremos con lupa los datos exactos que arroja el script:"*
- **1. Mejor Retorno Total:**
  - Stop Loss: **1.0%** | Take Profit: **50.0%**
  - **Retorno Total: +1090.8%** | 272 operaciones | **Tasa de acierto: 23.5%**
  - *"Fíjate en esto: ¡pierde en el 76.5% de las operaciones! Tres de cada cuatro operaciones son perdedoras, pero gana dinero porque cuando pierde solo cede un 1%, y cuando acierta captura un movimiento de hasta el 50%. Es la clásica asimetría del trend-following."*
- **2. Mayor Tasa de Acierto (Win Rate):**
  - Stop Loss: **18.0%** | Take Profit: **5.0%**
  - **Tasa de acierto: 71.6%** | 264 operaciones
  - *"Acierta 7 de cada 10 veces, pero arriesga un 18% para ganar un misero 5%. Si el mercado sufre una racha de tres pérdidas consecutivas del 18%, destruye meses de ganancias pequeñas."*
- **3. Mejor Ratio de Sharpe:**
  - Stop Loss: **12.0%** | Take Profit: **40.0%** | **Sharpe Ratio: 0.39** | Win Rate: 55.1% | 89 operaciones.

### 6. Las Tres Trampas Mortales del Cuantitativo (10:15 - 12:30)
- **[DIAPOSITIVA DE ADVERTENCIA / PANTALLA DIVIDIDA]**
- *"Ahora viene la lección más importante de todo este video. Ese +1090% de retorno es muy tentador, pero en trading real sería una catástrofe. ¿Por qué?"*
- **Trampa 1: Sesgo de Anticipación (*Look-Ahead Bias*)**
  - *"En la Celda 3 escribimos `df['SIGNAL'] = df['SIGNAL'].ffill().bfill()`. El uso de `bfill()` al inicio rellena señales hacia atrás usando información futura. Además, la señal se calcula con el precio de cierre de la vela diaria, pero el backtest asume que puedes entrar a ese mismo precio de cierre instantáneamente. En vivo, entras en la apertura de la vela siguiente."*
- **Trampa 2: Sobreajuste al Histórico (*Overfitting*)**
  - *"Probamos 200 combinaciones sobre los mismos datos históricos de 2014 a 2024. Escoger el '1% SL / 50% TP' simplemente porque fue el que mejor funcionó en el pasado sobre esa muestra concreta se llama sesgo de selección o minería de datos (*data snooping*). Sin una validación fuera de muestra (*Out-of-Sample*) o un análisis de ventana móvil (*Walk-Forward Analysis*), este número no tiene validez estadística hacia el futuro."*
- **Trampa 3: Comisiones y Deslizamiento (*Slippage*) con Stop Loss de 1%**
  - *"Bitcoin tiene una volatilidad intradiaria media superior al 3-4%. Si colocas un Stop Loss del 1%, cualquier mecha de ruido intradiario te expulsará de la posición antes de que comience el movimiento. Y con una comisión de exchange del 0.75%, ¡la comisión representa tres cuartas partes de todo tu margen de stop!"*

### 7. Conclusión y Llamada a la Acción (CTA) (12:30 - 13:30)
- **[CÁMARA]**
- *"Tienes el notebook `backtesting.ipynb` disponible tal cual en el repositorio de GitHub de Sunday-Tutorials enlazado en la descripción para que experimentes con otros periodos y parámetros."*
- *"Si quieres aprender a estructurar análisis cuantitativos rigurosos, limpieza de datos y modelado estadístico con Python y R, te espero en mi curso de Udemy en el enlace con descuento de abajo."*
- *"Para apoyar la producción de contenido cuantitativo abierto y de calidad, haz clic en el botón 'Unirme' en la portada de nuestro canal."*
- *"Déjame tu opinión en los comentarios: ¿prefieres operar con estrategias de alta tasa de acierto y bajo ratio beneficio/riesgo, o con baja tasa de acierto y pagos asimétricos? ¡Te leo y nos vemos en la próxima masterclass!"*
