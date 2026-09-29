# Guion de Video: DeepSeek-R1 local con Ollama (Razonamiento en tu máquina)

- **Duración estimada:** 9 minutos 45 segundos (rango objetivo: 7 - 12 minutos).
- **Tema:** Ejecución 100% local del modelo de razonamiento DeepSeek-R1 (versión destilada de 1.5B y 7B) usando Ollama, configuración de parámetros y uso interactivo/API.
- **Público objetivo:** Desarrolladores, estudiantes y entusiastas de la IA que buscan privacidad, coste cero por token y comprensión de la cadena de pensamiento (*Chain-of-Thought*).
- **Material de apoyo en repo:** `DeepSeekTutorial-DistiledR1/OllamaTutorial.md` y `contenido/deepseek-r1-local/hallazgos.md`.

---

## Tabla de Tiempos y Estructura

| Bloque | Minuto inicio | Minuto fin | Duración | Descripción |
|---|---|---|---|---|
| 1. Gancho y propuesta de valor | 0:00 | 0:45 | 0:45 | Razonamiento tipo o1/o3 totalmente gratis y privado en tu ordenador. |
| 2. ¿Qué es DeepSeek-R1 y qué modelo elegir? | 0:45 | 2:15 | 1:30 | Modelos destilados (1.5B, 7B, 14B), RAM requerida y precisión numérica. |
| 3. Instalación limpia de Ollama en Linux/Mac/Win | 2:15 | 3:45 | 1:30 | Instalación oficial, verificación del driver NVIDIA sin bloatware. |
| 4. Primera ejecución y observación del razonamiento | 3:45 | 5:30 | 1:45 | `ollama run deepseek-r1:1.5b`, descarga y análisis del bloque `<think>`. |
| 5. Cómo ajustar parámetros de verdad en Ollama | 5:30 | 7:15 | 1:45 | Por qué no existen flags en CLI; uso de `/set parameter` y `Modelfile`. |
| 6. Integración rápida vía API local con Python/curl | 7:15 | 8:45 | 1:30 | Consumo del endpoint HTTP en `localhost:11434` con streaming. |
| 7. Conclusión y Llamada a la Acción (CTA) | 8:45 | 9:45 | 1:00 | Repo con código, curso Udemy, membresía y debate en comentarios. |

---

## Tabla de Pantallas y Elementos Visuales

| Bloque | Tipo de plano | Elemento en pantalla | Apoyo gráfico / Texto sobreimpreso |
|---|---|---|---|
| 1 | Cámara + Plano medio | Presentador con terminal visible de fondo | "DeepSeek-R1 en tu PC: 0€ por token y 100% privado" |
| 2 | Gráfica comparativa | Tabla de tamaños de modelo vs. VRAM requerida | 1.5B (1.1 GB RAM), 7B (4.7 GB VRAM), 14B (9 GB VRAM) |
| 3 | Terminal en pantalla completa | Comandos `nvidia-smi` y `curl -fsSL https://ollama.com/install.sh \| sh` | Letras grandes (20pt), resaltado de sintaxis |
| 4 | Terminal en directo | Prompt interactivo de Ollama con respuesta en streaming | Resaltar en color ámbar las etiquetas `<think>` y `</think>` |
| 5 | Editor de código / Terminal | Archivo `Modelfile` con directivas `PARAMETER` | Cartel rojo: "Error común: los flags `--temperature` en la CLI no existen" |
| 6 | Terminal + Script Python | Llamada `curl` y mini script en Python con `requests` | Respuesta JSON con tokens y tiempo de evaluación |
| 7 | Cámara + Pantalla final | Presentador despidiendo el video | Tarjetas interactivas hacia el curso de Udemy y el botón de suscripción |

---

## Guion Detallado (Locución y Acciones)

### 1. Gancho y propuesta de valor (0:00 - 0:45)
- **[CÁMARA]**
- *"Los modelos de razonamiento como o1 o o3 han cambiado las reglas del juego: piensan antes de responder, se autocorrigen y resuelven problemas de lógica complejos paso a paso. Pero pagar suscripciones caras o enviar los datos confidenciales de tu empresa a la nube de terceros no siempre es una opción."*
- *"Hoy vas a aprender a instalar y correr **DeepSeek-R1** completamente gratis y en local en tu propio ordenador utilizando **Ollama**. Sin límites, sin APIs de pago y con la garantía de que tus datos jamás salen de tu máquina."*

### 2. ¿Qué es DeepSeek-R1 y qué modelo elegir? (0:45 - 2:15)
- **[TABLA EN PANTALLA]**
- *"Antes de tocar una sola línea de comandos, es vital entender qué modelo vamos a bajar. El modelo original de DeepSeek-R1 tiene 671 mil millones de parámetros y requiere un centro de datos. Pero el equipo de DeepSeek destiló ese razonamiento en arquitecturas más compactas basadas en Qwen y Llama."*
- *"Para tu ordenador personal tienes opciones fantásticas:"*
  - **1.5B** (~1.1 GB de descarga): corre prácticamente en cualquier laptop moderna, incluso solo con CPU y 8 GB de RAM. *(Ojo: son 1.500 millones de parámetros, mil millones, no un billón en español).*
  - **7B** (~4.7 GB): basado en Qwen 2.5, ideal si tienes una tarjeta gráfica de 6 u 8 GB como una RTX 3060 o una RTX 4050.
  - **14B** o **32B**: si cuentas con una GPU de 12 a 24 GB de VRAM.
- *"En este tutorial vamos a usar la versión de **1.5B** para que cualquier persona pueda reproducirlo ahora mismo, pero el comando es idéntico para cualquiera de las variantes."*

### 3. Instalación de Ollama (2:15 - 3:45)
- **[TERMINAL COMPLETA]**
- *"Si tienes GPU NVIDIA en Linux, asegúrate primero de que el controlador esté funcionando ejecutando:"*
  ```bash
  nvidia-smi
  ```
- *"Nota importante: **no** necesitas instalar los paquetes gigantes del CUDA Toolkit de desarrollo (`nvidia-cuda-toolkit`). Ollama ya incluye internamente las librerías aceleradas de cálculo y detecta automáticamente tu GPU a través del driver del sistema."*
- *"Para instalar Ollama en Linux, usamos el script oficial de su dominio actual (`ollama.com`):"*
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```
  *(Si estás en Windows o macOS, simplemente descargas el instalador gráfico desde `ollama.com`).*
- *"Comprobamos que el servicio está activo:"*
  ```bash
  ollama -v
  ```

### 4. Primera ejecución y observación del razonamiento (3:45 - 5:30)
- **[TERMINAL EN DIRECTO]**
- *"Descargar y arrancar el modelo se hace en un único comando:"*
  ```bash
  ollama run deepseek-r1:1.5b
  ```
- *"Ollama comprueba si tienes el modelo; como es la primera vez, descargará el archivo de aproximadamente 1.1 GB y abrirá un prompt interactivo `>>>`."*
- *"Vamos a poner a prueba su capacidad de razonamiento con un problema clásico de lógica:"*
  ```text
  >>> Una botella y un corcho cuestan 1.10 euros en total. La botella cuesta 1.00 euro más que el corcho. ¿Cuánto cuesta el corcho? Responde paso a paso.
  ```
- **[RESALTAR EN PANTALLA EL BLOQUE `<think>`]**
- *"Observa cómo lo primero que genera el modelo es un bloque etiquetado con `<think>` y `</think>`. Ese es el flujo de pensamiento (*Chain-of-Thought*). El modelo se plantea hipótesis, prueba valores (si el corcho valiera 10 céntimos, la botella costaría 1.10 y el total sería 1.20, por tanto se descarta), plantea la ecuación algebraica $x + (x + 1.00) = 1.10$, resuelve $x = 0.05$ euros y finalmente emite la respuesta limpia."*

### 5. Cómo ajustar parámetros de verdad en Ollama (5:30 - 7:15)
- **[EDITOR / TERMINAL]**
- *"Aquí viene un error muy extendido: en muchas guías no oficiales de internet verás comandos como `ollama run ... --temperature 0.7 --task text-generation`. Si pruebas eso en tu terminal, Ollama te dará un error inmediato: `unknown flag: --task`. Esos flags **no existen** en la CLI de Ollama."*
- *"¿Cómo se personaliza entonces el comportamiento del modelo?"*
- *"Tienes dos formas limpias:"*
  1. **Dentro de la sesión interactiva:** usa los comandos de control:
     ```text
     /set parameter temperature 0.6
     /set parameter top_p 0.95
     ```
  2. **Creando un `Modelfile`:**
     *"Creamos un archivo llamado `Modelfile`:"*
     ```dockerfile
     FROM deepseek-r1:1.5b
     PARAMETER temperature 0.6
     PARAMETER top_p 0.95
     SYSTEM "Eres un asistente técnico experto en Python y algoritmos matemáticos."
     ```
     *"Y generamos nuestro propio modelo empaquetado:"*
     ```bash
     ollama create mi-deepseek -f Modelfile
     ollama run mi-deepseek
     ```

### 6. Integración mediante la API local de Ollama (7:15 - 8:45)
- **[TERMINAL + EJEMPLO PYTHON]**
- *"Ollama no es solo una terminal: levanta por defecto un servidor HTTP REST en el puerto `11434`. Puedes consultarlo desde cualquier lenguaje."*
- *"Por ejemplo, con `curl`:"*
  ```bash
  curl http://localhost:11434/api/generate -d '{
    "model": "deepseek-r1:1.5b",
    "prompt": "Escribe una funcion en Python para calcular el factorial recursivo",
    "stream": false
  }'
  ```
- *"O en un script de Python en tres líneas con la librería oficial `ollama` (`pip install ollama`):"*
  ```python
  import ollama

  response = ollama.chat(model='deepseek-r1:1.5b', messages=[
      {'role': 'user', 'content': 'Explica en dos frases que es un puntero.'}
  ])
  print(response['message']['content'])
  ```
- *"Esto te permite integrar razonamiento profundo en tus aplicaciones sin gastar un céntimo en cuotas de API."*

### 7. Conclusión y Llamada a la Acción (CTA) (8:45 - 9:45)
- **[CÁMARA]**
- *"Tienes todos los comandos, el `Modelfile` y los ejemplos de código organizados en la carpeta del repositorio de GitHub que te enlazo en la descripción."*
- *"Si quieres dominar el análisis de datos y cómo conectar estos modelos con ciencia de datos real en Python y R, revisa el enlace a mi curso completo de Udemy que tienes abajo con cupón de descuento."*
- *"No olvides pulsar el botón 'Unirme' en el canal si quieres apoyar la producción de estos tutoriales técnicos en profundidad."*
- *"Cuéntame en los comentarios: ¿has probado ya la versión de 7B o 14B de DeepSeek-R1? ¿Qué tal ha respondido en tu tarjeta gráfica? ¡Deja tu comentario y nos vemos en el próximo video!"*
