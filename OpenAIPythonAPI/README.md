# OpenAIPythonAPI

Notebook didáctico (`openaipython.ipynb`) con ejemplos de la API de OpenAI: chat completions, generación de imágenes (DALL-E 3), texto a voz (TTS) y transcripción (Whisper). `speech.mp3` es el audio de ejemplo usado por las celdas de Whisper.

## Requisitos

- Python 3.9+
- Una clave de API de OpenAI (las llamadas a la API son de pago)

## Instalar y ejecutar

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r OpenAIPythonAPI/requirements.txt
export OPENAI_API_KEY="tu_clave"      # ver .env.example
jupyter notebook OpenAIPythonAPI/openaipython.ipynb
```

El cliente `OpenAI()` toma la clave de la variable de entorno `OPENAI_API_KEY`; nunca la escribas en el notebook ni la subas al repositorio. `.env.example` es solo una plantilla (el notebook no carga `.env`).

## Notas

- El notebook se versiona **sin outputs**: las respuestas pueden contener URLs firmadas e IDs de organización/usuario. Antes de hacer commit limpia los outputs (`jupyter nbconvert --clear-output --inplace OpenAIPythonAPI/openaipython.ipynb`).
