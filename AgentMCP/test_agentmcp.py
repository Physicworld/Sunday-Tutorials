"""Tests sin Ollama: evaluador seguro, servidor MCP real y agente con LLM simulado."""
import asyncio
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent as agent_mod  # noqa: E402
import mcp_server  # noqa: E402
from mcp_server import evaluar_expresion  # noqa: E402

AQUI = Path(__file__).resolve().parent


def calcular(expr):
    return mcp_server.calcular(expr)


# ---------- calcular ----------

def test_formato_resultado_igual_que_antes():
    assert calcular("2+3*4") == "Resultado de '2+3*4' = 14"


@pytest.mark.parametrize("expr,esperado", [
    ("(1+2)*3", 9), ("-3+5", 2), ("7//2", 3), ("7%4", 3), ("2**10", 1024),
    ("1/4", 0.25), (" 2 * 3 ", 6), ("--2", 2), ("2**-1", 0.5),
])
def test_aritmetica(expr, esperado):
    assert evaluar_expresion(expr) == esperado


@pytest.mark.parametrize("expr", [
    "9**9**9", "9**9**9**9", "10**1001", "(10**500)*(10**500)", "9.0**999", "2**100000000",
    "1"+"0"*300,
])
def test_dos_rechazado_rapido(expr):
    inicio = time.perf_counter()
    salida = calcular(expr)
    assert time.perf_counter() - inicio < 1
    assert salida.startswith("Error")


def test_division_por_cero():
    assert calcular("1/0").startswith("Error en cálculo")
    assert calcular("1//0").startswith("Error en cálculo")
    assert calcular("1%0").startswith("Error en cálculo")


@pytest.mark.parametrize("expr", [
    "__import__('os').system('id')", "abs(-1)", "a+1", "'a'*3", "True+1", "1 if 1 else 2",
    "[1]*3", "(1,2)", "1;2", "", "2+", "lambda: 1", "1j", "1<2", "(" * 500 + "1" + ")" * 500,
    "-" * 500 + "1", "x" * 500,
])
def test_expresiones_no_permitidas(expr):
    assert calcular(expr).startswith("Error")


def test_fecha_actual_existe():
    assert mcp_server.fecha_actual().startswith("Fecha y hora actual: ")


# ---------- servidor MCP real (stdio) y agente, sin Ollama ----------

def _agente_con_llm_falso(respuestas):
    ag = agent_mod.Agent()
    salidas = iter(respuestas)
    ag.ollama.generate = lambda prompt, system=None: next(salidas)
    return ag


def test_agente_invoca_calcular_via_mcp_desde_otro_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # el servidor se localiza por __file__, no por cwd

    async def escenario():
        ag = _agente_con_llm_falso([
            'USAR_HERRAMIENTA: calcular\nARGUMENTOS: {"expresion": "2+2*3"}',
            "El resultado es 8",
        ])
        await ag.connect_to_mcp()
        try:
            assert {t["name"] for t in ag.available_tools} == {"calcular", "fecha_actual"}
            respuesta = await ag.chat("¿cuánto es 2+2*3?")
            assert await ag.execute_tool(agent_mod.ToolCall("calcular", {"expresion": "2+2*3"})) \
                == "Resultado de '2+2*3' = 8"
            assert (await ag.execute_tool(agent_mod.ToolCall("calcular", {"expresion": "9**9**9"}))).startswith("Error")
            return respuesta
        finally:
            await ag.mcp_client.__aexit__(None, None, None)

    assert asyncio.run(escenario()) == "El resultado es 8"


def test_parse_tool_call():
    ag = agent_mod.Agent()
    call = ag.parse_tool_call('USAR_HERRAMIENTA: calcular\nARGUMENTOS: {"expresion": "1+1"}')
    assert call.name == "calcular" and call.arguments == {"expresion": "1+1"}
    assert ag.parse_tool_call("hola") is None


# ---------- cliente Ollama ----------

def test_ollama_usa_timeout_y_devuelve_error_si_falla(monkeypatch):
    vistos = {}

    def falso_post(url, json=None, timeout=None):
        vistos["timeout"] = timeout
        raise requests.exceptions.Timeout("lento")

    monkeypatch.setattr(agent_mod.requests, "post", falso_post)
    cliente = agent_mod.OllamaClient(base_url="http://x:1/", model="m", timeout=3)
    assert cliente.generate("hola").startswith("Ollama Error")
    assert vistos["timeout"] == 3


def test_configuracion_desde_entorno():
    codigo = (
        "import agent; print(agent.OLLAMA_BASE_URL, agent.OLLAMA_MODEL)"
    )
    salida = subprocess.run(
        [sys.executable, "-c", codigo], cwd=AQUI, capture_output=True, text=True,
        env={"OLLAMA_BASE_URL": "http://otro:9", "OLLAMA_MODEL": "qwen", "PATH": ""},
        check=True,
    ).stdout.strip()
    assert salida == "http://otro:9 qwen"
    defecto = subprocess.run(
        [sys.executable, "-c", codigo], cwd=AQUI, capture_output=True, text=True,
        env={"PATH": ""}, check=True,
    ).stdout.strip()
    assert defecto == "http://localhost:11434 gemma3:4b"
