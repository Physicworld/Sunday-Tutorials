# Guion de Video: Algoritmo Genético Visual en Python con Matplotlib

- **Duración estimada:** 12 minutos 15 segundos (rango objetivo: 10 - 14 minutos).
- **Tema:** Programación desde cero de un algoritmo genético en Python para regresión lineal continua, con visualización animada en 3 subplots sincronizados en tiempo real mediante Matplotlib.
- **Público objetivo:** Desarrolladores, estudiantes de computación e inteligencia artificial y entusiastas de heurísticas evolutivas que buscan entender la selección natural aplicada al código con feedback visual instantáneo.
- **Archivo fuente del repositorio:** `Heuristics/GA.py` (150 líneas, intocado).

---

## Tabla de Tiempos y Estructura

| Bloque | Minuto inicio | Minuto fin | Duración | Descripción |
|---|---|---|---|---|
| 1. Gancho e intuición evolutiva | 0:00 | 1:30 | 1:30 | La naturaleza como optimizador: qué es un algoritmo genético sin jerga innecesaria. |
| 2. Codificación del individuo en código | 1:30 | 3:00 | 1:30 | La clase `Individual` (`GA.py:8-12` y `31-32`), genotipo vs. fenotipo. |
| 3. Función de fitness y evaluación | 3:00 | 4:30 | 1:30 | Cálculo del error cuadrático `compute_fitness` (`GA.py:13-15`) y minimización. |
| 4. Operadores genéticos: Mutación y Cruce | 4:30 | 6:30 | 2:00 | `mutate` (`GA.py:17-22`) y `crossover` (`GA.py:23-30`) línea a línea. |
| 5. Selección, elitismo y el bucle principal | 6:30 | 8:00 | 1:30 | Función `genetic_algorithm` (`GA.py:34-82`), selección por orden y mejor global. |
| 6. Demo: La animación en vivo en 3 pantallas | 8:00 | 10:15 | 2:15 | `plt.ion()`, 3 subplots (`GA.py:92-127`), qué pasa en generaciones 0-5, 5-50 y 50-500. |
| 7. Hiperparámetros, límites y cuándo usarlo | 10:15 | 11:30 | 1:15 | Ajuste de tasas, detalle de `num_generations` vs. loop, y GA frente a OLS / gradiente. |
| 8. Conclusión y Llamada a la Acción (CTA) | 11:30 | 12:15 | 0:45 | Repositorio GitHub, curso en Udemy, membresía y reto para la comunidad. |

---

## Tabla de Pantallas y Elementos Visuales

| Bloque | Tipo de plano | Elemento en pantalla | Apoyo gráfico / Texto sobreimpreso |
|---|---|---|---|
| 1 | Cámara + Ventana flotante | Presentador a la izquierda; a la derecha, primeros segundos de la animación de `GA.py` corriendo | "Optimización evolutiva: código que aprende solo" |
| 2 | Editor (VS Code / Neovim) | `Heuristics/GA.py:8-32` resaltado con tipografía grande (18pt) | Esquema: Genotipo `[m, b]` → Fenotipo: Recta $y = mx + b$ |
| 3 | Editor + Fórmula matemática | Líneas 13-15 de `GA.py` + render LaTeX de la función de coste | $\text{Fitness} = \sum_{i=1}^N (y_i - (m x_i + b))^2$ |
| 4 | Editor en pantalla dividida | Líneas 17-22 (`mutate`) a la izquierda; líneas 23-30 (`crossover`) a la derecha | Diagrama esquemático de intercambio cromosómico |
| 5 | Editor de código | Líneas 58-82 de `GA.py`: ordenación `sorted(..., reverse=False)[:best_size]` | Esquema de flujo: Población → Evaluar → Ordenar → Cruzar → Mutar |
| 6 | Ventana gráfica (Matplotlib) | Ventana interactiva maximizada (1920x1080) con los 3 subplots actualizándose en vivo | Resaltadores: Subplot 1 (Fitness), Subplot 2 (Rectas), Subplot 3 (Mapa de calor) |
| 7 | Diapositiva comparativa | Tabla de algoritmos: OLS vs. Descenso de Gradiente vs. Algoritmos Genéticos | "¿Cuándo usar un Algoritmo Genético?" (No diferenciabilidad, espacios multimodales) |
| 8 | Cámara + Pantalla final | Presentador despidiendo con enlaces en pantalla | Enlace al repo, curso de Udemy y botón "Unirme" |

---

## Guion Detallado (Locución y Acciones)

### 1. Gancho e intuición evolutiva (0:00 - 1:30)
- **[CÁMARA CON ANIMACIÓN FLOTANTE]**
- *"Imagina que tienes una nube de datos dispersos y quieres encontrar la recta matemática que mejor los describe, pero no conoces el cálculo diferencial, no tienes matrices para mínimos cuadrados y no puedes calcular derivadas. ¿Cómo lo resolverías?"*
- *"La naturaleza resolvió este problema hace miles de millones de años mediante la evolución: creas una población de soluciones aleatorias, pruebas cuáles funcionan mejor, te quedas con las mejores, las cruzas entre sí, aplicas pequeñas mutaciones al azar y repites el proceso generación tras generación."*
- *"En este tutorial vamos a destripar línea por línea el archivo `Heuristics/GA.py` de nuestro repositorio. Programaremos un algoritmo genético continuo en Python y veremos en pantalla, en tiempo real con Matplotlib, cómo una población de rectas caóticas aprende y converge hacia el ajuste perfecto de los datos en apenas unos segundos."*

### 2. Codificación del individuo en código (`GA.py:8-32`) (1:30 - 3:00)
- **[EDITOR DE CÓDIGO - LÍNEAS 8-32]**
- *"Vamos al código fuente en `Heuristics/GA.py`. Todo algoritmo genético parte de una representación del individuo: el cromosoma."*
- *"En la línea 8 definimos la clase `Individual`:"*
  ```python
  class Individual:
      def __init__(self, gene_length):
          self.genes = [random.random() for _ in range(gene_length)]
          self.fitness = 0
  ```
- *"Observa la elegancia de la abstracción:"*
  - *"El **genotipo** es simplemente una lista de números flotantes aleatorios entre 0 y 1 (`self.genes`). Como buscamos una recta en el plano $y = m \cdot x + b$, nuestra longitud genética (`gene_length`) es 2: el primer gen representa la pendiente $m$ y el segundo representa el término independiente $b$."*
  - *"El **fenotipo** es la recta geométrica concreta que ese individuo proyecta en el plano, como vemos en el método `__repr__` de la línea 31: `y = {self.genes[0]}x + {self.genes[1]}`."*

### 3. Función de fitness y evaluación (`GA.py:13-15`) (3:00 - 4:30)
- **[EDITOR DE CÓDIGO + ESQUEMA VISUAL]**
- *"Para que la selección natural funcione, el entorno debe recompensar a los individuos adaptados y penalizar a los incompetentes. A eso lo llamamos función de **fitness** o aptitud."*
- *"Miremos las líneas 13 a 15 de `GA.py`:"*
  ```python
  def compute_fitness(self, data_x, data_y):
      m, b = self.genes
      self.fitness = sum([(y - (m * x + b)) ** 2 for x, y in zip(data_x, data_y)])
  ```
- *"Aquí calculamos la suma del error al cuadrado (*Sum of Squared Errors*, SSE) entre cada punto real $(x, y)$ y la predicción de la recta $m \cdot x + b$."*
- *"Punto clave a notar: en este diseño, **un menor fitness significa un mejor individuo**. Si la recta pasa exactamente por todos los puntos, el error sería cero. Cuanto más alejada esté la recta de los puntos, mayor será su fitness y peor será su calidad."*

### 4. Operadores genéticos: Mutación y Cruce (`GA.py:17-30`) (4:30 - 6:30)
- **[EDITOR - PANTALLA DIVIDIDA CON MUTATE Y CROSSOVER]**
- *"Ahora necesitamos los motores de la variabilidad biológica: la mutación y la recombinación genética."*
- *"En la línea 17 tenemos el método `mutate`:"*
  ```python
  def mutate(self, mutation_rate):
      rand = random.random()
      if rand < mutation_rate:
          gene_to_mutate = random.randint(0, len(self.genes) - 1)
          self.genes[gene_to_mutate] += random.uniform(-1, 1)
  ```
  *"Si un número aleatorio es menor que la tasa de mutación (definida en 0.5), seleccionamos al azar uno de los genes y le sumamos una perturbación continua uniforme en el rango $[-1, 1]$. Esto permite que los genes salgan del rango inicial $[0, 1)$ y exploren pendientes o cortes negativos o mayores que 1."*
- *"En la línea 23 encontramos el `crossover`:"*
  ```python
  def crossover(self, other_, crossover_rate):
      rand = random.random()
      if rand < crossover_rate:
          other = copy.deepcopy(other_)
          gene_to_cross = random.randint(0, len(self.genes) - 1)
          self.genes[gene_to_cross] = other.genes[gene_to_cross]
  ```
  *"Con una probabilidad dada por `crossover_rate`, el individuo copia un gen de otro individuo de la población (`other_`). Esto mezcla los aciertos de dos candidatos prometedores."*

### 5. Selección, elitismo y el bucle principal (`GA.py:34-82`) (6:30 - 8:00)
- **[EDITOR - LÍNEAS 34 A 82]**
- *"Bajamos a la función principal `genetic_algorithm`. Se inicializa una población de 1000 individuos (línea 53) y se guarda el mejor individuo global (línea 49)."*
- *"Veamos qué ocurre en cada iteración del bucle:"*
  1. **Evaluación (líneas 61-62):** *"Se calcula el fitness de cada uno de los 1000 individuos contra los datos de prueba generados en la línea 138-139 ($Y = 2X + 3 + \text{ruido}$)."*
  2. **Selección por truncamiento (línea 65):**
     ```python
     best_population = sorted(population, key=lambda x: x.fitness, reverse=False)[:best_size].copy()
     ```
     *"Ordenamos ascendentemente y nos quedamos con los 100 mejores (`best_size=100`, el top 10%)."*
  3. **Reproducción (líneas 68-70):** *"Cada individuo de la población se cruza con un padre elegido al azar de esa élite."*
  4. **Mutación (líneas 73-74):** *"Cada individuo tiene posibilidad de mutar."*
  5. **Elitismo estricto (líneas 76-80):** *"Comparamos el mejor de la generación con `global_best_individual`. Si el nuevo es mejor, lo adoptamos. ¡Nunca perdemos la mejor solución encontrada!"*

### 6. Demo: La animación en vivo en 3 pantallas (`GA.py:56, 92-127`) (8:00 - 10:15)
- **[MATPLOTLIB MAXIMIZADO - EJECUTANDO EN VIVO]**
- *"Ahora ejecutamos `python Heuristics/GA.py`. Activamos el modo interactivo con `plt.ion()` en la línea 48 y creamos una figura con 3 subplots verticales (`fig, ax = plt.subplots(3, 1)`). Observa la pantalla dividida en tres historias simultáneas:"*
- **Fase 1: El caos inicial (Generaciones 0 a 5)**
  - *"Subplot 1 (Arriba - Fitness): el error arranca en más de 13.000 unidades. En solo 3 generaciones se desploma en caída libre por debajo de 500."*
  - *"Subplot 2 (Centro - Datos vs. Mejor Individuo): los puntos azules son los datos reales ($y = 2x + 3$). En la generación 0, la recta roja está completamente torcida y las 9 líneas verdes (individuos aleatorios de la muestra) apuntan en direcciones absurdas. Pero casi instantáneamente, la recta roja gira como la manecilla de un reloj y se alinea con la diagonal de los datos."*
  - *"Subplot 3 (Abajo - Mapa de Fitness): los primeros puntos dispersos en el espacio $(m, b)$ se van tiñendo con el colormap `viridis`, del morado al verde."*
- **Fase 2: Ajuste fino y convergencia (Generaciones 5 a 50)**
  - *"Subplot 1: la curva de pérdida se aplana en forma de 'L' asintótica alrededor de 103-105."*
  - *"Subplot 2: la recta roja ya es prácticamente idéntica a los datos. El cuadro de texto superior izquierdo muestra `y = 2.01x + 2.98`. Fíjate cómo las líneas verdes translúcidas se agrupan en un haz estrecho alrededor de la roja: la población ha convergido genéticamente."*
  - *"Subplot 3: se forma una densa nube ovalada de puntos alrededor de las coordenadas $(m=2, b=3)$. El punto rojo central marca el campeón absoluto."*
- **Fase 3: Estabilidad en el ruido óptimo (Generaciones 50 a 500)**
  - *"La función de fitness oscila suavemente alrededor de 102.94. ¿Por qué no baja a cero? Porque generamos los datos con un ruido gaussiano de desviación estándar 1 sobre 100 puntos: la suma teórica esperada de los residuos es exactamente $100 \times 1^2 = 100$. ¡El algoritmo ha encontrado el mínimo global posible sin calcular ni una sola derivada!"*

### 7. Hiperparámetros, límites y cuándo usarlo (10:15 - 11:30)
- **[DIAPOSITIVA COMPARATIVA + CÓDIGO]**
- *"Tres observaciones cruciales para tu propia práctica:"*
  1. **Un detalle del código en la línea 58:** *"Fíjate que en la llamada de la línea 148 se pasa `num_generations=1000`, pero en el bucle de la línea 58 está escrito `for i in range(500):`. Es un detalle menor del script original, pero ilustra por qué a partir de la generación 80 el resultado ya es prácticamente óptimo."*
  2. **Sensibilidad a los hiperparámetros:** *"Si bajas `mutation_rate` a 0.05, el algoritmo se estancará si la población inicial no contiene buenos genes. Si lo subes a 0.99, la búsqueda se vuelve puro ruido browniano. El equilibrio del 0.5 con elitismo permite explorar y explotar simultáneamente."*
  3. **¿Cuándo usar algoritmos genéticos y cuándo NO?**
     - *"Para una regresión lineal simple, jamás usarías un algoritmo genético en producción: los mínimos cuadrados ordinarios (OLS) se resuelven en microsegundos de forma exacta con álgebra lineal, y el descenso de gradiente es mucho más eficiente."*
     - *"El verdadero poder de los algoritmos genéticos brilla cuando la función de coste es **discontinua, no derivable, con múltiples óptimos locales**, o cuando los parámetros son enteros o permutaciones (como el problema del viajante de comercio TSP o la optimización de hiperparámetros en trading)."*

### 8. Conclusión y Llamada a la Acción (CTA) (11:30 - 12:15)
- **[CÁMARA]**
- *"Tienes todo el código de `GA.py` y las instrucciones completas en la carpeta `Heuristics/` del repositorio de GitHub que te dejo en la descripción."*
- *"Si quieres dominar tanto los métodos heurísticos como el modelado estadístico riguroso y el machine learning en Python y R, revisa el enlace a mi curso de Udemy que tienes abajo con precio especial."*
- *"Para apoyar el desarrollo de más tutoriales de algoritmos visuales, haz clic en el botón 'Unirme' en la página de inicio del canal."*
- *"Y ahora te propongo un reto en los comentarios: si cambiamos la nube de puntos por una parábola cuadrática $y = a x^2 + b x + c$, ¿qué cambios mínimos tendrías que hacerle a la clase `Individual`? ¡Deja tu solución abajo y nos vemos en el próximo tutorial!"*
