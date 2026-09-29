# Metadatos de Publicación: Backtesting con Bandas de Bollinger

Configuración de metadatos para el video largo y sus dos Shorts asociados, validada para `tools/render_metadata.py` y las plantillas de `docs/youtube/` (`es_trading = true`).

---

## 1. Video Largo

### Ficha técnica y Miniatura (según `miniatura-spec.md`)
- **Título definitivo (61 caracteres):** `El error que arruina tu backtest en Python (y cómo evitarlo)`
  *(Fórmula 3 de `formulas-titulo.md`: Error común / mito).*
- **Miniatura:**
  - Resolución: 1280 x 720 px (16:9), PNG.
  - Fondo: Negro / gris muy oscuro (`#0D1117`).
  - Elemento visual: El mapa de calor 2D de Seaborn en tonos rojo/azul con la matriz de 200 combinaciones de Stop Loss y Take Profit.
  - Texto (3 palabras, legible en móvil): **"TU BACKTEST MIENTE"** con "TU" en blanco y "BACKTEST MIENTE" en amarillo neón (`#FFD600`).
  - Esquina inferior derecha despejada para el indicador de tiempo de YouTube.

### Archivo de datos TOML (`datos-largo.toml`)

```toml
titulo = "El error que arruina tu backtest en Python (y cómo evitarlo)"
resumen = "Analizamos una estrategia cuantitativa sobre Bitcoin aplicando Bandas de Bollinger sobre retornos logarítmicos. Optimizamos 200 combinaciones de Stop Loss y Take Profit en Python y destapamos las 3 trampas mortales: look-ahead bias, sobreajuste (overfitting) y costes de deslizamiento."

capitulos = [
  "0:00 Aviso legal y el mito del 1000% de rentabilidad",
  "1:00 Retornos logarítmicos vs. precios brutos en finanzas",
  "2:45 Descarga de datos con yfinance y cálculo de bandas",
  "4:30 El motor del Backtester: órdenes, balance y comisiones",
  "6:30 Grid Search: 200 combinaciones y 4 mapas de calor",
  "8:30 Win Rate vs. Retorno Asimétrico: la paradoja del 71%",
  "10:15 Las tres trampas mortales: Look-ahead bias, Overfitting y Slippage",
  "12:30 Conclusiones, recursos en GitHub y debate",
]

codigo_url = "https://github.com/Physicworld/Sunday-Tutorials/tree/main/AlgorithmicTrading/Backtesting"
herramientas = [
  "Python 3.11+",
  "pandas",
  "pandas_ta",
  "yfinance",
  "matplotlib / seaborn",
]
es_trading = true
hashtags = [
  "#Bitcoin",
  "#Backtesting",
  "#TradingAlgoritmico",
  "#Python",
  "#FinanzasCuantitativas",
]

pregunta = "¿Qué filtro o métrica utilizas tú para evitar el sobreajuste (overfitting) al evaluar una estrategia de trading? Cuéntamelo en los comentarios."
```

### Comando para renderizar
```bash
python tools/render_metadata.py \
  --template docs/youtube/plantilla-descripcion-larga.md \
  --data docs/youtube/enlaces.toml \
  --data contenido/backtesting-bollinger/datos-largo.toml \
  --allow-todo > descripcion_larga.txt
```

---

## 2. Metadatos de Shorts

### Short 1: El error de look-ahead que infla tu backtest
- **Título:** `El error de look-ahead que infla tu backtest #Shorts` (52 caracteres)
- **Gancho:** ¿Tu estrategia da 1000% de retorno? Probablemente tienes un sesgo de anticipación invisible en tu código.
- **Archivo de datos (`datos-short-1.toml`):**
  ```toml
  titulo = "El error de look-ahead que infla tu backtest #Shorts"
  gancho = "¿Tu estrategia da 1000% de retorno? Probablemente tienes un sesgo de anticipación invisible en tu código."
  video_largo_url = "TODO_LINK"
  codigo_url = "https://github.com/Physicworld/Sunday-Tutorials/tree/main/AlgorithmicTrading/Backtesting"
  es_trading = true
  hashtags = ["#Shorts", "#Trading", "#Python", "#Backtesting", "#Bitcoin"]
  ```

### Short 2: 71% de acierto y pierdes dinero
- **Título:** `71% de acierto y pierdes dinero: la trampa #Shorts` (49 caracteres)
- **Gancho:** Ganar el 71% de las operaciones puede arruinar tu cuenta si no vigilas la asimetría de los pagos.
- **Archivo de datos (`datos-short-2.toml`):**
  ```toml
  titulo = "71% de acierto y pierdes dinero: la trampa #Shorts"
  gancho = "Ganar el 71% de las operaciones puede arruinar tu cuenta si no vigilas la asimetría de los pagos."
  video_largo_url = "TODO_LINK"
  codigo_url = "https://github.com/Physicworld/Sunday-Tutorials/tree/main/AlgorithmicTrading/Backtesting"
  es_trading = true
  hashtags = ["#Shorts", "#Trading", "#Finanzas", "#Python", "#DataScience"]
  ```
