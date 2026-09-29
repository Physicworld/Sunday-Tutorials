# Guion de Video: Análisis de Ciclos de Bitcoin en Python (RSI Mensual y Halvings)

- **Duración estimada:** 13 minutos 00 segundos (rango objetivo: 12 - 15 minutos).
- **Tema:** Visualización y análisis cuantitativo de los ciclos cuatrienales de Bitcoin (`BTC-USD`) con Python: descarga de datos, remuestreo mensual, cálculo del RSI de 14 periodos y renderizado de un gráfico profesional en tema oscuro con fechas exactas de halving y zonas macro de acumulación y distribución.
- **Público objetivo:** Desarrolladores, inversores cuantitativos, entusiastas de cripto y analistas de datos interesados en modelos macroeconómicos y visualizaciones financieras de nivel institucional.
- **Archivo fuente del repositorio:** `AlgorithmicTrading/Backtesting/bitcoin_cycles.ipynb` (5 celdas, intocado).

---

## Aviso Legal Obligatorio (Trading Disclaimer)

> **AVISO:** Este video es solo contenido educativo. No es asesoría financiera, ni una recomendación de compra o venta de ningún activo. Los resultados de un backtest son históricos y no garantizan resultados futuros. Operar criptomonedas y derivados implica un alto riesgo de pérdida de capital; nunca inviertas dinero que no puedas permitirte perder y consulta a un profesional autorizado.
> *(Política: Contenido educativo gratuito. No se vende ni se cobra ninguna estrategia como producto).*

---

## Tabla de Tiempos y Estructura

| Bloque | Minuto inicio | Minuto fin | Duración | Descripción |
|---|---|---|---|---|
| 0. Disclaimer y Gancho | 0:00 | 1:15 | 1:15 | Disclaimer obligatorio + El enigma de los 4 años: ¿por qué Bitcoin se mueve en ciclos sincronizados? |
| 1. Fundamento Matemático y de Oferta | 1:15 | 3:00 | 1:45 | La matemática del Halving ($210.000$ bloques) y la fórmula del RSI mensual ($14$ barras). |
| 2. Secuencia en Notebook: Datos y Remuestreo | 3:00 | 5:00 | 2:00 | Ejecución de **Celdas 0 y 1**: librerías, descarga con `yfinance`, resample mensual y cálculo de `RSI_14`. |
| 3. Renderizado del Gráfico de Estilo Oscuro | 5:00 | 7:30 | 2:30 | Ejecución de **Celda 2**: configuración estética (`#1a1a1a`, `#00BFFF`, `#FFD700`), escala logarítmica y 2 subplots. |
| 4. Lectura Cuantitativa del Gráfico | 7:30 | 9:30 | 2:00 | Análisis de los picos históricos (2013, 2017, 2021) sobre RSI > 85 y los suelos de invierno en RSI < 47. |
| 5. Advertencias Críticas: Muestra N=4 y Rendimientos Decrecientes | 9:30 | 11:45 | 2:15 | Sesgo del tamaño muestral minúsculo ($N=4$), rendimientos decrecientes y la entrada de ETFs institucionales. |
| 6. Conclusión y Llamada a la Acción (CTA) | 11:45 | 13:00 | 1:15 | Notebook en el repositorio, curso de ciencia de datos en Udemy, membresía y pregunta de cierre. |

---

## Tabla de Pantallas y Elementos Visuales

| Bloque | Tipo de plano | Elemento en pantalla | Apoyo gráfico / Texto sobreimpreso |
|---|---|---|---|
| 0 | Cámara + Banner inferior | Presentador con el gráfico oscuro de Bitcoin visible en el monitor de fondo | Banner legal: "Contenido educativo - No es asesoría financiera" |
| 1 | Esquema animado | Infografía del bloque génesis a hoy: emisión de 50 a 3.125 BTC; fórmula de Wilder del RSI | $\text{RSI} = 100 - \frac{100}{1 + RS}, \quad RS = \frac{\text{EMA}(\text{subidas}, 14)}{\text{EMA}(\text{bajadas}, 14)}$ |
| 2 | Jupyter Notebook | Pantalla completa con `bitcoin_cycles.ipynb`: Celdas 0 y 1; advertencia de `FutureWarning: 'M'` | Resaltar dataframe con fechas mensuales de 2014 a hoy |
| 3 | Jupyter Notebook | Celda 2: paleta de colores oscuros (`BG_COLOR='#1a1a1a'`) y generación del gráfico en 18x12 pulgadas | Resaltar líneas punteadas de Halving y áreas de color |
| 4 | Zoom sobre el Gráfico | Panel superior (precio logarítmico) y panel inferior (oscilador RSI 14 mensual con franjas 47 y 85) | Resaltar las cumbres de ciclo cuando el RSI toca la banda roja superior |
| 5 | Diapositiva de advertencia | Tres tarjetas rojas: 1. Falacia de muestra pequeña ($N=4$), 2. Capitalización y volumen decreciente, 3. Macroeconomía y ETFs | "¿La historia se repite o solo rima?" |
| 6 | Cámara + Pantalla final | Presentador con pantalla dividida mostrando repo y curso | Miniatura del curso de Udemy en la descripción + botón "Unirme" |

---

## Guion Detallado (Locución y Acciones)

### 0. Disclaimer y Gancho (0:00 - 1:15)
- **[CÁMARA CON DISCLAIMER FIJO EN PANTALLA]**
- *"Aviso legal prioritario: este video es exclusivamente educativo. No es asesoría financiera ni recomendación de inversión. Las criptomonedas son activos de alta volatilidad y riesgo."*
- *"Dicho esto: desde su creación en 2009, el precio de Bitcoin parece obedecer una melodía matemática casi perfecta. Cada cuatro años, el mercado experimenta una fase de acumulación brutal, seguida de una carrera alcista parabólica, una distribución eufórica y un invierno gélido donde el activo corrige entre un 70% y un 85%."*
- *"¿Es casualidad? ¿O es una propiedad emergente de la política monetaria algorítmica inscrita en su código fuente?"*
- *"Hoy vamos a abrir el notebook `bitcoin_cycles.ipynb` de nuestro repositorio. Aprenderás a construir una visualización profesional en tema oscuro que mapea los cuatro ciclos históricos de Bitcoin, sus fechas de halving y cómo el indicador RSI en escala mensual ayuda a separar el ruido del mercado de los verdaderos puntos de inflexión macro."*

### 1. Fundamento Matemático y de Oferta (1:15 - 3:00)
- **[PIZARRA DIGITAL / INFOGRAFÍA]**
- *"La columna vertebral de este modelo descansa en dos pilares matemáticos:"*
- **1. La curva de emisión programada y el Halving:**
  - *"Cada 210.000 bloques minados (aproximadamente cada 3,9 años a razón de un bloque cada 10 minutos), la recompensa por bloque para los mineros se reduce a la mitad:"*
    - *2009: 50 BTC por bloque*
    - *2012 (1º Halving): 25 BTC*
    - *2016 (2º Halving): 12.5 BTC*
    - *2020 (3º Halving): 6.25 BTC*
    - *2024 (4º Halving): 3.125 BTC*
  - *"Esto genera un shock de oferta inelástico: si la demanda global se mantiene o crece, una reducción súbita del 50% en el flujo de nuevas monedas ejerce presión alcista estructural sobre el precio."*
- **2. El RSI mensual de 14 periodos:**
  - *"El Índice de Fuerza Relativa (*Relative Strength Index*, RSI) desarrollado por J. Welles Wilder mide el momentum de las ganancias frente a las pérdidas en una ventana fija:"*
    $$\text{RSI} = 100 - \frac{100}{1 + RS}, \quad \text{donde } RS = \frac{\text{Media de subidas}}{\text{Media de bajadas}}$$
  - *"En velas de 1 hora o 1 día, el RSI produce decenas de señales falsas por el ruido diario. Pero al calcularlo sobre **velas mensuales**, cada barra condensa 30 días de mercado. Un ciclo completo de 4 años son apenas 48 barras mensuales, lo que convierte al RSI(14) en un termómetro macro de sobrecalentamiento y capitulación."*

### 2. Secuencia en Notebook: Datos y Remuestreo (`Celdas 0 y 1`) (3:00 - 5:00)
- **[JUPYTER NOTEBOOK EN PANTALLA COMPLETA]**
- *"Abrimos `AlgorithmicTrading/Backtesting/bitcoin_cycles.ipynb` en nuestro entorno Jupyter."*
- **Ejecutar Celda 0:**
  ```python
  import matplotlib.pyplot as plt
  import yfinance as yf
  import pandas as pd
  import numpy as np
  import pandas_ta as ta
  import datetime
  import matplotlib.dates as mdates
  ```
- **Ejecutar Celda 1:** *"Descargamos los datos y realizamos el remuestreo mensual:"*
  ```python
  symbol = yf.Ticker('BTC-USD')
  start_date = datetime.datetime.fromtimestamp(1410912000) # Septiembre 2014
  end_date = datetime.datetime.now()
  df = symbol.history(start=start_date, end=end_date)
  df = df[['Open', 'High', 'Low', 'Close']].rename(...)
  df = df.resample('1M').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'})
  df.ta.rsi(length=14, append=True)
  ```
  - **Detalle técnico visible en pantalla:** *"Observa la advertencia de pandas en la salida:"*
    `FutureWarning: 'M' is deprecated and will be removed in a future version, please use 'ME' instead.`
    *"Es un aviso menor de las versiones modernas de pandas: en versiones futuras '1M' se sustituye por '1ME' (Month End), pero funciona perfectamente."*
  - **Resultado en pantalla:** DataFrame con más de 120 filas mensuales con Open, High, Low, Close y la nueva columna `RSI_14`.

### 3. Renderizado del Gráfico de Estilo Oscuro (`Celda 2`) (5:00 - 7:30)
- **[JUPYTER NOTEBOOK - CELDA 2]**
- *"Ahora ejecutamos la **Celda 2**, que contiene la lógica de renderizado visual profesional."*
- *"Analicemos la arquitectura del gráfico:"*
  - **Paleta de tema oscuro:**
    ```python
    BG_COLOR = '#1a1a1a'       # Gris grafito oscuro
    AXES_COLOR = '#212121'     # Contenedor interior
    PRIMARY_COLOR = '#00BFFF'  # Azul eléctrico para el precio de Bitcoin
    SECONDARY_COLOR = '#FFD700'# Dorado para el RSI
    RED_COLOR = '#FF5252'      # Rojo para sobrecompra extrema
    GREEN_COLOR = '#00C853'    # Verde para sobreventa macro
    ```
  - **Dimensiones:** `fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12), sharex=True, gridspec_kw={'height_ratios': [3, 1]})`. Damos el 75% del espacio vertical al precio y el 25% al oscilador.
  - **Escala logarítmica:** en el eje Y del precio (`ax1.set_yscale('log')`). Esto es indispensable: en un activo que pasa de 300 a 70.000 USD, una escala lineal aplastaría los primeros ciclos haciéndolos invisibles.

### 4. Lectura Cuantitativa del Gráfico (7:30 - 9:30)
- **[ZOOM EN EL GRÁFICO GENERADO]**
- *"Observemos lo que revela el gráfico resultante:"*
- **1. Las líneas verticales de los Halvings:**
  - *"Las marcas verticales punteadas señalan los momentos exactos de reducción de recompensa: julio de 2016, mayo de 2020 y abril de 2024."*
  - *"Históricamente, la fase verdaderamente explosiva del ciclo no ocurre el día del halving, sino entre 6 y 18 meses después, cuando la reducción acumulada del flujo diario de monedas choca contra la demanda del mercado."*
- **2. Los umbrales del RSI Mensual:**
  - *"El script define dos umbrales empíricos clave:"*
    `OVERBOUGHT_THRESHOLD = 85` | `OVERSOLD_THRESHOLD = 47`
  - **La zona roja (RSI > 85):** *"En los picos de 2013, 2017 y el primer pico de 2021, el RSI mensual penetró con fuerza por encima de 85-90. Marca momentos de euforia extrema donde el mercado está históricamente sobreextendido."*
  - **La zona verde (RSI < 47):** *"Durante los fondos de los inviernos cripto (finales de 2015, finales de 2018 y finales de 2022), el RSI mensual cayó a la zona de 45-47. Históricamente, cada vez que el RSI mensual visitó esa franja, el precio se encontraba en su suelo de ciclo de acumulación a largo plazo."*

### 5. Advertencias Críticas: Muestra N=4 y Rendimientos Decrecientes (9:30 - 11:45)
- **[DIAPOSITIVA DE ADVERTENCIA / CÁMARA]**
- *"Como analistas cuantitativos, es nuestro deber no caer en el fanatismo del gráfico. Miremos las limitaciones científicas de este modelo:"*
- **Limitación 1: Tamaño muestral insignificante ($N = 4$)**
  - *"En estadística, una muestra de 4 eventos no permite extraer conclusiones con significancia estadística. Que Bitcoin haya repetido un patrón cuatro veces no demuestra una ley inmutable de la física. Cualquier choque macroeconómico global (recesiones, tipos de interés elevados, eventos geopolíticos) puede desacoplar el precio del ciclo del halving."*
- **Limitación 2: Rendimientos decrecientes (*Diminishing Returns*)**
  - *"En el ciclo 2011-2013 el multiplicador de fondo a techo fue de más de 500x. En 2015-2017 fue de ~100x. En 2018-2021 fue de ~20x. A medida que la capitalización de mercado escala hacia el billón de dólares, mover el precio requiere flujos de liquidez exponencialmente mayores."*
- **Limitación 3: La transformación estructural de los ETFs Institucionales**
  - *"El ciclo actual inauguró la era de los ETFs spot de Bitcoin de BlackRock, Fidelity y otros gigantes. La demanda ya no está impulsada primordialmente por usuarios minoristas con exchanges offshore, sino por asignaciones de carteras institucionales vinculadas al ciclo de liquidez global de los bancos centrales."*

### 6. Conclusión y Llamada a la Acción (CTA) (11:45 - 13:00)
- **[CÁMARA]**
- *"Tienes el código completo de `bitcoin_cycles.ipynb` en la carpeta `AlgorithmicTrading/Backtesting/` del repositorio de GitHub enlazado abajo."*
- *"Si quieres dominar el análisis cuantitativo de series temporales, modelado estocástico y ciencia de datos en Python y R, revisa el enlace a mi curso completo de Udemy que tienes en la descripción con precio preferente."*
- *"Y si este tipo de análisis técnico sin humo te resulta útil, dale 'Me gusta', suscríbete y considera unirte como miembro del canal para acceder a análisis y código exclusivo."*
- *"Pregunta para la comunidad: ¿crees que los ciclos de 4 años seguirán dictando el ritmo de Bitcoin, o la liquidez macro y los ETFs han roto el patrón para siempre? ¡Deja tu opinión en los comentarios y nos vemos en el próximo video!"*
