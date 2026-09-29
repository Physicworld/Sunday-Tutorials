# AgentMCP — agente local con Ollama + FastMCP

Un mini agente de terminal: un modelo local (Ollama) decide cuándo llamar a herramientas expuestas por un servidor [MCP](https://modelcontextprotocol.io) escrito con [FastMCP](https://gofastmcp.com).

```
 ┌────────────┐  prompt / respuesta   ┌──────────────────┐
 │   Tú (CLI) │ ────────────────────▶ │     agent.py     │
 └────────────┘                       │  (cliente MCP)   │
                                      └───┬──────────┬───┘
                    HTTP /api/generate    │          │  MCP sobre stdio
                                          ▼          ▼
                                 ┌────────────┐  ┌───────────────┐
                                 │   Ollama   │  │ mcp_server.py │
                                 │ gemma3:4b  │  │ calcular      │
                                 └────────────┘  │ fecha_actual  │
                                                 └───────────────┘
```

`agent.py` lanza `mcp_server.py` como subproceso (por stdio), descubre sus herramientas y se las describe al modelo en el prompt del sistema. Si el modelo responde con `USAR_HERRAMIENTA: nombre` + `ARGUMENTOS: {...}`, el agente ejecuta la herramienta y pide al modelo una respuesta final.

## Requisitos

- Python 3.11+ (probado con 3.14)
- [Ollama](https://ollama.com) instalado y en ejecución

## Instalación

```bash
# 1. Ollama (Linux; en macOS/Windows usa el instalador de ollama.com)
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &            # si no se ha iniciado como servicio
ollama pull gemma3:4b

# 2. Dependencias Python (desde la raíz del repo)
python -m venv .venv && . .venv/bin/activate
pip install -r AgentMCP/requirements.txt
pip install -r AgentMCP/requirements-dev.txt   # solo para los tests
```

## Ejecutar

```bash
python AgentMCP/agent.py        # funciona desde cualquier carpeta
```

Prueba con `¿cuánto es 2+2*3?` (usa `calcular`) o `¿qué hora es?` (usa `fecha_actual`). Escribe `salir` para terminar.

## Configuración

Variables de entorno (ver `.env.example`; el agente no carga el archivo `.env` por sí solo, expórtalo con `set -a; . AgentMCP/.env; set +a`):

| Variable | Defecto | Descripción |
| --- | --- | --- |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Servidor Ollama |
| `OLLAMA_MODEL` | `gemma3:4b` | Modelo a usar |
| `OLLAMA_TIMEOUT` | `120` | Segundos máximos por petición a Ollama |

## Herramientas

- `calcular(expresion)`: aritmética con números, `+ - * / // % **`, paréntesis y signos. Se evalúa con un intérprete propio basado en `ast` (nunca `eval`). Límites: expresión ≤ 200 caracteres, exponente ≤ 1000, resultados ≤ 10^100; `9**9**9` o `1/0` devuelven un error inmediato.
- `fecha_actual()`: fecha y hora locales.

## Tests

```bash
pytest -q AgentMCP        # no necesita Ollama
```

## Limitaciones

- Un modelo de 4B parámetros falla a menudo: puede inventar herramientas, ignorarlas o devolver argumentos mal formados.
- El protocolo `USAR_HERRAMIENTA` / `ARGUMENTOS` es texto plano y frágil; un modelo con tool-calling nativo sería más fiable.
- Solo se ejecuta una herramienta por turno y el historial es texto sin límite de tokens (se envían las últimas 10 líneas).
