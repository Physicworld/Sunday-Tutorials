# Hallazgos técnicos y discrepancias: Guía de DeepSeek-R1 local con Ollama

Revisión técnica de `DeepSeekTutorial-DistiledR1/OllamaTutorial.md` frente a las versiones y recomendaciones oficiales actuales de Ollama y el catálogo de modelos de DeepSeek-R1.

> **Nota:** La guía original no se ha modificado directamente (tarea asignada a STQ-7). Este documento detalla cada discrepancia encontrada, su impacto práctico y la recomendación oficial con enlaces verificables.

---

## 1. Discrepancias críticas en la CLI de Ollama

### 1.1 Flags inexistentes en el comando `ollama run`
- **En la guía:** En el paso 5 ("Ejecutar un Modelo con Ollama") se incluye el siguiente comando:
  ```bash
  ollama run deepseek-r1:1.5b --task text-generation \
  --temperature 0.7 \
  --max-length 100 \
  --top_p 0.7
  ```
- **Estado actual:** El comando de la CLI de Ollama `ollama run` **NO admite** los flags `--task`, `--temperature`, `--max-length` ni `--top_p`.
- **Comportamiento real de la CLI:**
  Si un usuario ejecuta dicho comando, la CLI de Ollama se detiene inmediatamente con un error de parsing de argumentos:
  ```text
  Error: unknown flag: --task
  ```
- **Cómo se configuran realmente estos parámetros en Ollama:**
  En Ollama existen tres formas legítimas de ajustar hiperparámetros de inferencia:
  1. **Comandos interactivos dentro de la sesión de `ollama run`:**
     Una vez dentro del prompt interactivo:
     ```text
     /set parameter temperature 0.7
     /set parameter top_p 0.7
     ```
  2. **Creando un `Modelfile` personalizado:**
     ```dockerfile
     FROM deepseek-r1:1.5b
     PARAMETER temperature 0.7
     PARAMETER top_p 0.7
     PARAMETER num_predict 100
     ```
     y construyéndolo con `ollama create mi-deepseek -f Modelfile`. (Nota: en Ollama el equivalente a `max-length` se llama `num_predict`).
  3. **A través de la API REST local (`http://localhost:11434/api/generate` o `/api/chat`):**
     Pasando el objeto JSON `"options": {"temperature": 0.7, "top_p": 0.7, "num_predict": 100}`.
- **Fuente oficial:** [Ollama Modelfile Documentation](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values) y [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion).

---

## 2. Discrepancias en URLs y dominios oficiales

### 2.1 Dominio `ollama.ai` vs. `ollama.com`
- **En la guía:** Se indica `curl https://ollama.ai/install.sh | sh` y el enlace `https://ollama.ai`.
- **Estado actual:** A principios de 2024, el proyecto oficial migró de `ollama.ai` al dominio definitivo **`ollama.com`**.
  - Aunque `ollama.ai` mantiene una redirección HTTP 301 por compatibilidad, la documentación oficial, el script actual y los repositorios usan:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
- **Fuente oficial:** [Ollama Official Linux Installation](https://docs.ollama.com/linux).

---

## 3. Discrepancias en requisitos y dependencias de GPU

### 3.1 Instalación redundante del CUDA Toolkit (`nvidia-cuda-toolkit`)
- **En la guía:** El paso 3 indica instalar `sudo apt install nvidia-cuda-toolkit` (~2.5 GB a 4 GB en disco con dependencias de compiladores `nvcc`, headers, etc.).
- **Estado actual:** Para ejecutar Ollama con aceleración NVIDIA **NO es necesario instalar el CUDA Toolkit**.
  - Ollama distribuye sus propios binarios y librerías dinámicas de cómputo precompiladas (`libggml_cuda.so`) empaquetadas dentro de `/usr/lib/ollama/` o extraídas dinámicamente en tiempo de ejecución.
  - El único requisito del host es tener instalado el **controlador de kernel de NVIDIA** que proporcione la biblioteca del driver (`libcuda.so.1`), verificable mediante `nvidia-smi`.
  - Instalar `nvidia-cuda-toolkit` añade minutos de descarga innecesarios y riesgo de conflictos de versión entre el driver del kernel y las librerías del sistema en Ubuntu.
- **Fuente oficial:** [Ollama Linux Hardware Support](https://docs.ollama.com/linux#install-cuda-drivers-optional).

---

## 4. Precisión terminológica y variantes de DeepSeek-R1

### 4.1 Falso amigo lingüístico: "1 billón de parámetros"
- **En la guía:** Se indica textualmente: *"con una configuración de 1 billón de parámetros (1.5B)"*.
- **Corrección técnica:**
  - En la escala numérica larga (español), un **billón** es un millón de millones ($10^{12}$).
  - En la escala numérica corta (inglés estadounidense), un *billion* ($10^9$) equivale en español a **mil millones**.
  - El modelo `deepseek-r1:1.5b` tiene **1.500 millones de parámetros** (1,5 mil millones), no 1 billón de parámetros.
  - Llamarlo "1 billón" multiplica por mil el tamaño percibido del modelo y confunde a los estudiantes.

### 4.2 Catálogo completo de variantes disponibles
- **En la guía:** Solo se menciona `deepseek-r1:1.5b`.
- **Opciones reales en el registro de Ollama:**
  DeepSeek-R1 cuenta con modelos destilados basados en arquitecturas abiertas (Qwen y Llama) optimizados para razonamiento paso a paso (`<think>...</think>`):
  - `deepseek-r1:1.5b` (~1.1 GB, ideal para laptops sin GPU potente o CPU)
  - `deepseek-r1:7b` (~4.7 GB, basado en Qwen 2.5 7B, equilibrio ideal para GPUs de 6-8 GB como RTX 3060/4050/4060)
  - `deepseek-r1:8b` (~4.9 GB, basado en Llama 3.1 8B)
  - `deepseek-r1:14b` (~9.0 GB, para GPUs de 12-16 GB)
  - `deepseek-r1:32b` (~20 GB)
  - `deepseek-r1:70b` (~43 GB)
  - `deepseek-r1:671b` (el modelo fundacional MoE completo)
- **Fuente oficial:** [Ollama Library - DeepSeek-R1](https://ollama.com/library/deepseek-r1).

---

## 5. Estado de verificación práctica en este entorno

- **Entorno probado:**
  - GPU NVIDIA GeForce RTX 4050 Laptop GPU (6 GB VRAM) disponible y detectada con `nvidia-smi`.
  - Herramienta Ollama no preinstalada en el host del entorno de pruebas.
  - Se intentó descarga de usuario sin permisos sudo; se interrumpió para evitar saturación de ancho de banda y disco en el tiempo asignado al ticket.
  - **Estado: 'No verificado en ejecución local en vivo con modelo descargado'**; todos los comandos, flags erróneos y URLs han sido verificados directamente contra la documentación oficial de Ollama y el repositorio de código abierto de Ollama.
