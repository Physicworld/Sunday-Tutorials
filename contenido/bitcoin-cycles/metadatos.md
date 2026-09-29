# Metadatos de Publicación: Ciclos de Bitcoin y RSI Mensual

Configuración de metadatos para el video largo y sus dos Shorts asociados, validada para `tools/render_metadata.py` y las plantillas de `docs/youtube/` (`es_trading = true`).

---

## 1. Video Largo

### Ficha técnica y Miniatura (según `miniatura-spec.md`)
- **Título definitivo (67 caracteres):** `Cómo analizar los ciclos de Bitcoin en Python con tema oscuro y RSI`
  *(Fórmula 1 de `formulas-titulo.md`: Cómo + resultado + herramienta).*
- **Miniatura:**
  - Resolución: 1280 x 720 px (16:9), PNG.
  - Fondo: Gris grafito oscuro (`#1a1a1a`).
  - Elemento visual: El gráfico del notebook de dos paneles con la curva de precio azul eléctrico (`#00BFFF`), las líneas verticales de los Halvings y el oscilador RSI dorado (`#FFD700`).
  - Texto (3 palabras, legible en móvil): **"CICLOS DE BITCOIN"** con "CICLOS DE" en blanco roto y "BITCOIN" en dorado neón (`#FFD700`).
  - Esquina inferior derecha despejada para el indicador de duración de YouTube.

### Archivo de datos TOML (`datos-largo.toml`)

```toml
titulo = "Cómo analizar los ciclos de Bitcoin en Python con tema oscuro y RSI"
resumen = "Aprende a analizar cuantitativamente los ciclos cuatrienales de Bitcoin en Python. Descargamos datos históricos con yfinance, remuestreamos a velas mensuales, calculamos el RSI de 14 periodos y renderizamos un gráfico profesional en tema oscuro con las fechas exactas de halving y zonas macro de acumulación."

capitulos = [
  "0:00 Aviso legal y el misterio del reloj de 4 años",
  "1:15 Matemática del Halving (shock de oferta) y el RSI mensual",
  "3:00 Descarga de datos históricos con yfinance y remuestreo mensual",
  "5:00 Configuración visual profesional: tema oscuro y escala logarítmica",
  "7:30 Lectura cuantitativa: techos de ciclo en RSI 85 y suelos en RSI 47",
  "9:30 Advertencias críticas: muestra pequeña N=4 y el impacto de los ETFs",
  "11:45 Conclusiones, código en GitHub y debate en comentarios",
]

codigo_url = "https://github.com/Physicworld/Sunday-Tutorials/tree/main/AlgorithmicTrading/Backtesting"
herramientas = [
  "Python 3.11+",
  "pandas",
  "pandas_ta",
  "yfinance",
  "matplotlib",
]
es_trading = true
hashtags = [
  "#Bitcoin",
  "#Cripto",
  "#Python",
  "#DataScience",
  "#FinanzasCuantitativas",
]

pregunta = "¿Crees que los ciclos de 4 años seguirán dictando el ritmo de Bitcoin o los ETFs institucionales han cambiado la estructura del mercado? ¡Déjame tu opinión abajo!"
```

### Comando para renderizar
```bash
python tools/render_metadata.py \
  --template docs/youtube/plantilla-descripcion-larga.md \
  --data docs/youtube/enlaces.toml \
  --data contenido/bitcoin-cycles/datos-largo.toml \
  --allow-todo > descripcion_larga.txt
```

---

## 2. Metadatos de Shorts

### Short 1: El reloj de 4 años de Bitcoin en Python
- **Título:** `El reloj de 4 años de Bitcoin en Python #Shorts` (49 caracteres)
- **Gancho:** ¿Por qué Bitcoin se mueve en un ciclo de 4 años casi matemático? Te lo explico con Python.
- **Archivo de datos (`datos-short-1.toml`):**
  ```toml
  titulo = "El reloj de 4 años de Bitcoin en Python #Shorts"
  gancho = "¿Por qué Bitcoin se mueve en un ciclo de 4 años casi matemático? Te lo explico con datos en Python."
  video_largo_url = "TODO_LINK"
  codigo_url = "https://github.com/Physicworld/Sunday-Tutorials/tree/main/AlgorithmicTrading/Backtesting"
  es_trading = true
  hashtags = ["#Shorts", "#Bitcoin", "#Python", "#Halving", "#Cripto"]
  ```

### Short 2: El indicador mensual que detecta techos en Bitcoin
- **Título:** `El indicador mensual que detecta techos en Bitcoin #Shorts` (58 caracteres)
- **Gancho:** Si filtras el ruido diario con velas mensuales, este indicador revela los techos históricos de Bitcoin.
- **Archivo de datos (`datos-short-2.toml`):**
  ```toml
  titulo = "El indicador mensual que detecta techos en Bitcoin #Shorts"
  gancho = "Si filtras el ruido diario con velas mensuales, este indicador revela los techos históricos de Bitcoin."
  video_largo_url = "TODO_LINK"
  codigo_url = "https://github.com/Physicworld/Sunday-Tutorials/tree/main/AlgorithmicTrading/Backtesting"
  es_trading = true
  hashtags = ["#Shorts", "#Trading", "#Bitcoin", "#RSI", "#Finanzas"]
  ```
