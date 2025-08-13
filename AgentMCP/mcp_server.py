import os
import json
import requests
import subprocess
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("Demo Server for Ollama Agent")

@mcp.tool
def calcular(expresion: str) -> str:
    """Calcula una expresion matemática simple"""
    try:
        # Solo permitir operaciones seguras
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expresion):
            return "Error: Solo se permiten números y operadores básicos (+, -, *, /, (), .)"

        resultado = eval(expresion)
        return f"Resultado de '{expresion}' = {resultado}"
    except Exception as e:
        return f"Error en cálculo: {str(e)}"


@mcp.tool
def fecha_actual() -> str:
    """Obtiene la fecha y hora actual"""
    now = datetime.now()
    return f"Fecha y hora actual: {now.strftime('%Y-%m-%d %H:%M:%S')}"


if __name__ == "__main__":
    print("🚀 Servidor MCP Demo iniciado")
    mcp.run()
