# LLMStudio

Wrapper mínimo en Python sobre la API REST compatible con OpenAI del servidor local de [LM Studio](https://lmstudio.ai).

## Requisitos

- Python 3.9+
- LM Studio con un modelo descargado

## Preparar LM Studio

1. Abre LM Studio y descarga/carga un modelo (p. ej. `gemma-2-2b-it`).
2. En la pestaña **Developer** (Local Server) pulsa **Start Server**. Por defecto escucha en `http://localhost:1234/v1/`.
3. Copia el identificador exacto del modelo cargado (aparece en la lista de modelos).

## Instalar y ejecutar

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r LLMStudio/requirements.txt
export LMSTUDIO_MODEL="identificador-del-modelo"   # opcional; ver .env.example
python LLMStudio/main.py
```

`main.py` lista los modelos y lanza un ejemplo de chat y otro de completion.

## Configuración

| Variable | Por defecto | Uso |
| --- | --- | --- |
| `LMSTUDIO_BASE_URL` | `http://localhost:1234/v1/` | URL base del servidor |
| `LMSTUDIO_MODEL` | `lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf` | Modelo usado en `main.py` |

Las variables se leen del entorno; el script no carga `.env` automáticamente (`.env.example` es una plantilla).

## Errores

Si el servidor está apagado o no responde en 60 s, `main.py` imprime un mensaje claro y termina con código distinto de 0 (sin traceback).
