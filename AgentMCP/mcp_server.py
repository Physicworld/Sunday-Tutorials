import os
import json
import requests
import subprocess
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("Demo Server for Ollama Agent")


@mcp.tool
def obtener_clima(ciudad: str) -> str:
    """Obtiene información del clima para una ciudad específica"""
    try:
        return f"El clima en {ciudad}: 22°C, soleado con nubes dispersas. Humedad: 65%"
    except Exception as e:
        return f"Error al obtener el clima: {e}"


@mcp.tool
def buscar_en_internet(consulta: str) -> str:
    """Simula una búsqueda en internet (placeholder)"""
    return f"Resultados de búsqueda para '{consulta}':\n1. Resultado simulado 1\n2. Resultado simulado 2\n3. Resultado simulado 3\n\n."


@mcp.tool
def listar_archivos(directorio: str = ".") -> str:
    """Lista los archivos en un directorio"""
    try:
        archivos = []
        for item in os.listdir(directorio):
            item_path = os.path.join(directorio, item)
            tipo = "📁" if os.path.isdir(item_path) else "📄"
            size = os.path.getsize(item_path) if os.path.isfile(item_path) else 0
            archivos.append(f"{tipo} {item} ({size} bytes)")

        return f"Archivos en {directorio}:\n" + "\n".join(archivos[:20])  # Limitar a 20
    except Exception as e:
        return f"Error listando archivos: {str(e)}"


@mcp.tool
def leer_archivo(ruta: str) -> str:
    """Lee el contenido de un archivo de texto"""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        return f"Contenido de {ruta}:\n{contenido[:1000]}{'...' if len(contenido) > 1000 else ''}"
    except Exception as e:
        return f"Error leyendo archivo: {str(e)}"


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


@mcp.resource("info://servidor")
def info_servidor() -> str:
    """Información sobre este servidor MCP"""
    return """
    🤖 Servidor MCP Demo para Agente Ollama

    Herramientas disponibles:
    - Gestión de archivos (listar, leer, crear)
    - Cálculos matemáticos
    - Información del sistema
    - Simulación de búsqueda web
    - Información de clima (simulada)

    Versión: 1.0
    Creado para demostrar integración Ollama + MCP
    """

if __name__ == "__main__":
    print("🚀 Servidor MCP Demo iniciado")
    mcp.run()
