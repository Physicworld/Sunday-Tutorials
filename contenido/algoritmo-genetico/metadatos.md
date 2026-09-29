# Metadatos de Publicación: Algoritmo Genético Visual con Matplotlib

Configuración de metadatos para el video largo y sus dos Shorts asociados, validada para su procesamiento mediante `tools/render_metadata.py` y las plantillas de `docs/youtube/`.

---

## 1. Video Largo

### Ficha técnica y Miniatura (según `miniatura-spec.md`)
- **Título definitivo (76 caracteres):** `Algoritmo genético desde cero en Python: mira cómo evoluciona una recta`
  *(Fórmula 5 de `formulas-titulo.md`: Construye X desde cero + resultado visual).*
- **Miniatura:**
  - Resolución: 1280 x 720 px (16:9), PNG.
  - Fondo: Negro / azul muy oscuro (`#0D1117`).
  - Elemento visual: El Subplot 2 de Matplotlib en grande con los puntos azules dispersos, la recta roja óptima y varias rectas verdes translúcidas convergiendo.
  - Texto (3 palabras, legible en móvil): **"CÓDIGO QUE EVOLUCIONA"** con "CÓDIGO QUE" en blanco y "EVOLUCIONA" resaltado en cian neón (`#00E5FF`).
  - Esquina inferior derecha despejada para el indicador de duración de YouTube.

### Archivo de datos TOML (`datos-largo.toml`)

```toml
titulo = "Algoritmo genético desde cero en Python: mira cómo evoluciona una recta"
resumen = "Aprende qué es y cómo programar un algoritmo genético desde cero en Python con NumPy y Matplotlib. Vemos en tiempo real cómo una población de rectas evoluciona y converge para ajustar una nube de datos sin usar derivadas ni cálculo diferencial."

capitulos = [
  "0:00 La naturaleza como optimizador",
  "1:30 Codificación del individuo (Genotipo y Fenotipo)",
  "3:00 Función de Fitness y cálculo de error cuadrático",
  "4:30 Operadores genéticos: Mutación y Cruce línea a línea",
  "6:30 El bucle evolutivo y el elitismo estricto",
  "8:00 Demo animada: Caos, convergencia y estabilidad en 3 subplots",
  "10:15 Hiperparámetros, límites teóricos y cuándo usarlo",
  "11:30 Código en el repo, recursos y reto en comentarios",
]

codigo_url = "https://github.com/Physicworld/Sunday-Tutorials/tree/main/Heuristics"
herramientas = [
  "Python 3.11+",
  "NumPy",
  "Matplotlib (animación interactiva con plt.ion)",
]
es_trading = false
hashtags = [
  "#Python",
  "#AlgoritmosGeneticos",
  "#Matplotlib",
  "#InteligenciaArtificial",
  "#Programacion",
]

pregunta = "¿Qué problema no lineal o complejo resolverías tú con un algoritmo genético en lugar de gradiente descendente? Deja tu respuesta abajo."
```

### Comando para renderizar descripción y comentario fijado
```bash
# Descripción larga (agrega repo_url y udemy_url desde enlaces.toml):
python tools/render_metadata.py \
  --template docs/youtube/plantilla-descripcion-larga.md \
  --data docs/youtube/enlaces.toml \
  --data contenido/algoritmo-genetico/datos-largo.toml \
  --allow-todo > descripcion_larga.txt

# Comentario fijado:
python tools/render_metadata.py \
  --template docs/youtube/comentario-fijado.md \
  --data docs/youtube/enlaces.toml \
  --data contenido/algoritmo-genetico/datos-largo.toml > comentario_fijado.txt
```

---

## 2. Metadatos de Shorts

### Short 1: Una población de rectas que aprende sola
- **Título:** `Una población de rectas que aprende sola #Shorts` (49 caracteres)
- **Gancho:** Una población de 1000 rectas al azar aprende a ajustar datos por pura selección natural.
- **Archivo de datos (`datos-short-1.toml`):**
  ```toml
  titulo = "Una población de rectas que aprende sola #Shorts"
  gancho = "Una población de 1000 rectas al azar aprende a ajustar datos por pura selección natural sin derivadas ni cálculo."
  video_largo_url = "TODO_LINK"
  codigo_url = "https://github.com/Physicworld/Sunday-Tutorials/tree/main/Heuristics"
  es_trading = false
  hashtags = ["#Shorts", "#Python", "#AlgoritmosGeneticos", "#Matplotlib", "#IA"]
  ```

### Short 2: De 14.000 de error a 100 en 3 segundos
- **Título:** `De 14.000 de error a 100 en 3 segundos #Shorts` (47 caracteres)
- **Gancho:** Mira cómo cae el error de un algoritmo genético de 14.000 a 100 en apenas 20 generaciones en Python.
- **Archivo de datos (`datos-short-2.toml`):**
  ```toml
  titulo = "De 14.000 de error a 100 en 3 segundos #Shorts"
  gancho = "Mira cómo cae el error de un algoritmo genético de 14.000 a 100 en apenas 20 generaciones en Python."
  video_largo_url = "TODO_LINK"
  codigo_url = "https://github.com/Physicworld/Sunday-Tutorials/tree/main/Heuristics"
  es_trading = false
  hashtags = ["#Shorts", "#Python", "#DataScience", "#Animacion", "#Matplotlib"]
  ```
